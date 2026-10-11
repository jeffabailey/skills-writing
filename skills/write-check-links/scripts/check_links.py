#!/usr/bin/env python3
"""Run lychee on one Markdown file and triage the results for a Hugo site.

Usage:
  check_links.py <file.md> [--lychee-json report.json] [--config lychee.toml]

What it does, in order:
  1. Preflight: lychee on PATH (exit 3 with an install hint if not).
  2. Finds the git root and the lychee.toml (walks up from the file; also
     accepts a dir holding hugo.toml / config.toml / config/_default).
  3. Runs lychee FROM THE GIT ROOT so the repo-root .lycheeignore applies.
  4. Triages every failure into: broken / known false positive / unverified,
     with the source line and a suggested fix.
  5. Checks {{< ref >}} / {{< relref >}} targets against hugo/content (lychee
     never sees them).

Exit codes: 0 nothing broken, 1 broken links found, 3 lychee missing,
4 lychee.toml not found, 5 lychee crashed / no JSON produced.
Unverified links (timeouts, 5xx) do not fail the run; they are listed.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlparse

HUGO_CONFIGS = ("hugo.toml", "hugo.yaml", "hugo.json", "config.toml", "config.yaml", "config.json")
ASSET_EXT = re.compile(r"\.(png|jpe?g|gif|webp|svg|avif|pdf|mp4|webm|mp3|zip|txt|json|csv)$", re.IGNORECASE)
REF_RE = re.compile(r"\{\{<\s*(?:rel)?ref\s+\"([^\"]+)\"\s*>\}\}")


def die(code: int, msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def git_root(start: Path) -> Path | None:
    try:
        out = subprocess.run(["git", "-C", str(start), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        return Path(out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def find_site(file: Path, stop: Path | None) -> tuple[Path | None, Path | None]:
    """Return (hugo_dir, lychee_toml). Walk up from the file, then check <root>/hugo."""
    candidates = list(file.parents)
    if stop is not None:
        candidates += [stop / "hugo", stop]
    hugo_dir = lychee = None
    for d in candidates:
        if lychee is None and (d / "lychee.toml").is_file():
            lychee = d / "lychee.toml"
        if hugo_dir is None and (any((d / c).is_file() for c in HUGO_CONFIGS) or (d / "config/_default").is_dir()):
            hugo_dir = d
        if hugo_dir and lychee:
            break
        if stop is not None and d == stop:
            # keep scanning the explicit <root>/hugo fallback appended above
            continue
    return hugo_dir, lychee


def read_base_url(lychee_toml: Path) -> str:
    m = re.search(r'^\s*base_url\s*=\s*"([^"]+)"', lychee_toml.read_text(), re.MULTILINE)
    return m.group(1).rstrip("/") if m else ""


def front_matter(md: Path) -> dict:
    try:
        text = md.read_text(errors="replace")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^(url|slug|draft):\s*\"?([^\"#]*?)\"?\s*$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def build_index(content: Path) -> list[dict]:
    pages = []
    for md in content.rglob("*.md"):
        if md.name in ("index.md", "_index.md"):
            rel_dir = md.parent.relative_to(content)
            name = md.parent.name
        else:
            rel_dir = md.relative_to(content).with_suffix("")
            name = md.stem
        fm = front_matter(md)
        parts = list(rel_dir.parts)
        if fm.get("slug") and parts and md.name != "_index.md":
            parts[-1] = fm["slug"]
        derived = "/" + "/".join(parts) + "/" if parts else "/"
        urls = {derived.lower()}
        if fm.get("url"):
            u = fm["url"]
            urls.add(("/" + u.strip("/") + "/").lower() if u.strip("/") else "/")
        pages.append({"file": md, "name": name, "rel": str(rel_dir), "urls": urls,
                      "slug": fm.get("slug", ""), "draft": fm.get("draft", "false").lower() == "true"})
    return pages


def resolve_page(path: str, pages: list[dict]) -> tuple[dict | None, list[str]]:
    p = "/" + unquote(path).split("#")[0].split("?")[0].strip("/") + "/"
    p = p.lower() if p != "//" else "/"
    for pg in pages:
        if p in pg["urls"]:
            return pg, []
    last = p.strip("/").split("/")[-1]
    names = sorted({pg["slug"] or pg["name"] for pg in pages} | {pg["name"] for pg in pages})
    return None, difflib.get_close_matches(last, names, n=2, cutoff=0.6)


def resolve_ref(ref: str, article: Path, content: Path, pages: list[dict]) -> tuple[list[dict], list[str]]:
    target = ref.split("#")[0]
    if not target:
        return [{"file": article, "draft": False}], []
    if "/" in target.strip("/"):
        bases = [content / target.lstrip("/"), article.parent / target]
        hits = []
        for b in bases:
            b = b.with_suffix("") if b.suffix == ".md" else b
            for c in (b.with_suffix(".md"), b / "index.md", b / "_index.md"):
                if c.is_file():
                    hits.append({"file": c, "draft": front_matter(c).get("draft", "false").lower() == "true"})
        if hits:
            return hits[:1], []
    key = target.strip("/").split("/")[-1].removesuffix(".md")
    hits = [pg for pg in pages if pg["name"] == key]
    return hits, ([] if hits else difflib.get_close_matches(key, sorted({pg["name"] for pg in pages}), n=2, cutoff=0.6))


def host_resolves(url: str) -> bool:
    host = urlparse(url).hostname
    if not host:
        return False
    try:
        socket.getaddrinfo(host, None)
        return True
    except OSError:
        return False


def find_line(article_lines: list[str], url: str, base_url: str) -> int | None:
    needles = [url]
    if base_url and url.startswith(base_url):
        tail = url[len(base_url):]
        needles += [tail, tail.lstrip("/")]
    for n in needles:
        for i, line in enumerate(article_lines, 1):
            if n and n in line:
                return i
    return None


def triage(entry: dict, kind: str, article: Path, base_url: str, content: Path | None,
           static: Path | None, pages: list[dict] | None) -> tuple[str, str, str]:
    """Return (status, verdict, fix)."""
    url = entry["url"]
    st = entry.get("status", {})
    code = st.get("code")
    text = st.get("details") or st.get("text") or ""
    status = str(code) if code else ("TIMEOUT" if kind == "timeout" else text.split(".")[0][:40])

    if kind == "timeout":
        return status, "unverified", "Host did not answer in time. Open it in a browser or re-run later; if CI is blocked by this host for good, add a regex to the repo-root .lycheeignore."

    internal = bool(base_url) and url.startswith(base_url)
    if internal:
        path = urlparse(url).path
        if ASSET_EXT.search(path):
            name = Path(unquote(path)).name
            if (article.parent / unquote(path).lstrip("/")).is_file() or (article.parent / name).is_file():
                return status, "known false positive", f"`{name}` exists next to the article; lychee rewrote the bundle-relative path onto {base_url}. No action."
            if static is not None and (static / unquote(path).lstrip("/")).is_file():
                return status, "known false positive", f"File exists in hugo/static{path}; it will deploy with the site. No action."
            return status, "broken", f"`{name}` is not in {article.parent.name}/ (or static/). Add the file next to index.md or fix the filename."
        if pages is not None:
            pg, close = resolve_page(path, pages)
            if pg and pg["draft"]:
                return status, "broken", f"Target is a draft ({pg['rel']}); it will 404 once this post publishes. Publish it first or drop the link."
            if pg:
                return status, "unverified", f"Exists in content ({pg['rel']}) but not live yet; it should work after deploy. Prefer {{{{< ref \"{pg['name']}\" >}}}} so the build checks it."
            hint = f" Closest content: {', '.join(close)}." if close else ""
            return status, "broken", f"No page under hugo/content has this URL.{hint} Fix the path or use {{{{< ref \"<bundle-name>\" >}}}}."

    if kind == "error" and not code:
        if not host_resolves(url):
            return "DNS", "broken", "Host does not resolve (domain gone or typo). Replace the link, or point at a Wayback Machine copy: https://web.archive.org/web/*/" + url
        return status, "unverified", "Connection failed but the host resolves; may be a network or bot block. Check in a browser, then re-run."
    if code and int(code) >= 500:
        return status, "unverified", "Server error; often transient. Re-run later before changing the link."
    if code in (404, 410):
        return status, "broken", "Page is gone. Search the site for its new location, or use a Wayback copy: https://web.archive.org/web/*/" + url
    return status, "broken", "Rejected status. Check the URL in a browser and fix or replace it."


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--config", help="explicit lychee.toml")
    ap.add_argument("--lychee-json", help="re-triage an existing lychee --format json report instead of running lychee")
    a = ap.parse_args()

    article = Path(a.file).resolve()
    if not article.is_file():
        die(2, f"File not found: {a.file}")

    if not a.lychee_json and shutil.which("lychee") is None:
        die(3, "TOOL MISSING: lychee is not installed (this is not a link failure).\n"
               "Install: brew install lychee   (or: cargo install lychee)\n"
               "CI pins lychee v0.22.0 via lycheeverse/lychee-action@v2.")

    root = git_root(article.parent) or Path.cwd()
    hugo_dir, lychee_toml = find_site(article, root)
    if a.config:
        lychee_toml = Path(a.config).resolve()
    if lychee_toml is None:
        die(4, "No lychee.toml found above the file or in <git-root>/hugo. Pass --config <path>.")

    base_url = read_base_url(lychee_toml)
    content = hugo_dir / "content" if hugo_dir and (hugo_dir / "content").is_dir() else None
    static = hugo_dir / "static" if hugo_dir and (hugo_dir / "static").is_dir() else None
    ignore = root / ".lycheeignore"

    rel_article = os.path.relpath(article, root)
    print(f"git root:     {root}")
    print(f"lychee.toml:  {os.path.relpath(lychee_toml, root)}")
    print(f".lycheeignore: {'applied (cwd = git root)' if ignore.is_file() else 'none at git root'}")
    print(f"hugo content: {content or 'not found (internal links checked live only)'}")

    if a.lychee_json:
        report = json.loads(Path(a.lychee_json).read_text())
    else:
        ver = subprocess.run(["lychee", "--version"], capture_output=True, text=True).stdout.strip()
        print(f"lychee:       {ver} (CI pins v0.22.0); expect ~40s with max_concurrency=4 and retries")
        tmp = Path(tempfile.mkdtemp()) / "lychee.json"
        cmd = ["lychee", "--config", os.path.relpath(lychee_toml, root), "--format", "json",
               "--output", str(tmp), rel_article]
        print("command:      (cd " + str(root) + " && " + " ".join(cmd) + ")")
        proc = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        if not tmp.is_file():
            die(5, f"lychee produced no report (exit {proc.returncode}):\n{proc.stderr[-2000:]}")
        report = json.loads(tmp.read_text())

    pages = build_index(content) if content else None
    lines = article.read_text(errors="replace").splitlines()

    rows = []
    for kind, key in (("error", "error_map"), ("timeout", "timeout_map")):
        for entries in (report.get(key) or {}).values():
            for e in entries:
                line = (e.get("span") or {}).get("line") or find_line(lines, e["url"], base_url)
                status, verdict, fix = triage(e, kind, article, base_url, content, static, pages)
                rows.append((line or 0, e["url"], status, verdict, fix))
    rows.sort()

    ref_rows = []
    if content is not None:
        for i, line in enumerate(lines, 1):
            for ref in REF_RE.findall(line):
                hits, close = resolve_ref(ref, article, content, pages)
                if len(hits) > 1:
                    ref_rows.append((i, ref, "broken", f"Ambiguous: {len(hits)} pages named `{ref}`; use the content path."))
                elif not hits:
                    hint = f" Closest: {', '.join(close)}." if close else ""
                    ref_rows.append((i, ref, "broken", f"REF_NOT_FOUND: no bundle or file named `{ref}`.{hint} refs match the folder name, not the slug."))
                elif hits[0]["draft"]:
                    ref_rows.append((i, ref, "broken", "Target is draft: true; the normal build fails with REF_NOT_FOUND."))
                else:
                    ref_rows.append((i, ref, "ok", os.path.relpath(hits[0]["file"], root)))

    print()
    print(f"lychee: {report.get('total', 0)} links, {report.get('successful', 0)} OK, "
          f"{report.get('excludes', 0)} excluded, {report.get('errors', 0)} errors, {report.get('timeouts', 0)} timeouts")
    print()
    if rows:
        print("| Line | URL | Status | Verdict | Fix |")
        print("| ---: | --- | --- | --- | --- |")
        for line, url, status, verdict, fix in rows:
            print(f"| {line or '?'} | {url} | {status} | {verdict} | {fix} |")
    else:
        print("No failing URLs from lychee.")
    if ref_rows:
        print()
        print("Hugo ref/relref targets (not seen by lychee; checked against hugo/content):")
        print()
        print("| Line | ref | Verdict | Detail |")
        print("| ---: | --- | --- | --- |")
        for r in ref_rows:
            print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")

    broken = sum(1 for r in rows if r[3] == "broken") + sum(1 for r in ref_rows if r[2] == "broken")
    unverified = sum(1 for r in rows if r[3] == "unverified")
    fp = sum(1 for r in rows if r[3] == "known false positive")
    print()
    print(f"SUMMARY: broken={broken} unverified={unverified} known_false_positive={fp} "
          f"refs_checked={len(ref_rows)}")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()

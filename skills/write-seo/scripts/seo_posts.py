#!/usr/bin/env python3
"""Helpers for write-seo on the jeffbaileyblog Hugo site (stdlib only).

Subcommands (run from anywhere; --hugo-dir points at the site's hugo/ folder):

  list     Published blog posts from `hugo list all`, with the ref key Hugo resolves.
           --match TERM ... keeps rows whose title or path contains any term.
  refs     Check every {{< ref "..." >}} in a file against the published list.
  fm       Check a post's title/description/keywords against seo-front-matter.md.
  drift    Compare the bundled prompt copy with the blog's authoritative prompt.

`hugo list all` is the source of truth for published (draft=false) posts. Hugo
resolves `ref` by content path / bundle folder name, NOT by front-matter slug,
so the `ref` column below is the bundle folder name (or file stem).
"""
import argparse
import csv
import io
import os
import re
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_PROMPT = os.path.join(SKILL_DIR, "references", "seo-front-matter.md")


def load_rows(hugo_dir, csv_path=None):
    if csv_path:
        with open(csv_path, newline="", encoding="utf-8") as fh:
            text = fh.read()
    else:
        try:
            text = subprocess.run(
                ["hugo", "list", "all"], cwd=hugo_dir, check=True,
                capture_output=True, text=True).stdout
        except FileNotFoundError:
            sys.exit("tool missing: hugo (install: brew install hugo)")
        except subprocess.CalledProcessError as err:
            sys.exit(f"check failed: `hugo list all` in {hugo_dir}: {err.stderr.strip()}")
    return list(csv.DictReader(io.StringIO(text)))


def ref_key(path):
    base = os.path.basename(path)
    if base in ("index.md", "_index.md"):
        return os.path.basename(os.path.dirname(path))
    return os.path.splitext(base)[0]


def published_posts(rows):
    out = []
    for r in rows:
        p = r.get("path", "")
        if r.get("draft") != "false" or not p.startswith("content/blog/"):
            continue
        if os.path.basename(p) == "_index.md":
            continue
        r = dict(r)
        r["ref"] = ref_key(p)
        url_last = r.get("permalink", "").rstrip("/").split("/")[-1]
        r["slug_mismatch"] = bool(r.get("slug")) and r["slug"] != r["ref"] or (
            not r.get("slug") and url_last != r["ref"])
        out.append(r)
    return out


def cmd_list(a):
    posts = published_posts(load_rows(a.hugo_dir, a.csv))
    terms = [t.lower() for t in (a.match or [])]
    if terms:
        posts = [p for p in posts
                 if any(t in (p["title"] + " " + p["path"]).lower() for t in terms)]
    print("ref\ttitle\tpath\tnote")
    for p in sorted(posts, key=lambda x: x["path"]):
        note = f"slug={p['slug'] or '-'} differs from folder; ref uses folder" if p["slug_mismatch"] else ""
        print(f"{p['ref']}\t{p['title']}\t{p['path']}\t{note}")
    print(f"# {len(posts)} published posts", file=sys.stderr)


REF_RE = re.compile(r'\{\{<\s*ref\s+"([^"]+)"\s*>\}\}')


def cmd_refs(a):
    rows = load_rows(a.hugo_dir, a.csv)
    published = {p["ref"] for p in published_posts(rows)}
    by_path = {r["path"]: r for r in rows}
    drafts = {ref_key(r["path"]) for r in rows if r.get("draft") == "true"}
    slugs = {r["slug"]: ref_key(r["path"]) for r in rows if r.get("slug")}
    text = open(a.file, encoding="utf-8").read()
    bad = 0
    for target in sorted(set(REF_RE.findall(text))):
        key = target.strip("/").split("/")[-1]
        full = "content/" + target.strip("/") + ("/index.md" if not target.endswith(".md") else "")
        if key in published or (full in by_path and by_path[full].get("draft") == "false"):
            print(f"ok\t{target}")
            continue
        bad += 1
        if key in drafts:
            print(f"FAIL\t{target}\tdraft post (breaks the normal build)")
        elif key in slugs:
            print(f"FAIL\t{target}\tthat is a slug; use the folder name: {slugs[key]}")
        else:
            print(f"FAIL\t{target}\tnot in `hugo list all` (REF_NOT_FOUND)")
    sys.exit(1 if bad else 0)


def split_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        sys.exit("check failed: no YAML front matter")
    return m.group(1)


def fm_fields(fm):
    """Minimal YAML reader: top-level scalars, block lists, flow lists."""
    fields, raw, key = {}, {}, None
    for line in fm.splitlines():
        m = re.match(r"^([A-Za-z_][\w.-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2)
            raw[key] = val
            if val.startswith("["):
                fields[key] = [v.strip().strip("'\"") for v in val.strip("[]").split(",") if v.strip()]
            elif val == "":
                fields[key] = []
            else:
                fields[key] = val.strip().strip("'\"") if val[:1] in "'\"" else val.strip()
        elif key and re.match(r"^\s+-\s+", line) and isinstance(fields.get(key), list):
            fields[key].append(re.sub(r"^\s+-\s+", "", line).strip().strip("'\""))
        elif not line.startswith(" "):
            key = None
    return fields, raw


def cmd_fm(a):
    fields, raw = fm_fields(split_front_matter(open(a.file, encoding="utf-8").read()))
    problems, notes = [], []
    title = fields.get("title", "")
    desc = fields.get("description", "")
    kws = fields.get("keywords") or []
    cats = [c.lower() for c in (fields.get("categories") or [])]

    if not title:
        problems.append("title missing")
    elif len(title) > 60:
        notes.append(f"title is {len(title)} chars; keep the essential meaning in the first ~60")
    if a.csv or a.hugo_dir:
        rows = load_rows(a.hugo_dir, a.csv)
        own = os.path.abspath(a.file)
        clashes = [r["path"] for r in rows
                   if r.get("title", "").strip().lower() == title.strip().lower()
                   and not own.endswith(r["path"].removeprefix("content"))]
        if clashes:
            problems.append(f"title not unique; also used by: {', '.join(clashes)}")
    if not raw.get("description", "").startswith('"'):
        problems.append("description is not double-quoted")
    if len(desc) > 160:
        problems.append(f"description is {len(desc)} chars (> 160)")
    if not 4 <= len(kws) <= 7:
        problems.append(f"keywords has {len(kws)} entries (want 4-7)")
    dup_cat = [k for k in kws if k.lower() in cats]
    if dup_cat:
        problems.append(f"keywords duplicate categories: {dup_cat}")
    seen = set()
    for k in kws:
        if k.lower() in seen:
            problems.append(f"duplicate keyword: {k}")
        seen.add(k.lower())
    for k in ("url", "slug"):
        if raw.get(k, "")[:1] in "'\"" and raw.get(k):
            problems.append(f"{k} must be bare (unquoted)")
    if kws and title and kws[0].lower().split()[0] not in (title + " " + desc).lower():
        notes.append("first keyword's head term is absent from title/description; check cross-field agreement")

    print(f"title ({len(title)}): {title}")
    print(f"description ({len(desc)}): {desc}")
    print(f"keywords ({len(kws)}): {kws}")
    for n in notes:
        print(f"note\t{n}")
    for p in problems:
        print(f"FAIL\t{p}")
    print("PASS" if not problems else f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)


def prompt_body(text):
    m = re.search(r"\{\{%\s*prompt-text[^%]*%\}\}(.*?)\{\{%\s*/prompt-text\s*%\}\}", text, re.DOTALL)
    if m:
        text = m.group(1)
    elif text.startswith("---\n"):
        text = text.split("\n---\n", 1)[-1]
    return "\n".join(l.rstrip() for l in text.strip().splitlines())


def cmd_drift(a):
    blog = os.path.join(a.hugo_dir, "content", "prompts", "seo-front-matter.md")
    if not os.path.exists(blog):
        print(f"offline: {blog} not found; using bundled fallback {LOCAL_PROMPT}")
        return
    same = prompt_body(open(blog, encoding="utf-8").read()) == prompt_body(open(LOCAL_PROMPT, encoding="utf-8").read())
    if same:
        print(f"in sync: {blog}")
    else:
        print(f"DRIFT: bundled copy differs from {blog}. Follow the blog file; "
              f"refresh the copy with: python3 {__file__} drift --hugo-dir {a.hugo_dir} --update")
        if a.update:
            with open(LOCAL_PROMPT, "w", encoding="utf-8") as fh:
                fh.write(prompt_body(open(blog, encoding="utf-8").read()) + "\n")
            print("bundled copy refreshed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hugo-dir", default=os.path.expanduser("~/Projects/websites/jeffbaileyblog/hugo"))
    ap.add_argument("--csv", help="use a saved `hugo list all` CSV instead of running hugo")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("--match", nargs="*"); s.set_defaults(fn=cmd_list)
    s = sub.add_parser("refs"); s.add_argument("file"); s.set_defaults(fn=cmd_refs)
    s = sub.add_parser("fm"); s.add_argument("file"); s.set_defaults(fn=cmd_fm)
    s = sub.add_parser("drift"); s.add_argument("--update", action="store_true"); s.set_defaults(fn=cmd_drift)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()

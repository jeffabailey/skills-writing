#!/usr/bin/env python3
"""Front-matter checker for jeffbaileyblog posts (rules from hugo/AGENTS.md
"Front matter" + "Cover images" and content/prompts/seo-front-matter.md).

None of these break `hugo`, which is why they need a mechanical check.

BLOCKING  quoted url / slug / cover.image; date or lastmod not YYYY-MM-DD;
          missing title / description / cover.image; description unquoted.
WARNING   description > 160 chars; slug, url tail, bundle dir, or cover name disagree;
          cover file missing beside index.md; type/author not post/Jeff Bailey;
          keywords count outside 4-7.
INFO      draft status (tells you whether the build needs --buildDrafts).

Usage: check_front_matter.py path/to/index.md
Exit:  0 = no blocking, 1 = blocking found, 2 = could not parse.
"""
import re
import sys
from pathlib import Path


def raw_front_matter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return None


def parse(lines):
    """Tiny YAML subset: top-level scalars, `cover:` children, list counts. Keeps raw values."""
    top, cover, lists, cur = {}, {}, {}, None
    for ln in lines:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\S[^:]*):\s*(.*)$", ln)
        if m:
            cur = m.group(1).strip()
            top[cur] = m.group(2).rstrip()
            continue
        m = re.match(r"^\s+-\s*(.*)$", ln)
        if m and cur:
            lists.setdefault(cur, []).append(m.group(1))
            continue
        m = re.match(r"^\s+(\w+):\s*(.*)$", ln)
        if m and cur == "cover":
            cover[m.group(1)] = m.group(2).rstrip()
    return top, cover, lists


def is_quoted(v: str) -> bool:
    v = v.strip()
    return len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'"


def unq(v: str) -> str:
    v = (v or "").strip()
    return v[1:-1] if is_quoted(v) else v


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    try:
        fm = raw_front_matter(path.read_text(encoding="utf-8"))
    except OSError as e:
        print(f"ERROR: {e}")
        return 2
    if fm is None:
        print("BLOCKING no YAML front matter (--- ... ---) found")
        return 1
    top, cover, lists = parse(fm)
    out = []

    def rep(level, msg):
        out.append((level, msg))

    for key, val in (("url", top.get("url")), ("slug", top.get("slug")), ("cover.image", cover.get("image"))):
        if val is not None and is_quoted(val):
            rep("BLOCKING", f"{key} is quoted ({val}); write it bare: {key.split('.')[-1]}: {unq(val)}")

    for key in ("date", "lastmod"):
        v = top.get(key)
        if v is None:
            rep("BLOCKING" if key == "date" else "WARNING", f"{key} missing; use YYYY-MM-DD")
        elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}", unq(v)):
            rep("BLOCKING", f"{key}: {v} is not YYYY-MM-DD (no ISO timestamps); use {key}: {unq(v)[:10]}")
    if top.get("date") and top.get("lastmod") and unq(top["lastmod"])[:10] < unq(top["date"])[:10]:
        rep("WARNING", "lastmod is earlier than date")

    if not unq(top.get("title", "")):
        rep("BLOCKING", "title missing")
    desc = top.get("description")
    if desc is None or not unq(desc):
        rep("BLOCKING", "description missing")
    else:
        if not is_quoted(desc):
            rep("BLOCKING", "description is not quoted (an unquoted colon breaks YAML); wrap it in double quotes")
        n = len(unq(desc))
        if n > 160:
            rep("WARNING", f"description is {n} chars; seo-front-matter.md caps it at 160")

    bundle = path.parent.name if path.name == "index.md" else path.stem
    slug = unq(top.get("slug", "")) or None
    url = unq(top.get("url", "")) or None
    url_tail = url.rstrip("/").split("/")[-1] if url else None
    effective = slug or url_tail or bundle
    if url and not re.fullmatch(r"/blog/\d{4}/\d{2}/\d{2}/[^/\s]+/?", url):
        rep("WARNING", f"url {url} does not match /blog/YYYY/MM/DD/<slug>")
    if url and top.get("date") and re.match(r"/blog/\d{4}/\d{2}/\d{2}/", url):
        if url[6:16].replace("/", "-") != unq(top["date"])[:10]:
            rep("INFO", f"url date {url[6:16]} differs from date {unq(top['date'])[:10]} (fine for a revised post)")
    names = {"slug": slug, "url tail": url_tail, "bundle dir": bundle}
    present = {k: v for k, v in names.items() if v}
    if len(set(present.values())) > 1:
        rep("WARNING", "slug / url tail / bundle dir disagree: " + ", ".join(f"{k}={v}" for k, v in present.items())
            + "  ({{< ref >}} resolves by the bundle path, not slug)")

    img = unq(cover.get("image", "")) if cover else ""
    if "cover" not in top:
        rep("BLOCKING", f"cover block missing; add cover: image: {effective}.png, relative: true, alt")
    elif not img:
        rep("BLOCKING", f"cover.image missing; use image: {effective}.png")
    else:
        if Path(img).stem != effective or not img.endswith(".png"):
            rep("WARNING", f"cover.image {img} should be {effective}.png")
        if not img.startswith(("http", "/")) and not (path.parent / img).is_file():
            rep("WARNING", f"cover file {img} not found beside {path.name} (generate it with generate-cover-image)")
        if not unq(cover.get("alt", "")):
            rep("WARNING", "cover.alt missing; describe what the image shows")
        if cover.get("relative", "").strip() != "true":
            rep("WARNING", "cover.relative should be true for a bundled cover")

    if unq(top.get("type", "post")) != "post":
        rep("WARNING", f"type is {top.get('type')}; blog posts use type: post")
    if top.get("author") is not None and unq(top["author"]) != "Jeff Bailey":
        rep("WARNING", f"author is {top['author']}; blog posts use author: Jeff Bailey")
    kw = lists.get("keywords", [])
    if "keywords" in top and not (4 <= len(kw) <= 7):
        rep("WARNING", f"{len(kw)} keywords; seo-front-matter.md asks for 4-7")

    draft = unq(top.get("draft", "false")).lower() == "true"
    rep("INFO", f"draft: {'true -> build with --buildDrafts' if draft else 'false'}; effective slug: {effective}")

    print(f"# front-matter check: {path}")
    order = {"BLOCKING": 0, "WARNING": 1, "INFO": 2}
    for level, msg in sorted(out, key=lambda x: order[x[0]]):
        print(f"{level} {msg}")
    return 1 if any(l == "BLOCKING" for l, _ in out) else 0


if __name__ == "__main__":
    sys.exit(main())

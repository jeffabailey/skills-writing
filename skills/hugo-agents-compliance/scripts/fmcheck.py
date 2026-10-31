#!/usr/bin/env python3
"""Check a jeffbaileyblog post's front matter against hugo/archetypes/blog.md (the
field list, with each field's rule in a template comment) and
content/prompts/seo-front-matter.md.

Shared by hugo-agents-compliance (authoring) and write-validate-article (the
read-only gate, which calls it by sibling path). Keep one copy.

None of these break `hugo`, which is why they need a mechanical check.

BLOCK  quoted url / slug / cover.image; url missing; date missing or not
       YYYY-MM-DD; lastmod not YYYY-MM-DD; title / description / cover.image
       missing; description unquoted; categories empty.
WARN   description > 160 chars (must-fix on new posts, legacy posts keep their
       wording); slug, url tail, bundle dir, or cover name disagree; url not
       /blog/YYYY/MM/DD/<slug>; cover file missing (hand off to
       generate-cover-image); cover.alt missing; cover.relative not true;
       lastmod missing or earlier than date; type/author not post/Jeff Bailey;
       keywords missing or outside 4-7; a category not yet used on the site.
INFO   draft status (draft: true needs a --buildDrafts build) and effective slug.

Usage: fmcheck.py path/to/index.md
Exit:  0 no BLOCK, 1 BLOCK found, 2 usage error or unreadable file.
"""
import json
import os
import re
import sys
from pathlib import Path


def raw_front_matter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return None


def parse(lines):
    """Tiny YAML subset: top-level scalars, `cover:` children, lists (block or [a, b])."""
    top, cover, lists, cur = {}, {}, {}, None
    for ln in lines:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\S[^:]*):[ \t]*(.*)$", ln)
        if m:
            cur = m.group(1).strip()
            val = m.group(2).rstrip()
            top[cur] = val
            if val.startswith("[") and val.endswith("]"):
                lists[cur] = [x.strip() for x in val[1:-1].split(",") if x.strip()]
            continue
        m = re.match(r"^\s+-\s*(.*)$", ln)
        if m and cur:
            lists.setdefault(cur, []).append(m.group(1))
            continue
        m = re.match(r"^\s+(\w+):\s*(.*)$", ln)
        if m and cur == "cover":
            cover[m.group(1)] = m.group(2).rstrip()
    return top, cover, lists


def is_quoted(v):
    v = (v or "").strip()
    return len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'"


def unq(v):
    v = (v or "").strip()
    return v[1:-1] if is_quoted(v) else v


def find_site_root(p):
    d = p.resolve().parent
    for cand in [d, *d.parents]:
        if (cand / "content").is_dir() and any((cand / c).is_file() for c in (
                "config.toml", "hugo.toml", "config.yaml", "hugo.yaml", "config.json", "hugo.json")):
            return cand
    return None


def check(path):
    fm = raw_front_matter(path.read_text(encoding="utf-8"))
    if fm is None:
        return [("BLOCK", "no YAML front matter (--- ... ---) found")], None
    top, cover, lists = parse(fm)
    out = []

    def rep(level, msg):
        out.append((level, msg))

    for key, val in (("url", top.get("url")), ("slug", top.get("slug")), ("cover.image", cover.get("image"))):
        if val is not None and is_quoted(val):
            rep("BLOCK", f"{key} is quoted ({val}); write it bare: {key.split('.')[-1]}: {unq(val)}")
    if not unq(top.get("url")):
        rep("BLOCK", "url missing; use url: /blog/YYYY/MM/DD/<slug>")

    for key in ("date", "lastmod"):
        v = top.get(key)
        if v is None:
            rep("BLOCK" if key == "date" else "WARN", f"{key} missing; use {key}: YYYY-MM-DD")
        elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}", unq(v)):
            rep("BLOCK", f"{key}: {v} is not YYYY-MM-DD (no ISO timestamps); use {key}: {unq(v)[:10]}")
    if top.get("date") and top.get("lastmod") and unq(top["lastmod"])[:10] < unq(top["date"])[:10]:
        rep("WARN", "lastmod is earlier than date")

    if not unq(top.get("title")):
        rep("BLOCK", "title missing")
    desc = top.get("description")
    if desc is None or not unq(desc):
        rep("BLOCK", "description missing")
    else:
        if not is_quoted(desc):
            rep("BLOCK", "description is not quoted (an unquoted colon breaks YAML); wrap it in double quotes")
        n = len(unq(desc))
        if n > 160:
            rep("WARN", f"description is {n} chars; seo-front-matter.md caps it at 160 "
                        "(fix on new posts; on legacy posts suggest, do not reword)")

    bundle = path.parent.name if path.name == "index.md" else path.stem
    slug = unq(top.get("slug")) or None
    url = unq(top.get("url")) or None
    url_tail = url.rstrip("/").split("/")[-1] if url else None
    effective = slug or url_tail or bundle
    if url and not re.fullmatch(r"/blog/\d{4}/\d{2}/\d{2}/[^/\s]+/?", url):
        rep("WARN", f"url {url} does not match /blog/YYYY/MM/DD/<slug>")
    if url and top.get("date") and re.match(r"/blog/\d{4}/\d{2}/\d{2}/", url):
        if url[6:16].replace("/", "-") != unq(top["date"])[:10]:
            rep("INFO", f"url date {url[6:16]} differs from date {unq(top['date'])[:10]} (fine for a revised post)")
    present = {k: v for k, v in {"slug": slug, "url tail": url_tail, "bundle dir": bundle}.items() if v}
    if len(set(present.values())) > 1:
        rep("WARN", "slug / url tail / bundle dir disagree: " + ", ".join(f"{k}={v}" for k, v in present.items())
            + f"  ({{{{< ref >}}}} resolves by the bundle folder: {bundle})")

    img = unq(cover.get("image"))
    if "cover" not in top:
        rep("BLOCK", f"cover block missing; add cover: image: {effective}.png, relative: true, alt")
    elif not img:
        rep("BLOCK", f"cover.image missing; use image: {effective}.png")
    else:
        if Path(img).stem != effective or not img.endswith(".png"):
            rep("WARN", f"cover.image {img} should be {effective}.png")
        if not img.startswith(("http", "/")) and not (path.parent / img).is_file():
            rep("WARN", f"cover file {img} not found beside {path.name}: hand off to generate-cover-image")
        if not unq(cover.get("alt")):
            rep("WARN", "cover.alt missing; describe what the image shows (open the PNG first)")
        if cover.get("relative", "").strip() != "true":
            rep("WARN", "cover.relative should be true for a bundled cover")

    cats = [unq(c) for c in lists.get("categories", [])]
    if not cats:
        rep("BLOCK", "categories empty or missing; pick at least one existing category")
    else:
        root = find_site_root(path)
        meta = root / "data" / "site-metadata.json" if root else None
        if meta and meta.is_file():
            try:
                known = set(json.loads(meta.read_text(encoding="utf-8")).get("categories", []))
            except (ValueError, OSError):
                known = set()
            for term in (root / "content" / "categories").glob("*/_index.md"):
                # data/site-metadata.json is generated and lags new categories.
                m = re.search(r"^title:\s*(.+)$", term.read_text(encoding="utf-8"), re.M)
                if m:
                    known.add(unq(m.group(1)))
            new = [c for c in cats if known and c not in known]
            if new:
                rep("WARN", f"categories not yet used on the site: {new} (prefer existing ones)")

    if unq(top.get("type")) != "post":
        rep("WARN", f"type is {top.get('type') or 'missing'}; blog posts use type: post")
    if unq(top.get("author")) != "Jeff Bailey":
        rep("WARN", f"author is {top.get('author') or 'missing'}; blog posts use author: Jeff Bailey")
    kw = lists.get("keywords", [])
    if not kw:
        rep("WARN", "keywords missing; seo-front-matter.md asks for 4-7")
    elif not 4 <= len(kw) <= 7:
        rep("WARN", f"{len(kw)} keywords; seo-front-matter.md asks for 4-7")

    draft = unq(top.get("draft", "false")).lower() == "true"
    rep("INFO", f"draft: {'true -> build with --buildDrafts' if draft else 'false'}; effective slug: {effective}")
    return out, unq(top.get("title"))


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(sys.argv) == 2 else 2
    path = Path(sys.argv[1])
    try:
        out, title = check(path)
    except OSError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    print(f"# front-matter check: {path}")
    if title:
        print(f"title: {title}")
    order = {"BLOCK": 0, "WARN": 1, "INFO": 2}
    for level, msg in sorted(out, key=lambda x: order[x[0]]):
        print(f"{level} {msg}")
    blocks = sum(1 for lvl, _ in out if lvl == "BLOCK")
    warns = sum(1 for lvl, _ in out if lvl == "WARN")
    print(f"{blocks} BLOCK, {warns} WARN")
    return 1 if blocks else 0


if __name__ == "__main__":
    sys.exit(main())

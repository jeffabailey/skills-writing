#!/usr/bin/env python3
"""Check a jeffbaileyblog post's front matter against hugo/AGENTS.md mechanics.

Usage:
    fmcheck.py path/to/content/blog/<section>/<bundle>/index.md

Regex-based (no PyYAML needed). Prints one line per check: PASS / FAIL / WARN.
WARN covers things that are legitimate on legacy posts (slug != folder, missing
keywords) or that need a handoff (cover PNG missing -> generate-cover-image).
Exit 1 if any FAIL, else 0.
"""
import json
import os
import re
import sys


def field(fm, key):
    m = re.search(rf"^{key}:[ \t]*(.*)$", fm, re.MULTILINE)
    return m.group(1).strip() if m else None


def block_list(fm, key):
    m = re.search(rf"^{key}:[ \t]*(\[.*\])?[ \t]*\n((?:[ \t]+-.*\n?)*)", fm, re.MULTILINE)
    if not m:
        return None
    if m.group(1):
        inner = m.group(1).strip("[] ")
        return [x.strip().strip("\"'") for x in inner.split(",") if x.strip()]
    return [l.strip()[1:].strip().strip("\"'") for l in m.group(2).splitlines() if l.strip()]


def find_site_root(p):
    d = os.path.dirname(os.path.abspath(p))
    while d != os.path.dirname(d):
        if os.path.isfile(os.path.join(d, "config.toml")) and os.path.isdir(os.path.join(d, "content")):
            return d
        d = os.path.dirname(d)
    return None


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    p = sys.argv[1]
    s = open(p, encoding="utf-8").read()
    if not s.startswith("---"):
        print("FAIL front matter: file does not start with ---")
        return 1
    fm = s.split("---", 2)[1]
    bundle = os.path.basename(os.path.dirname(os.path.abspath(p)))
    res = []

    def chk(level_if_bad, ok, name, detail=""):
        res.append(("PASS" if ok else level_if_bad, name, detail))

    slug, url = field(fm, "slug"), field(fm, "url")
    img_m = re.search(r"^cover:\s*\n(?:[ \t]+.*\n)*?[ \t]+image:[ \t]*(.*)$", fm, re.MULTILINE)
    img = img_m.group(1).strip() if img_m else None
    q = lambda v: v is not None and v[:1] in ("'", '"')
    chk("FAIL", url is not None and not q(url), "url present and bare", f"url={url}")
    chk("FAIL", slug is None or not q(slug), "slug bare (if present)", f"slug={slug}")
    chk("FAIL", img is not None and not q(img), "cover.image present and bare", f"image={img}")
    eff_slug = (slug or "").strip("\"'") or ((url or "").strip("\"'").rstrip("/").split("/")[-1]) or bundle
    url_tail = (url or "").strip("\"'").rstrip("/").split("/")[-1]
    chk("WARN", eff_slug == bundle == url_tail, "slug == bundle folder == url tail",
        f"slug={eff_slug} folder={bundle} url_tail={url_tail} (ref resolves by folder: {bundle})")
    if img:
        chk("WARN", img.strip("\"'") == f"{eff_slug}.png", "cover.image == <slug>.png", img)
        cover_file = os.path.join(os.path.dirname(os.path.abspath(p)), img.strip("\"'"))
        chk("WARN", os.path.isfile(cover_file), "cover image file exists beside index.md",
            "missing: hand off to generate-cover-image" if not os.path.isfile(cover_file) else cover_file)
    chk("WARN", re.search(r"^[ \t]+alt:", fm, re.MULTILINE) is not None, "cover.alt present")
    d, lm = field(fm, "date"), field(fm, "lastmod")
    ymd = lambda v: bool(v and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v.strip("\"'")))
    chk("FAIL", ymd(d), "date is YYYY-MM-DD", f"date={d}")
    chk("FAIL", lm is None or ymd(lm), "lastmod is YYYY-MM-DD (if present)", f"lastmod={lm}")
    desc = field(fm, "description")
    chk("FAIL", q(desc), "description quoted", (desc or "")[:60])
    if desc and q(desc):
        n = len(desc[1:-1])
        chk("FAIL", n <= 160, "description <= 160 chars", f"{n} chars")
    cats = block_list(fm, "categories")
    chk("FAIL", bool(cats), "categories non-empty", str(cats))
    root = find_site_root(p)
    meta = os.path.join(root, "data", "site-metadata.json") if root else None
    if cats and meta and os.path.isfile(meta):
        known = set(json.load(open(meta)).get("categories", []))
        new = [c for c in cats if c not in known]
        chk("WARN", not new, "categories already in use on the site", f"new: {new}" if new else "")
    kws = block_list(fm, "keywords")
    chk("WARN", bool(kws), "keywords present", f"{len(kws or [])} keywords")
    chk("WARN", field(fm, "type") == "post", "type: post", str(field(fm, "type")))
    chk("WARN", field(fm, "author") == "Jeff Bailey", "author: Jeff Bailey", str(field(fm, "author")))
    print(f"title: {field(fm, 'title')}")
    print(f"draft: {field(fm, 'draft')}")
    for lvl, name, det in res:
        print(f"{lvl} {name}" + (f"  [{det}]" if det else ""))
    return 1 if any(r[0] == "FAIL" for r in res) else 0


if __name__ == "__main__":
    sys.exit(main())

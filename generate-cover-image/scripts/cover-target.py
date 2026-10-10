#!/usr/bin/env python3
"""Resolve where a jeffbaileyblog cover goes, before anything is generated.

Usage:
    cover-target.py <bundle>/index.md | <category>/_index.md [...]

Prints one JSON object per file:

    slug         from front matter `slug:`, else the last segment of `url:`,
                 else the bundle directory name (949 of 1278 posts have no slug:)
    slug_source  "slug", "url", or "dir"
    png          <slug>.png, the default output name beside the index file
    design_name  <slug>, or category-<slug> for a category page
    cover_image  the current cover.image, if any
    keep_existing  when cover.image differs from png: the existing name and the
                 design name that goes with it (older designs are named after
                 the PNG, e.g. 21-laws-of-leadership-book-review)
    warnings     e.g. cover.image differs from <slug>.png, the PNG is missing,
                 or the image path is root-relative
    png_exists   whether png (or cover_image) already exists in the bundle,
                 which makes the run an overwrite
    inline       body `{{< cover-inline >}}` shortcodes (src, alt) to keep in step
    prompts_md   for a category, its prompts.md path and whether it has a
                 "## Cover Image" section (the stored inspiration text)

Read-only: it never writes.
"""
import json
import os
import re
import sys


def front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---", 3)
    return (text[4:end], text[end + 4:]) if end != -1 else ("", text)


def top_key(fm: str, key: str) -> str:
    m = re.search(rf"^{key}:[ \t]*(.*)$", fm, re.MULTILINE)
    return m.group(1).strip().strip("'\"") if m else ""


def cover_key(fm: str, key: str) -> str:
    m = re.search(r"^cover:[ \t]*\n((?:[ \t]+.*\n?|[ \t]*\n)*)", fm, re.MULTILINE)
    if not m:
        return ""
    k = re.search(rf"^[ \t]+{key}:[ \t]*(.*)$", m.group(1), re.MULTILINE)
    return k.group(1).strip().strip("'\"") if k else ""


def resolve(path: str) -> dict:
    text = open(path, encoding="utf-8").read()
    fm, body = front_matter(text)
    bundle = os.path.dirname(os.path.abspath(path))
    dirname = os.path.basename(bundle)
    category = os.path.basename(path) == "_index.md" and os.sep + "categories" + os.sep in bundle + os.sep
    if category:
        slug, source = dirname, "dir"
    elif top_key(fm, "slug"):
        slug, source = top_key(fm, "slug"), "slug"
    elif top_key(fm, "url"):
        slug, source = top_key(fm, "url").rstrip("/").split("/")[-1], "url"
    else:
        slug, source = dirname, "dir"
    png = f"{slug}.png"
    cur = cover_key(fm, "image")
    warnings = []
    if source != "slug" and not category:
        warnings.append(f"no slug: in front matter; slug taken from {source}")
    keep = None
    if cur and os.path.basename(cur) != png:
        name = os.path.basename(cur)
        keep = {"png": name, "design_name": ("category-" if category else "") + os.path.splitext(name)[0]}
        warnings.append(
            f"cover.image is {cur!r}, not {png!r}: ask which name to keep "
            "(keeping the existing name avoids an orphaned PNG and a changed og:image URL; "
            "its design, if any, is named after it: see keep_existing)")
    if cur.startswith("/"):
        warnings.append("cover.image is root-relative; a bundle-relative name is expected")
    existing = [n for n in {png, os.path.basename(cur)} if n and os.path.exists(os.path.join(bundle, n))]
    if cur and not os.path.exists(os.path.join(bundle, os.path.basename(cur))):
        warnings.append(f"cover.image {cur!r} does not exist in the bundle")
    inline = [
        {"src": s, "alt": a}
        for s, a in re.findall(r'\{\{<\s*cover-inline\s+src="([^"]*)"\s+alt="([^"]*)"', body)
    ]
    out = {
        "file": path, "kind": "category" if category else "article",
        "title": top_key(fm, "title"), "slug": slug, "slug_source": source, "png": png,
        "design_name": f"category-{slug}" if category else slug,
        "cover_image": cur, "cover_alt": cover_key(fm, "alt"),
        "png_exists": existing, "inline": inline, "warnings": warnings,
    }
    if keep:
        out["keep_existing"] = keep
    pm = os.path.join(bundle, "prompts.md")
    if category or os.path.exists(pm):
        has = os.path.exists(pm) and "## Cover Image" in open(pm, encoding="utf-8").read()
        out["prompts_md"] = {"path": pm, "exists": os.path.exists(pm), "has_cover_image": has}
    return out


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        print(json.dumps(resolve(p), ensure_ascii=False))


if __name__ == "__main__":
    main()

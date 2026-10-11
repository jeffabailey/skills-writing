#!/usr/bin/env python3
"""Find and check internal link targets for a jeffbaileyblog draft.

`{{< ref "name" >}}` resolves by the bundle's folder name (content path), not by the
front matter `slug:`, and a ref to a draft breaks the production build (drafts are not
rendered because buildDrafts=false). `hugo list all` is the source of truth for which
pages are published, so both subcommands read it.

Usage (run from anywhere; HUGO_DIR is the site root that holds config.toml):
  blog_links.py find  HUGO_DIR TERM [TERM ...]   # published posts whose title/path match all terms
  blog_links.py check HUGO_DIR path/to/index.md  # every ref in the file must be a published page

`check` exits 1 when a ref is missing, points at a draft or future-dated page, or is ambiguous.
"""
import csv
import datetime as dt
import io
import os
import re
import shutil
import subprocess
import sys


def load_pages(hugo_dir):
    if not shutil.which("hugo"):
        sys.exit("tool missing: hugo (install: brew install hugo)")
    out = subprocess.run(["hugo", "list", "all"], cwd=hugo_dir, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"check failed: `hugo list all` exited {out.returncode}\n{out.stderr[-2000:]}")
    now = dt.datetime.now(dt.timezone.utc)
    pages = []
    for row in csv.DictReader(io.StringIO(out.stdout)):
        if row.get("kind") != "page":
            continue
        path = row["path"]
        folder = os.path.basename(os.path.dirname(path)) if path.endswith("index.md") else os.path.splitext(os.path.basename(path))[0]
        try:
            pub = dt.datetime.fromisoformat(row["publishDate"].replace("Z", "+00:00"))
        except ValueError:
            pub = None
        future = bool(pub and pub > now)
        row.update(folder=folder, published=row["draft"] == "false" and not future, future=future)
        pages.append(row)
    return pages


def cmd_find(hugo_dir, terms):
    terms = [t.lower() for t in terms]
    hits = [p for p in load_pages(hugo_dir)
            if p["published"] and p["path"].startswith("content/blog/")
            and all(t in (p["title"] + " " + p["path"]).lower() for t in terms)]
    for p in sorted(hits, key=lambda p: p["path"])[:40]:
        print(f'ref "{p["folder"]}"\t{p["title"]}\t{p["path"]}')
    if not hits:
        print("no published post matches all terms; widen the search", file=sys.stderr)


def cmd_check(hugo_dir, md_file):
    text = open(md_file, encoding="utf-8").read()
    refs = re.findall(r'\{\{<\s*(?:ref|relref)\s+"([^"]+)"\s*>\}\}', text)
    if not refs:
        print("no ref/relref shortcodes found")
        return 0
    pages = load_pages(hugo_dir)
    by_folder, by_path = {}, {}
    for p in pages:
        by_folder.setdefault(p["folder"], []).append(p)
        by_path[p["path"].removeprefix("content/")] = p
    bad = 0
    for ref in dict.fromkeys(refs):
        key = ref.strip("/").split("#")[0]
        cands = [by_path[k] for k in (key, key + "/index.md", key + ".md") if k in by_path] or by_folder.get(key.split("/")[-1], [])
        if not cands:
            slug_hits = [p["folder"] for p in pages if p.get("slug") == key]
            hint = f' (a post has slug "{key}"; ref its folder name "{slug_hits[0]}" instead)' if slug_hits else ""
            print(f"MISSING   {ref}{hint}"); bad += 1
        elif len(cands) > 1:
            print(f"AMBIGUOUS {ref}: " + ", ".join(c["path"] for c in cands) + " (use the section path)"); bad += 1
        elif not cands[0]["published"]:
            why = "future-dated" if cands[0]["future"] else "draft: true"
            print(f"UNPUBLISHED {ref} -> {cands[0]['path']} ({why}); breaks `hugo --gc --minify`"); bad += 1
        else:
            print(f"OK        {ref} -> {cands[0]['path']}")
    return 1 if bad else 0


def main(argv):
    if len(argv) < 3 or argv[0] not in ("find", "check"):
        sys.exit(__doc__)
    if argv[0] == "find":
        cmd_find(argv[1], argv[2:])
        return 0
    return cmd_check(argv[1], argv[2])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

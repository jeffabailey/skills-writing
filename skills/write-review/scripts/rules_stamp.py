#!/usr/bin/env python3
"""Stamp a write-review report with the exact rules it was graded against, or check a stamp.

  rules_stamp.py stamp ARTICLE RUBRIC [RUBRIC ...] [--no-blog]
      Print one line per rule file read, for the saved review's header:
        Rubric: references/fundamentals.md @ <blob hash>
        Style: hugo/content/prompts/writing-style.md @ <blob hash>
        SEO: hugo/content/prompts/seo-front-matter.md @ <blob hash>
        Checklist: write-article/references/great-blog-post.md @ <blob hash>
      RUBRIC is a filename in this skill's references/ (fundamentals.md, ...).
      Style/SEO are the blog's live prompts when the article's repo has them
      (path relative to the repo root), else the bundled copies, shown as
      "references/<file> (bundled)". --no-blog omits them (non-blog articles).
      Checklist is the blog-post quality checklist every review scores, read
      from the sibling write-article skill; it is omitted when that skill is
      not installed.

  rules_stamp.py check REVIEW ARTICLE
      Recompute the stamp REVIEW carries and compare. Prints one line per rule:
      "same", "changed", or "missing", and a verdict line. Exit 0 = every rule
      matches; 1 = a rule changed, moved, or is gone; 2 = REVIEW has no stamp.

Hashes are git blob hashes (identical to `git hash-object FILE`), computed here
so they never depend on git being installed or on anyone typing them.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

REFS = Path(__file__).resolve().parent.parent / "references"
CHECKLIST = REFS.parent.parent / "write-article" / "references" / "great-blog-post.md"
LINE = re.compile(r"^\s*(?:[-*]\s*)?\**(Rubric|Style|SEO|Checklist)\**:\s*\**\s*(\S+)(?:\s+\(bundled\))?\s+@\s+([0-9a-f]{40})\b")


def blob_hash(p: Path) -> str:
    data = p.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def repo_root(article: Path) -> Path | None:
    start = article if article.is_dir() else article.parent
    if not start.is_dir():
        return None
    out = subprocess.run(["git", "-C", str(start), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.returncode == 0 else None


def blog_prompt(article: Path, name: str) -> tuple[str, Path]:
    """(label, path) of the prompt write-review reads: live blog copy first, bundled fallback."""
    root = repo_root(article)
    if root:
        for rel in (f"hugo/content/prompts/{name}", f"content/prompts/{name}"):
            if (root / rel).is_file():
                return rel, root / rel
    return f"references/{name} (bundled)", REFS / name


def stamp_lines(article: Path, rubrics: list[str], blog: bool,
                checklist: bool = True) -> list[tuple[str, str, Path]]:
    rows = []
    for r in rubrics:
        name = Path(r).name
        p = REFS / name
        if not p.is_file():
            sys.exit(f"rubric not found in {REFS}: {name}")
        rows.append(("Rubric", f"references/{name}", p))
    if blog:
        rows.append(("Style", *blog_prompt(article, "writing-style.md")))
        rows.append(("SEO", *blog_prompt(article, "seo-front-matter.md")))
    if checklist and CHECKLIST.is_file():
        rows.append(("Checklist", "write-article/references/great-blog-post.md", CHECKLIST))
    return rows


def cmd_stamp(a) -> int:
    for kind, label, p in stamp_lines(Path(a.article).expanduser().resolve(), a.rubric, not a.no_blog):
        print(f"{kind}: {label} @ {blob_hash(p)}")
    return 0


def cmd_check(a) -> int:
    review = Path(a.review).expanduser()
    article = Path(a.article).expanduser().resolve()
    stamped = []
    for line in review.read_text(encoding="utf-8", errors="replace").splitlines()[:60]:
        m = LINE.match(line)
        if m:
            stamped.append(m.groups())
    if not stamped:
        print(f"no rules stamp in {review}: re-check every finding against the current rules")
        return 2
    rubrics = [Path(lbl).name for kind, lbl, _ in stamped if kind == "Rubric"]
    blog = any(kind in ("Style", "SEO") for kind, _, _ in stamped)
    checklist = any(kind == "Checklist" for kind, _, _ in stamped)
    now = {kind + ":" + (lbl if kind == "Rubric" else ""): (lbl, p)
           for kind, lbl, p in stamp_lines(article, rubrics, blog, checklist)}
    bad = 0
    for kind, lbl, old in stamped:
        key = kind + ":" + (lbl if kind == "Rubric" else "")
        cur_lbl, p = now.get(key, (None, None))
        if p is None or not p.is_file():
            print(f"missing  {kind}: {lbl}")
            bad += 1
        elif cur_lbl.split(" ")[0] != lbl:
            print(f"changed  {kind}: {lbl} -> now reads {cur_lbl} @ {blob_hash(p)}")
            bad += 1
        elif blob_hash(p) != old:
            print(f"changed  {kind}: {lbl} @ {old[:10]} -> {blob_hash(p)[:10]}")
            bad += 1
        else:
            print(f"same     {kind}: {lbl}")
    print("verdict: rules unchanged" if not bad else f"verdict: {bad} rule file(s) changed since the review")
    return 0 if not bad else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("stamp")
    s.add_argument("article")
    s.add_argument("rubric", nargs="+")
    s.add_argument("--no-blog", action="store_true")
    s.set_defaults(fn=cmd_stamp)
    c = sub.add_parser("check")
    c.add_argument("review")
    c.add_argument("article")
    c.set_defaults(fn=cmd_check)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())

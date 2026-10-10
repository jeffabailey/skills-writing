#!/usr/bin/env python3
"""Measured content inventory for a Hugo site, for the content-strategy mode.

Usage:
  content_inventory.py <hugo-dir>            # runs `hugo list all` there (read-only)
  content_inventory.py --csv <list-all.csv> [--root <hugo-dir>]  # reuse a saved output
Options:
  --section blog   content section to count (default: blog)
  --months 24      months of publishing history to show (default: 24)
  --root DIR       hugo dir for draft word counts when using --csv

Prints Markdown: published vs draft counts per category (the folder under
content/<section>/), published posts per month, and backlog totals. Every number
it prints can be cited as [Evidence: hugo list all].

Why: `hugo list all` is the source of truth. Counting folders mixes drafts with
published posts (on jeffbaileyblog roughly 3 of 4 bundles are drafts), which
makes any strategy built on folder counts wrong.
"""
import argparse
import collections
import csv
import io
import shutil
import subprocess
import sys
from datetime import date


def load_rows(args):
    if args.csv:
        with open(args.csv, newline="") as f:
            return list(csv.DictReader(f))
    if not shutil.which("hugo"):
        sys.exit("tool missing: hugo (install: brew install hugo)")
    out = subprocess.run(["hugo", "list", "all"], cwd=args.hugo_dir,
                         capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("check failed: `hugo list all` exited %d\n%s" % (out.returncode, out.stderr))
    return list(csv.DictReader(io.StringIO(out.stdout)))


def category(path, section):
    parts = path.split("/")
    # content/<section>/<category>/<bundle>/index.md
    if len(parts) >= 5 and parts[1] == section:
        return parts[2]
    return "(uncategorized)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hugo_dir", nargs="?")
    ap.add_argument("--csv")
    ap.add_argument("--section", default="blog")
    ap.add_argument("--months", type=int, default=24)
    ap.add_argument("--root")
    args = ap.parse_args()
    if not args.hugo_dir and not args.csv:
        ap.error("give a hugo dir or --csv")

    rows = [r for r in load_rows(args)
            if r.get("kind") == "page" and r.get("section") == args.section]
    pub = [r for r in rows if r.get("draft") == "false"]
    drafts = [r for r in rows if r.get("draft") == "true"]

    print("## Content inventory (source: `hugo list all`, section `%s`, run %s)\n"
          % (args.section, date.today().isoformat()))
    print("- Published pages: %d" % len(pub))
    print("- Draft pages: %d (%.0f%% of all pages)\n"
          % (len(drafts), 100.0 * len(drafts) / max(1, len(rows))))

    cats = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        cats[category(r["path"], args.section)][0 if r["draft"] == "false" else 1] += 1
    print("| Category | Published | Drafts |")
    print("|---|---:|---:|")
    for name, (p, d) in sorted(cats.items(), key=lambda kv: (-kv[1][0], kv[0])):
        print("| %s | %d | %d |" % (name, p, d))

    months = collections.Counter(r["date"][:7] for r in pub if r.get("date"))
    recent = sorted(months.items())[-args.months:]
    print("\n| Month | Published |")
    print("|---|---:|")
    for m, n in recent:
        print("| %s | %d |" % (m, n))
    if recent:
        avg = sum(n for _, n in recent) / len(recent)
        print("\n- Average published per month over the last %d months shown: %.1f"
              % (len(recent), avg))
        if len(recent) >= 12:
            last6 = [n for _, n in recent[-7:-1]]
            prev6 = [n for _, n in recent[-13:-7]]
            print("- Last 6 full months avg: %.1f; the 6 before that: %.1f"
                  % (sum(last6) / 6.0, sum(prev6) / 6.0))
        print("- Note: the current month is partial if it is %s." % date.today().strftime("%Y-%m"))

    root = args.root or args.hugo_dir
    if root and drafts:
        import os
        words = []
        for r in drafts:
            fp = os.path.join(root, r["path"])
            try:
                body = open(fp, encoding="utf-8").read()
            except OSError:
                continue
            parts = body.split("---", 2)
            body = parts[2] if body.startswith("---") and len(parts) == 3 else body
            words.append(len(body.split()))
        if words:
            words.sort()
            stub = sum(1 for w in words if w < 150)
            real = sum(1 for w in words if w >= 800)
            print("\n### Draft depth (body words, front matter excluded)\n")
            print("- Stubs under 150 words: %d" % stub)
            print("- 150-799 words: %d" % (len(words) - stub - real))
            print("- 800+ words (near publishable): %d" % real)
            print("- Median draft length: %d words" % words[len(words) // 2])


if __name__ == "__main__":
    main()

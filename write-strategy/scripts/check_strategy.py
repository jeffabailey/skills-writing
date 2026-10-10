#!/usr/bin/env python3
"""Self-check a write-strategy report before handing it over.

Usage: check_strategy.py <report.md> --mode content|competitor|growth

Checks (exit 1 if any FAIL):
  - no unfilled {{placeholders}} and no emdashes
  - required sections for the mode are present
  - every scoring table row: Priority = Impact x Feasibility, scores in 1-5,
    rows sorted by Priority descending
  - a "Sources and Assumptions" section exists, with at least one URL or local
    source when any [Evidence: ...] tag is used
  - evidence tags are present; lines that state a number with no tag are
    listed as WARN for a human look (not every number needs a tag, e.g. dates)
"""
import argparse
import re
import sys

REQUIRED = {
    "content": ["Inventory", "Audience", "Pillars", "Prioritized Actions",
                "Calendar", "Measures", "Sources and Assumptions"],
    "competitor": ["Competitive Landscape", "Opportunity Gaps",
                   "Prioritized Actions", "Key Insights", "Sources and Assumptions"],
    "growth": ["Approach", "Scorecard", "Top Bottlenecks", "Quick Wins",
               "Strategic Initiatives", "Risks", "90-Day Roadmap",
               "Executive Summary", "Sources and Assumptions"],
}
TAG = re.compile(r"\[(Evidence:[^\]]+|Inference|Assumption)(?:[:\s][^\]]*)?\]")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def check_tables(lines, out):
    i = 0
    found = False
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("|"):
            hdr = [c.lower() for c in cells(line)]
            ii = next((k for k, h in enumerate(hdr) if h.startswith("impact")), None)
            fi = next((k for k, h in enumerate(hdr) if h.startswith(("feasib", "ease"))), None)
            pi = next((k for k, h in enumerate(hdr) if "priority" in h or h == "score"), None)
            if None not in (ii, fi, pi):
                found = True
                prev = None
                j = i + 2
                while j < len(lines) and lines[j].lstrip().startswith("|"):
                    c = cells(lines[j])
                    try:
                        a, b, p = (int(re.sub(r"\D", "", c[k]) or -1) for k in (ii, fi, pi))
                    except (IndexError, ValueError):
                        out.append(("FAIL", "unparseable score row: " + lines[j].strip()[:80]))
                        j += 1
                        continue
                    label = c[0][:40]
                    if not (1 <= a <= 5 and 1 <= b <= 5):
                        out.append(("FAIL", "score outside 1-5 in row '%s'" % label))
                    if a * b != p:
                        out.append(("FAIL", "row '%s': %d x %d != %d" % (label, a, b, p)))
                    if prev is not None and p > prev:
                        out.append(("FAIL", "rows not sorted by priority at '%s'" % label))
                    prev = p
                    j += 1
                i = j
                continue
        i += 1
    if not found:
        out.append(("FAIL", "no Impact / Feasibility / Priority table found"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--mode", required=True, choices=sorted(REQUIRED))
    a = ap.parse_args()
    text = open(a.report).read()
    lines = text.splitlines()
    out = []

    if "{{" in text:
        out.append(("FAIL", "unfilled {{placeholder}} present"))
    if "—" in text:
        out.append(("FAIL", "%d emdash(es) present" % text.count("—")))
    heads = [l.lstrip("#").strip().lower() for l in lines if l.startswith("#")]
    for sec in REQUIRED[a.mode]:
        if not any(sec.lower() in h for h in heads):
            out.append(("FAIL", "missing section heading: " + sec))
    check_tables(lines, out)

    tags = TAG.findall(text)
    ev = [t for t in tags if t.startswith("Evidence")]
    if not tags:
        out.append(("FAIL", "no [Evidence: ...] / [Inference] / [Assumption] tags"))
    src_idx = next((k for k, l in enumerate(lines)
                    if l.startswith("#") and "sources and assumptions" in l.lower()), None)
    if src_idx is not None and ev:
        tail = "\n".join(lines[src_idx:])
        if not re.search(r"https?://|hugo list all|user input|\.md|\.csv", tail):
            out.append(("FAIL", "Sources and Assumptions lists no URL or local source"))

    untagged = []
    in_src = False
    for n, l in enumerate(lines, 1):
        if l.startswith("## ") or l.startswith("# "):
            in_src = "sources and assumptions" in l.lower()
        if in_src or l.lstrip().startswith("|") or l.startswith("#"):
            continue
        bare = re.sub(r"https?://\S+|\bby 1000\b", "", l)
        if re.search(r"\$\d|\d+(\.\d+)?\s?%|\b\d{2,}[kKmM]?\b", bare) and not TAG.search(l) \
                and not re.search(r"\b(19|20)\d{2}\b|[Ww]eek", l):
            untagged.append(n)

    for level, msg in out:
        print("%s: %s" % (level, msg))
    print("INFO: tags evidence=%d inference=%d assumption=%d"
          % (len(ev), tags.count("Inference"), tags.count("Assumption")))
    if untagged:
        print("WARN: numeric lines without a tag (review): %s" % untagged[:30])
    print("RESULT: %s" % ("FAIL" if any(l == "FAIL" for l, _ in out) else "PASS"))
    sys.exit(1 if any(l == "FAIL" for l, _ in out) else 0)


if __name__ == "__main__":
    main()

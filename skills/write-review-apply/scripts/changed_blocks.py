#!/usr/bin/env python3
"""List what an applied review changed, and check the guards around it.

Usage: changed_blocks.py ORIGINAL RESULT [--json]

ORIGINAL is the article before the fixes (a saved copy, or `git show HEAD:<path>`
written to a temp file); RESULT is the edited index.md.

Splits both bodies into blocks (paragraphs, list groups, headings, fenced code)
and prints only the blocks that changed, with their line in RESULT and the
section they sit in. Use that list for the line-polish pass and to pick the
sections to re-score; everything not listed is byte-identical.

Moved blocks (same text, new place) are reported as moves, not rewrites.
Changed fenced code is listed separately, not failed: a review can ask for a
code change, but each one must trace to a finding you verified.

FAIL (exit 1): url/slug/date/draft changed in front matter, profanity count
dropped, an emdash was added, or a category_footer partial was added.
WARN: a new external URL (needs a source the author supplied), or a new
"we"/"our" in changed prose. Standard library only.
"""
import difflib
import json
import re
import sys

FRONT = re.compile(r"\A(---|\+\+\+)\n(.*?)\n\1\n", re.DOTALL)
PROTECTED = ("url", "slug", "date", "draft")
PROFANITY = ["fuck", "shit", "damn", "hell", "ass", "crap", "bastard", "bitch", "piss"]
URL = re.compile(r"https?://[^\s)>\]\"']+")
WE = re.compile(r"\b(we|our|us|we're|we've|ours)\b", re.IGNORECASE)


def split(text):
    """Return (front_matter, blocks). Each block: dict(text, line, section, code)."""
    m = FRONT.match(text)
    front = m.group(2) if m else ""
    offset = text[: m.end()].count("\n") if m else 0
    lines = (text[m.end():] if m else text).split("\n")
    blocks, cur, start, section, fence = [], [], 0, "(top)", None

    def flush(code=False):
        nonlocal cur
        if cur:
            blocks.append({"text": "\n".join(cur), "line": start + offset + 1,
                           "section": section, "code": code})
        cur = []

    for i, line in enumerate(lines):
        if fence:
            cur.append(line)
            if line.lstrip().startswith(fence):
                flush(code=True)
                fence = None
            continue
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            flush()
            fence, start, cur = stripped[:3], i, [line]
            continue
        if line.strip() == "":
            flush()
            continue
        if re.match(r"#{1,6} ", line):
            flush()
            section = line.lstrip("# ").strip()
            start, cur = i, [line]
            flush()
            continue
        if not cur:
            start = i
        cur.append(line)
    flush(code=bool(fence))
    return front, blocks


def field(front, key):
    m = re.search(rf"^{key}\s*[:=].*$", front, re.MULTILINE)
    return m.group(0) if m else None


def count(word, text):
    return len(re.findall(rf"\b{word}", text.lower()))


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    raw_o, raw_n = (open(p, encoding="utf-8").read() for p in argv[1:3])
    fo, bo = split(raw_o)
    fn, bn = split(raw_n)
    fails, warns, info = [], [], []

    for k in PROTECTED:
        if field(fo, k) != field(fn, k):
            fails.append(f"front matter {k} changed: {field(fo, k)!r} -> {field(fn, k)!r}")
    changed_fm = [k for k in ("title", "description", "keywords", "lastmod")
                  if field(fo, k) != field(fn, k)]
    if changed_fm:
        info.append(f"front matter changed: {', '.join(changed_fm)} (only if the review flagged it)")

    sm = difflib.SequenceMatcher(a=[b["text"] for b in bo], b=[b["text"] for b in bn],
                                 autojunk=False)
    deleted, inserted = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("delete", "replace"):
            deleted += bo[i1:i2]
        if tag in ("insert", "replace"):
            inserted += bn[j1:j2]
    pool = list(deleted)
    moved, changed = [], []
    for b in inserted:
        same = next((d for d in pool if d["text"] == b["text"]), None)
        if same:
            pool.remove(same)
            moved.append(b)
        else:
            changed.append(b)
    for b in changed:  # pair each rewrite with the original block it most resembles
        ratio = lambda d: difflib.SequenceMatcher(a=d["text"], b=b["text"]).ratio()
        best = max((d for d in pool if d["code"] == b["code"]), key=ratio, default=None)
        if best and ratio(best) >= 0.5:
            pool.remove(best)
            b["before"] = best["text"]
    removed = pool

    for w in PROFANITY:
        a, b = count(w, raw_o), count(w, raw_n)
        if b < a:
            fails.append(f"profanity '{w}' dropped {a} -> {b} (the author's voice; restore it)")
    if raw_n.count("—") > raw_o.count("—"):
        fails.append(f"emdash added ({raw_o.count(chr(0x2014))} -> {raw_n.count(chr(0x2014))})")
    if raw_n.count("category_footer") > raw_o.count("category_footer"):
        fails.append("category_footer partial added (the layout already renders it)")
    new_urls = sorted(set(URL.findall(raw_n)) - set(URL.findall(raw_o)))
    if new_urls:
        warns.append(f"new external URLs (each needs a source the author supplied): {new_urls}")
    for b in changed:
        if not b["code"]:
            old_we = sum(len(WE.findall(x["text"])) for x in deleted)
            if len(WE.findall(b["text"])) > old_we:
                warns.append(f"line {b['line']}: new 'we'/'our' in changed prose")
                break

    sections = sorted({b["section"] for b in changed + moved + removed})
    result = {
        "status": "FAIL" if fails else "PASS",
        "fail": fails, "warn": warns, "info": info,
        "changed_prose": [{"line": b["line"], "section": b["section"], "text": b["text"],
                           "before": b.get("before")} for b in changed if not b["code"]],
        "changed_code": [{"line": b["line"], "section": b["section"], "text": b["text"],
                          "before": b.get("before")} for b in changed if b["code"]],
        "moved": [{"line": b["line"], "section": b["section"], "first": b["text"].split("\n")[0]}
                  for b in moved],
        "removed": [{"orig_line": b["line"], "section": b["section"], "text": b["text"]}
                    for b in removed],
        "sections_touched": sections,
        "blocks_unchanged": f"{len(bo) - len(deleted)}/{len(bo)}",
    }
    if "--json" in argv:
        print(json.dumps(result, indent=1))
    else:
        print(f"{result['status']}  {result['blocks_unchanged']} original blocks unchanged; "
              f"sections touched: {sections or 'none'}")
        for f in fails:
            print("  FAIL", f)
        for w in warns:
            print("  WARN", w)
        for i in info:
            print("  INFO", i)
        for key, label in (("changed_prose", "PROSE"), ("changed_code", "CODE")):
            for b in result[key]:
                kind = "rewritten" if b["before"] else "added"
                print(f"  {label} {kind} L{b['line']} [{b['section']}]: {b['text'][:160]!r}")
        for b in result["moved"]:
            print(f"  MOVED L{b['line']} [{b['section']}]: {b['first'][:100]!r}")
        for b in result["removed"]:
            print(f"  REMOVED orig L{b['orig_line']} [{b['section']}]: {b['text'][:100]!r}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

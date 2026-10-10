#!/usr/bin/env python3
"""Scan a jeffbaileyblog Markdown file against the LIVE ban list in writing-style.md.

Usage:
    banscan.py path/to/index.md [--ws path/to/writing-style.md] [--list]

The ban list is extracted fresh on every run, so new bans added to
writing-style.md are picked up without editing this script. Sources:
  * every `* Skip "..."` bullet (all quoted strings on the line)
  * every quoted phrase in bullets under "## Writing Style: Things to NOT Do"
  * every `Do NOT write "..."` line and `Using these words: "..."`
Single-word quoted strings are ignored unless they come from "Using these words"
(they are usually examples like "weight", not bans). Phrases with placeholders
(X/Y, A/B, [doing something]) become patterns reported as REVIEW, not BLOCK,
because contrast framing is allowed when it adds meaning.

Markup checks (outside fenced code and inline code): emdash, <a href>, inline
[text](url) links, bare {{< ref >}} outside a link definition, fences without a
language, Markdown tables, H1 in body, category_footer partial in the body, and
arrow-chain text diagrams (REVIEW).

Exit codes: 0 clean (REVIEW items may print), 1 BLOCK hits, 2 usage/setup error.
"""
import argparse
import os
import re
import sys

QUOTE = r'["“]([^"”]+)["”]'


def norm(s):
    return (s.replace("’", "'").replace("‘", "'")
             .replace("…", "").replace("...", "").lower())


def find_ws(md_path):
    d = os.path.dirname(os.path.abspath(md_path))
    while d != os.path.dirname(d):
        cand = os.path.join(d, "content", "prompts", "writing-style.md")
        if os.path.isfile(cand):
            return cand
        cand = os.path.join(d, "hugo", "content", "prompts", "writing-style.md")
        if os.path.isfile(cand):
            return cand
        d = os.path.dirname(d)
    return None


def extract_bans(ws):
    """Return list of (phrase, kind) where kind is 'literal' or 'pattern'."""
    raw = []
    in_not_do = False
    for line in ws.splitlines():
        if line.startswith("## "):
            in_not_do = line.strip().startswith("## Writing Style: Things to NOT Do")
        s = line.strip()
        if not s.startswith("*"):
            continue
        words_line = "Using these words" in s
        if s.startswith("* Skip") or "Do NOT write" in s or words_line or in_not_do:
            # 'Skip "are real" use "exist"': quotes after "use"/"instead" are the
            # recommended replacement, not a ban.
            s = re.split(r"\b(?:use|instead|say)\b", s, maxsplit=1, flags=re.IGNORECASE)[0] if s.startswith("* Skip") else s
            for q in re.findall(QUOTE, s):
                raw.append((q, words_line))
    bans = {}
    for q, words_line in raw:
        t = norm(q).strip().rstrip(".,;:!").strip()
        if not t:
            continue
        if "[" in t:  # "Quietly [doing something]" -> review the lead word
            t = re.sub(r"\s*\[[^\]]*\]", "", t).strip()
            if t:
                bans[t] = "pattern"
            continue
        toks = t.split()
        if re.search(r"\b[xyab]\b", t) and len(toks) > 1:
            bans[t] = "pattern"
            continue
        if len(toks) == 1 and not words_line:
            continue
        bans.setdefault(t, "literal")
    return bans


def to_regex(t, kind):
    if kind == "pattern" and re.search(r"\b[xyab]\b", t):
        parts = re.split(r"\b[xyab]\b", t)
        return r"\b" + r".{1,40}?".join(re.escape(p) for p in parts) + r"\b"
    words = [re.escape(w) for w in t.split()]
    if words and len(words[-1]) > 3 and words[-1].endswith("s"):
        words[-1] = words[-1][:-1] + "s?"  # nightmare scenarios -> scenario(s)
    pat = r"[\s-]+".join(words)  # load bearing == load-bearing
    end = r"\b" if t[-1].isalnum() else ""
    return r"\b" + pat + end


def body_lines(text):
    """Yield (lineno, line_without_inline_code, in_front_matter) for prose lines."""
    lines = text.splitlines()
    fm_end = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_end = i + 1
                break
    fence = None
    out = []
    for i, line in enumerate(lines, 1):
        if i <= fm_end:
            out.append((i, line, True, False))
            continue
        s = line.strip()
        m = re.match(r"^(```+|~~~+)(.*)$", s)
        if m:
            if fence is None:
                fence = m.group(1)
                out.append((i, line, False, "OPEN:" + m.group(2).strip()))
            elif s.startswith(fence):
                fence = None
            continue
        if fence is not None:
            continue
        out.append((i, re.sub(r"`[^`]*`", "``", line), False, False))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--ws", help="path to writing-style.md (auto-found from the file)")
    ap.add_argument("--list", action="store_true", help="print the extracted ban list")
    a = ap.parse_args()
    ws_path = a.ws or find_ws(a.file)
    if not ws_path or not os.path.isfile(ws_path):
        print("ERROR: writing-style.md not found; pass --ws", file=sys.stderr)
        return 2
    bans = extract_bans(open(ws_path, encoding="utf-8").read())
    if a.list:
        for t, k in sorted(bans.items()):
            print(f"{k:8} {t}")
    text = open(a.file, encoding="utf-8").read()
    hits = []  # (level, rule, lineno, excerpt)
    regs = [(t, k, re.compile(to_regex(t, k), re.IGNORECASE)) for t, k in bans.items()]
    for n, line, in_fm, fence in body_lines(text):
        if fence:
            if fence == "OPEN:":
                hits.append(("BLOCK", "FENCE_NO_LANG", n, line.strip()))
            continue
        ex = line.strip()[:110]
        if "—" in line:
            hits.append(("BLOCK", "EMDASH", n, ex))
        if in_fm:
            continue
        nl = norm(line)
        for t, k, rx in regs:
            if rx.search(nl):
                hits.append(("BLOCK" if k == "literal" else "REVIEW", f'BAN "{t}"', n, ex))
        if re.search(r"<a\s+href", line, re.IGNORECASE):
            hits.append(("BLOCK", "HTML_LINK", n, ex))
        if re.search(r"\]\((?:https?:|/|\{\{|mailto:)", line):
            hits.append(("BLOCK", "INLINE_LINK", n, ex))
        if re.search(r"\{\{<\s*ref\b", line) and not re.match(r"^\s*\[[^\]]+\]:\s*\{\{<\s*ref\b", line):
            hits.append(("BLOCK", "BARE_OR_INLINE_REF", n, ex))
        if re.match(r"^\s*\|.*\|\s*$", line) and re.search(r"\|\s*:?-{3,}", line):
            hits.append(("BLOCK", "MARKDOWN_TABLE (use cards shortcode)", n, ex))
        if re.match(r"^# ", line):
            hits.append(("BLOCK", "H1_IN_BODY", n, ex))
        if "category_footer" in line:
            hits.append(("BLOCK", "CATEGORY_FOOTER_IN_BODY (single.html renders it)", n, ex))
        if line.count("→") >= 2 or line.count("->") >= 2:
            hits.append(("REVIEW", "ARROW_DIAGRAM (use Mermaid)", n, ex))
    print(f"writing-style: {ws_path}")
    print(f"ban phrases extracted: {len(bans)}")
    for lvl, rule, n, ex in hits:
        print(f"{lvl} L{n} {rule}: {ex}")
    blocks = sum(1 for h in hits if h[0] == "BLOCK")
    reviews = len(hits) - blocks
    print("CLEAN" if not hits else f"{blocks} BLOCK, {reviews} REVIEW")
    return 1 if blocks else 0


if __name__ == "__main__":
    sys.exit(main())

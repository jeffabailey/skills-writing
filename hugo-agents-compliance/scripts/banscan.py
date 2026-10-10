#!/usr/bin/env python3
"""Scan a jeffbaileyblog Markdown file against the LIVE ban list in writing-style.md.

Shared by hugo-agents-compliance (authoring) and write-validate-article (the
read-only gate, which calls it by sibling path). Keep one copy.

Usage:
    banscan.py path/to/index.md [--ws|--style path/to/writing-style.md] [--list]

The ban list is extracted fresh on every run, so new bans added to
writing-style.md are picked up without editing this script. Sources:
  * every `* Skip "..."` bullet (the banned phrase, not the replacement after
    "use"/"instead"/"say")
  * every quoted phrase in bullets under "## Writing Style: Things to NOT Do"
    (quoted labels after "for"/"e.g." are skipped: they are examples)
  * every `Do NOT write "..."` line and `Using these words: "..."`
Single-word quotes count only from "Using these words" (elsewhere they are
examples such as "I" or "weight"). Phrases with placeholders (X/Y, A/B,
[doing something]), every example under the contrast-framing heading, and the built-in contrast templates ("It's not X, it's Y",
"This isn't A. It's B.", "Not X. Y.") are REVIEW, not BLOCK: writing-style.md
allows contrast when it adds meaning. Apostrophes are optional, space and
hyphen are interchangeable, and a trailing plural "s" is optional.

Markup checks (outside fenced code and inline code): emdash, <a href>, inline
[text](url) links (images excepted), bare {{< ref >}} outside a link
definition, fences without a language, Markdown tables, H1 in body,
category_footer partial in the body, and arrow-chain text diagrams (REVIEW).
Front matter: emdash anywhere; ban phrases in title/description only.

Output: one line per hit, `BLOCK|REVIEW file:line:col RULE -> "match" [writing-style.md:N]`,
then `CLEAN` or `<n> BLOCK, <n> REVIEW`.
Exit codes: 0 no BLOCK (REVIEW items may print), 1 BLOCK hits, 2 usage/setup error.
"""
import argparse
import os
import re
import sys

QUOTE = re.compile(r'["“]([^"”]{1,80})["”]')
APOS = "['’]"


def norm(s):
    return s.replace("’", "'").replace("‘", "'").replace("…", "").replace("...", "").lower()


def find_ws(md_path):
    d = os.path.dirname(os.path.abspath(md_path))
    while d != os.path.dirname(d):
        for cand in (os.path.join(d, "content", "prompts", "writing-style.md"),
                     os.path.join(d, "hugo", "content", "prompts", "writing-style.md")):
            if os.path.isfile(cand):
                return cand
        d = os.path.dirname(d)
    return None


def extract_bans(ws):
    """Return {phrase: (kind, source_line)}; kind is 'literal' or 'pattern'."""
    raw = []
    in_not_do = in_contrast = False
    for ln, line in enumerate(ws.splitlines(), 1):
        if line.startswith("## "):
            in_not_do = line.strip().lower().startswith("## writing style: things to not do")
        if line.startswith("#"):
            in_contrast = line.startswith("### ") and "contrast framing" in line.lower()
        s = line.strip()
        if not s.startswith("*"):
            continue
        words_line = "using these words" in s.lower()
        skip_line = bool(re.match(r"^\*\s+Skip\b", s))
        if not (skip_line or "Do NOT write" in s or words_line or in_not_do):
            continue
        if skip_line:  # 'Skip "are real" use "exist"': quotes after use/instead/say are replacements
            s = re.split(r"\b(?:use|instead|say)\b", s, maxsplit=1, flags=re.IGNORECASE)[0]
        for m in QUOTE.finditer(s):
            before = s[: m.start()].lower().rstrip()
            if in_not_do and not skip_line and not words_line and (
                    re.search(r"\b(for|e\.g\.)\s*\(?$", before) or "e.g." in before):
                continue  # a quoted label or example ("weight", "e.g. ..."), not a ban
            raw.append((m.group(1), words_line, ln, in_contrast))
    bans = {}
    for q, words_line, ln, contrast in raw:
        t = norm(q).strip().rstrip(".,;:!").strip()
        if not t:
            continue
        if "[" in t:  # "Quietly [doing something]" -> review the lead word
            t = re.sub(r"\s*\[[^\]]*\]", "", t).strip()
            if t:
                bans.setdefault(t, ("pattern", ln))
            continue
        toks = t.split()
        if contrast or (re.search(r"\b[xyab]\b", t) and len(toks) > 1):
            bans.setdefault(t, ("pattern", ln))
            continue
        if len(toks) == 1 and not words_line:
            continue
        bans.setdefault(t, ("literal", ln))
    return bans


def word_rx(text):
    """Escape text; apostrophes optional, space/hyphen interchangeable."""
    out = []
    for ch in text:
        if ch == "'":
            out.append(APOS + "?")
        elif ch in " -":
            out.append(r"[\s-]+")
        else:
            out.append(re.escape(ch))
    return re.sub(r"(\[\\s-\]\+)+", r"[\\s-]+", "".join(out))


def to_regex(t, kind):
    if kind == "pattern" and re.search(r"\b[xyab]\b", t):
        parts = re.split(r"\b[xyab]\b", t)
        return r"\b" + r".{1,40}?".join(word_rx(p) for p in parts)
    words = t.split()
    if words and len(words[-1]) > 3 and words[-1].endswith("s"):
        words[-1] = words[-1][:-1]
        body = word_rx(" ".join(words)) + "s?"  # nightmare scenarios -> scenario(s)
    else:
        body = word_rx(t)
    start = r"\b" if t[0].isalnum() else ""
    end = r"\b" if t[-1].isalnum() else ""
    return start + body + end


CONTRAST = [
    (rf"\b(it|that|this){APOS}?s not [^.,;:!?\n]{{1,60}}[,;]\s*(it|that|this){APOS}?s\b",
     "contrast framing: it's not X, it's Y", re.IGNORECASE),
    (rf"\b(isn{APOS}?t|is not|aren{APOS}?t|are not) (just )?[^.!?\n]{{1,60}}\.\s+(it|this|that|they){APOS}?(s|re)\b",
     "contrast framing: this isn't A. It's B.", re.IGNORECASE),
    (r"(^|[.!?]\s+)Not \w+\.\s+[A-Z]\w+\.", "contrast framing: Not X. Y.", 0),
]


def body_lines(text):
    """Return [(lineno, line_without_inline_code, zone, fence_open_info)].

    zone: 'fm' front matter, 'body' prose. fence_open_info is the info string of
    an opening fence line (None otherwise); fenced content is dropped.
    """
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
            out.append((i, line, "fm", None))
            continue
        s = line.strip()
        m = re.match(r"^(`{3,}|~{3,})(.*)$", s)
        if m:
            if fence is None:
                fence = m.group(1)
                out.append((i, line, "body", m.group(2).strip()))
            elif s.startswith(fence) and not s[len(fence):].strip():
                fence = None
            continue
        if fence is not None:
            continue
        out.append((i, re.sub(r"`[^`]*`", lambda mm: " " * len(mm.group(0)), line), "body", None))
    return out


def scan(text, bans):
    hits = []  # (level, lineno, col, rule, match, src)
    regs = [(t, k, src, re.compile(to_regex(t, k), re.IGNORECASE)) for t, (k, src) in bans.items()]
    contrast = [(re.compile(rx, fl), label) for rx, label, fl in CONTRAST]
    for n, line, zone, fence_info in body_lines(text):
        if fence_info is not None:
            if fence_info == "":
                hits.append(("BLOCK", n, 1, "FENCE_NO_LANG", line.strip(), None))
            continue
        for mm in re.finditer("—", line):
            hits.append(("BLOCK", n, mm.start() + 1, "EMDASH", "—", None))
        if zone == "fm" and not re.match(r"^\s*(title|description)\s*:", line):
            continue
        is_def = bool(re.match(r"^\s*\[[^\]]+\]:\s", line))
        if not is_def:
            spans = []  # pattern-hit spans, so a built-in template does not repeat them
            for t, k, src, rx in regs:
                for mm in rx.finditer(line):
                    if k == "pattern":
                        spans.append(mm.span())
                    hits.append(("BLOCK" if k == "literal" else "REVIEW", n, mm.start() + 1,
                                 f'BAN "{t}"', mm.group(0).strip(), src))
            for rx, label in contrast:
                for mm in rx.finditer(line):
                    if not any(a < mm.end() and mm.start() < b for a, b in spans):
                        hits.append(("REVIEW", n, mm.start() + 1, label, mm.group(0).strip(), None))
        if zone == "fm":
            continue
        for mm in re.finditer(r"<a\s+href", line, re.IGNORECASE):
            hits.append(("BLOCK", n, mm.start() + 1, "HTML_LINK", mm.group(0), None))
        if not is_def:
            for mm in re.finditer(r"(?<!!)\[[^\]]*\]\((?!\s*\))[^)]*\)", line):  # images excepted
                hits.append(("BLOCK", n, mm.start() + 1, "INLINE_LINK (use reference-style)", mm.group(0)[:80], None))
            inline_ref = re.search(r"\]\(\s*\{\{<\s*ref\b", line)
            if re.search(r"\{\{<\s*ref\b", line) and not inline_ref:
                hits.append(("BLOCK", n, line.find("{{") + 1, "BARE_REF (use [text][label] + a definition)", "{{< ref", None))
        if re.match(r"^\s*\|.*\|\s*$", line) and re.search(r"\|\s*:?-{3,}", line):
            hits.append(("BLOCK", n, 1, "MARKDOWN_TABLE (use cards shortcode)", line.strip()[:80], None))
        if re.match(r"^# ", line):
            hits.append(("BLOCK", n, 1, "H1_IN_BODY", line.strip()[:80], None))
        if "category_footer" in line:
            hits.append(("BLOCK", n, line.find("category_footer") + 1,
                         "CATEGORY_FOOTER_IN_BODY (single.html renders it)", "category_footer", None))
        if line.count("→") >= 2 or line.count("->") >= 2:
            hits.append(("REVIEW", n, 1, "ARROW_DIAGRAM (use Mermaid)", line.strip()[:80], None))
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("file")
    ap.add_argument("--ws", "--style", dest="ws", help="path to writing-style.md (auto-found from the file)")
    ap.add_argument("--list", action="store_true", help="print the extracted ban list and exit")
    a = ap.parse_args()
    if not os.path.isfile(a.file):
        print(f"ERROR: {a.file} not found", file=sys.stderr)
        return 2
    ws_path = a.ws or find_ws(a.file)
    if not ws_path or not os.path.isfile(ws_path):
        print("ERROR: writing-style.md not found; pass --ws", file=sys.stderr)
        return 2
    bans = extract_bans(open(ws_path, encoding="utf-8").read())
    if a.list:
        for t, (k, src) in sorted(bans.items()):
            print(f"{'BLOCK' if k == 'literal' else 'REVIEW':6} {t}  (writing-style.md:{src})")
        for _, label, _ in CONTRAST:
            print(f"REVIEW {label}  (built-in template)")
        return 0
    hits = scan(open(a.file, encoding="utf-8").read(), bans)
    name = os.path.basename(a.file)
    print(f"# ban scan: {a.file}")
    print(f"writing-style: {ws_path}  ({len(bans)} live phrases + {len(CONTRAST)} contrast templates)")
    for lvl, n, col, rule, match, src in sorted(hits, key=lambda h: (h[1], h[2])):
        where = f"  [writing-style.md:{src}]" if src else ""
        print(f'{lvl} {name}:{n}:{col} {rule} -> "{match}"{where}')
    blocks = sum(1 for h in hits if h[0] == "BLOCK")
    print("CLEAN" if not hits else f"{blocks} BLOCK, {len(hits) - blocks} REVIEW")
    return 1 if blocks else 0


if __name__ == "__main__":
    sys.exit(main())

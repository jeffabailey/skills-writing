#!/usr/bin/env python3
"""Check that an edit of a Markdown/text file changed only prose.

Usage: check_edit.py ORIGINAL EDITED [--json] [--allow-tables] [--section "Heading" ...]

--section (repeatable) names the headings the edit was limited to. Text
outside those sections must be byte-identical (FAIL otherwise), and the
word count and cut % are reported for the named sections only.

FAIL (exit 1) when a frozen part changed: front matter, fenced code blocks,
inline code, link/image URLs, Hugo shortcodes, HTML comments, table rows
(unless --allow-tables, for when the user asked to edit table prose),
numbers, or a drop in profanity count (the author's voice).
WARN (exit 0) when a capitalized name or quoted phrase disappeared, or a
stock AI word appears more often than before. Review warnings by hand.
Always prints prose word counts so you can see how far the cut went.
Standard library only.
"""
import json
import re
import sys
from collections import Counter

FENCE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.MULTILINE | re.DOTALL)
FRONT = re.compile(r"\A(---|\+\+\+)\n.*?\n\1\n", re.DOTALL)
SHORTCODE = re.compile(r"\{\{[<%].*?[%>]\}\}", re.DOTALL)
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
INLINE = re.compile(r"`[^`\n]+`")
MDLINK = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
REFDEF = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
BARE = re.compile(r"(?<![(<\[\"'])\bhttps?://[^\s)>\]\"']+")
NUMBER = re.compile(r"[$€£]?\d+(?:[.,]\d+)*(?:%|[kKMB]\b)?")
NAME = re.compile(r"(?<=[a-z,;:] )[A-Z][\w.-]*[A-Za-z0-9]")
QUOTED = re.compile(r"\"([^\"\n]{3,80})\"|“([^”\n]{3,80})”")
PROFANITY = ["fuck", "shit", "damn", "hell", "ass", "crap", "bastard", "bitch", "piss"]
AI_WORDS = ["pivotal", "crucial", "vital", "testament", "seamless", "robust",
            "leverage", "delve", "foster", "realm", "tapestry", "multifaceted",
            "groundbreaking", "cutting-edge", "showcase", "underscore", "landscape"]


def parts(text):
    front = FRONT.match(text)
    body = text[front.end():] if front else text
    fences = [m.group(0) for m in FENCE.finditer(body)]
    rest = FENCE.sub("", body)
    shortcodes = SHORTCODE.findall(rest)
    comments = COMMENT.findall(rest)
    rest = COMMENT.sub("", SHORTCODE.sub("", rest))
    inline = INLINE.findall(rest)
    table = [l.strip() for l in rest.splitlines() if l.lstrip().startswith("|")]
    urls = MDLINK.findall(rest) + REFDEF.findall(rest) + BARE.findall(rest)
    prose = INLINE.sub(" ", "\n".join(l for l in rest.splitlines()
                                      if not l.lstrip().startswith("|")))
    prose_text = MDLINK.sub("]", prose)
    return {
        "front_matter": front.group(0) if front else "",
        "fenced_code": fences,
        "shortcodes": shortcodes,
        "html_comments": comments,
        "inline_code": Counter(inline),
        "table_rows": table,
        "urls": Counter(urls),
        "numbers": Counter(n.strip() for n in NUMBER.findall(prose_text)),
        "names": set(NAME.findall(prose_text)),
        "quoted": {a or b for a, b in QUOTED.findall(prose_text)},
        "prose_words": len(re.findall(r"\w[\w'’-]*", prose_text)),
        "lower": text.lower(),
    }


HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def split_sections(text, names):
    """Return (inside, outside) text for the named headings (case-insensitive)."""
    want = {x.strip().lower() for x in names}
    inside, outside, level, fence = [], [], None, False
    for line in text.splitlines(keepends=True):
        if line.startswith(("```", "~~~")):
            fence = not fence
        m = None if fence else HEADING.match(line.rstrip("\n"))
        if m:
            depth, title = len(m.group(1)), m.group(2).strip().lower()
            if level is not None and depth <= level:
                level = None
            if level is None and title in want:
                level = depth
        (inside if level is not None else outside).append(line)
    return "".join(inside), "".join(outside)


def option_values(argv, flag):
    return [argv[i + 1] for i, a in enumerate(argv[:-1]) if a == flag]


def count(word, lower):
    return len(re.findall(r"\b" + re.escape(word) if word in ("hell", "ass", "crap") else re.escape(word), lower))


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    raw_o, raw_n = (open(p, encoding="utf-8").read() for p in argv[1:3])
    o, n = parts(raw_o), parts(raw_n)
    fails, warns = [], []
    sections = option_values(argv, "--section")
    if sections:
        in_o, out_o = split_sections(raw_o, sections)
        in_n, out_n = split_sections(raw_n, sections)
        if not in_o:
            fails.append(f"no heading matched {sections}")
        if out_o != out_n:
            fails.append("text outside the named sections changed (must be byte-identical)")
        o["prose_words"] = parts(in_o)["prose_words"]
        n["prose_words"] = parts(in_n)["prose_words"]

    for key in ("front_matter", "fenced_code", "shortcodes", "html_comments", "table_rows"):
        if o[key] != n[key]:
            msg = f"{key} changed (must be byte-identical and in order)"
            if key == "table_rows" and "--allow-tables" in argv:
                warns.append(msg + "; allowed by --allow-tables, so check names, values, and quoted triggers by hand")
            else:
                fails.append(msg)
    for key in ("inline_code", "urls", "numbers"):
        lost = o[key] - n[key]
        if lost:
            fails.append(f"{key} lost: {sorted(lost.elements())[:20]}")
    for w in PROFANITY:
        a, b = count(w, o["lower"]), count(w, n["lower"])
        if b < a:
            fails.append(f"profanity '{w}' dropped {a} -> {b} (voice; restore unless the user asked)")
    lost_names = sorted(o["names"] - n["names"])
    if lost_names:
        warns.append(f"capitalized words gone (check names/products survive): {lost_names[:30]}")
    lost_q = sorted(o["quoted"] - n["quoted"])
    if lost_q:
        warns.append(f"quoted phrases gone (trigger phrases/quotes are data): {lost_q[:15]}")
    added_ai = [w for w in AI_WORDS if count(w, n["lower"]) > count(w, o["lower"])]
    if added_ai:
        warns.append(f"stock AI words added: {added_ai}")

    wo, wn = o["prose_words"], n["prose_words"]
    cut = round(100 * (1 - wn / wo), 1) if wo else 0.0
    result = {"status": "FAIL" if fails else "PASS", "fail": fails, "warn": warns,
              "prose_words": {"before": wo, "after": wn, "cut_pct": cut}}
    if "--json" in argv:
        print(json.dumps(result, indent=1))
    else:
        scope = f" in {len(sections)} section(s)" if sections else ""
        print(f"{result['status']}  prose words{scope} {wo} -> {wn} ({cut}% cut)")
        for f in fails:
            print("  FAIL", f)
        for w in warns:
            print("  WARN", w)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

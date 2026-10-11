#!/usr/bin/env python3
"""Check reader-facing marketing copy before delivery.

Usage:
  check_copy.py COPY.md [--source README.md ...] [--limit Body=120w] [--limit Ad headline=30c]

Only the paste-ready part is checked: the text before the first heading that
starts the needs list or appendix ("Part B", "Needs from you", "Strategy",
"Length check", "Appendix"). Reports:
  - emdashes
  - persuasion-law names ("48 Laws", "Law 4", "Laws of Power")
  - marketing buzzwords (ai-sanitize prose.md category 2)
  - scarcity or urgency phrases
  - quoted testimonials (blockquotes or "..." followed by an attribution)
  - numbers that do not appear in any --source file (skips [NEEDS FACT] markers)
  - word and character counts per labeled part (**Label:** or a heading),
    checked against --limit LABEL=N[w|c]
Exit 0 when clean, 1 when anything is flagged, 2 on usage errors.
"""
import argparse
import re
import sys

STOP = re.compile(r"^#{1,6}\s*(part\s*b|part\s*c|needs from you|strategy|length check|appendix|editor)", re.IGNORECASE | re.MULTILINE)
LAW = re.compile(r"48 laws|laws of power|\blaw\s*#?\d+\b", re.IGNORECASE)
BUZZ = re.compile(r"elevat|seamless|next.gen|supercharg|unleash|unlock|empower|harness|revolutioni|robust|"
                  r"cutting.edge|world.class|effortless|blazing|game.changer", re.IGNORECASE)
SCARCITY = re.compile(r"limited (time|spots?|seats?|offer|availability)|only \d+ (left|spots?|seats?)|today only|"
                      r"don.t miss|hurry|before it.s gone|act now|last chance|price (goes|will go) up|"
                      r"while (supplies|spots) last|ends (soon|tonight)", re.IGNORECASE)
TESTIMONIAL = re.compile(r'^>\s*\S|"[^"]{15,}"\s*(?:[-,]|—)\s*[A-Z]', re.MULTILINE)
NEEDS = re.compile(r"\[NEEDS FACT:[^\]]*\]")
NUM = re.compile(r"(?<![\w#/.-])\d+(?:[.,]\d+)*%?")
LABEL = re.compile(r"^(?:\*\*([^*]+?):\*\*[ \t]*|#{1,6}\s+(.+?)\s*$)", re.MULTILINE)


def parts(text):
    """Split copy into (label, body) by **Label:** prefixes or headings."""
    marks = list(LABEL.finditer(text))
    if not marks:
        return [("copy", text)]
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        label = (m.group(1) or m.group(2)).strip()
        body = text[m.end():end]
        first = body.split("\n", 1)[0]
        if m.group(1) and first.strip():
            body = first  # "**Button:** Install it" is a one-line part
        out.append((label, body))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("copy")
    ap.add_argument("--source", action="append", default=[], help="fact source file (repeatable)")
    ap.add_argument("--limit", action="append", default=[], help="LABEL=N followed by w (words) or c (chars)")
    a = ap.parse_args()

    try:
        full = open(a.copy, encoding="utf-8").read()
        sources = "\n".join(open(s, encoding="utf-8").read() for s in a.source)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    m = STOP.search(full)
    copy = full[: m.start()] if m else full
    clean = NEEDS.sub("", copy)
    flags = []

    def report(name, hits):
        hits = sorted(set(hits), key=str)
        print(f"{name}: {len(hits)}" + (f"  {hits}" if hits else ""))
        if hits:
            flags.append(name)

    dashes = clean.count("—")
    print(f"emdashes: {dashes}")
    if dashes:
        flags.append("emdashes")
    report("law names", LAW.findall(clean))
    report("buzzwords", [x.group(0) for x in BUZZ.finditer(clean)])
    report("scarcity", [x.group(0) for x in SCARCITY.finditer(clean)])
    report("testimonial-like quotes", [x.group(0)[:40] for x in TESTIMONIAL.finditer(clean)])
    if a.source:
        report("numbers not in sources", [n for n in NUM.findall(clean) if n.rstrip("%") not in sources])
    else:
        print("numbers not in sources: skipped (no --source given)")
    print(f"[NEEDS FACT] markers: {len(NEEDS.findall(copy))}")

    limits = {}
    for spec in a.limit:
        lm = re.fullmatch(r"(.+)=(\d+)([wc])", spec)
        if not lm:
            print(f"error: bad --limit {spec!r} (want LABEL=120w or LABEL=30c)", file=sys.stderr)
            return 2
        limits[lm.group(1).strip().lower()] = (int(lm.group(2)), lm.group(3))
    print("lengths:")
    for label, body in parts(copy):
        body = body.strip()
        words, chars = len(body.split()), len(body)
        line = f"  {label}: {words} words, {chars} chars"
        lim = limits.pop(label.lower(), None)
        if lim:
            n, unit = lim
            got = words if unit == "w" else chars
            ok = got <= n
            line += f"  (limit {n}{unit}: {'ok' if ok else 'OVER'})"
            if not ok:
                flags.append(f"{label} over limit")
        print(line)
    for label in limits:
        print(f"  {label}: no part with this label found")
        flags.append(f"{label} missing")

    print("RESULT:", "clean" if not flags else "flagged: " + ", ".join(flags))
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())

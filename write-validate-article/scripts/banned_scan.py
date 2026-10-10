#!/usr/bin/env python3
"""Banned-phrase scan for jeffbaileyblog articles.

The ban list is read live from content/prompts/writing-style.md on every run,
so new bans added there are enforced without editing this script:

  * inline  Skip "..."            markers (anywhere in the file)
  * quoted bullets under          ## Writing Style: Things to NOT Do
  * Using these words: "..."      entries
  * contrast-framing templates    ("It's not X, it's Y", "This isn't A. It's B.", "Not chaos. Clarity.")
  * mechanical bans               emdash, <a href>, inline [text](url), bare {{< ref >}} in body

Usage: banned_scan.py ARTICLE.md [--style path/to/writing-style.md]
Exit:  0 = no hits, 1 = hits (each is BLOCKING), 2 = could not run.
"""
import argparse
import re
import sys
from pathlib import Path

APOS = "['’]"  # straight or curly apostrophe


def find_style(article: Path) -> Path | None:
    for d in [article.resolve().parent, *article.resolve().parents]:
        cand = d / "content" / "prompts" / "writing-style.md"
        if cand.is_file():
            return cand
    return None


def phrase_to_regex(phrase: str) -> str | None:
    p = phrase.strip().strip("“”\"").strip()
    p = re.sub(r"\s*\[[^\]]*\]", "", p)          # "Quietly [doing something]" -> "Quietly"
    p = p.rstrip("….").rstrip()              # "And honestly…" -> "And honestly"
    if len(p) < 3:
        return None
    parts = []
    for ch in p:
        if ch in "'’":
            parts.append(APOS + "?")
        elif ch in " -":
            parts.append(r"[\s-]+")
        else:
            parts.append(re.escape(ch))
    rx = "".join(parts)
    start = r"\b" if p[0].isalnum() else ""
    end = r"\b" if p[-1].isalnum() else ""
    if p.lower() == "quietly":
        end = r"\s+\w+"  # "quietly [doing something]"
    return start + rx + end


QUOTED = re.compile(r"[\"“]([^\"”]{2,80})[\"”]")

CONTRAST_RULES = [
    (rf"\b(it|that|this){APOS}?s not [^.,;:!?\n]{{1,60}}[,;]\s*(it|that|this){APOS}?s\b", "contrast framing: it's not X, it's Y"),
    (rf"\b(isn{APOS}?t|is not|aren{APOS}?t|are not) (just )?[^.!?\n]{{1,60}}\.\s+(it|this|that|they){APOS}?(s|re)\b", "contrast framing: this isn't A. It's B."),
    (r"(^|[.!?]\s+)Not \w+\.\s+[A-Z]\w+\.", "contrast framing: Not X. Y."),
]


def build_rules(style_path: Path):
    lines = style_path.read_text(encoding="utf-8").splitlines()
    rules, seen = [], set()

    def add(phrase, cat, ln):
        rx = phrase_to_regex(phrase)
        if rx and rx.lower() not in seen:
            seen.add(rx.lower())
            rules.append((re.compile(rx, re.IGNORECASE), f"{cat}: {phrase.strip()}", ln))

    in_not_do = False
    in_contrast = False
    for i, raw in enumerate(lines, 1):
        s = raw.strip()
        if s.startswith("## "):
            in_not_do = "things to not do" in s.lower()
        if s.startswith("### "):
            in_contrast = "contrast framing" in s.lower()
        if re.match(r"^\*\s+Skip\b", s):
            # only the banned phrase, not the suggested replacement after "use"/"instead"
            head = re.split(r"\b(?:use|instead)\b", s, maxsplit=1)[0]
            for q in QUOTED.findall(head):
                add(q, "Skip", i)
        elif "using these words" in s.lower():
            for q in QUOTED.findall(s):
                add(q, "Using these words", i)
        elif in_not_do and not in_contrast and s.startswith("* "):
            for m in QUOTED.finditer(s):
                before = s[: m.start()].lower()
                if re.search(r"\b(for|e\.g\.)\s*\(?$", before.strip() + " ") or "e.g." in before:
                    continue  # a quoted label or an example template, not a phrase ban
                add(m.group(1), "Things to NOT Do", i)
    for rx, label in CONTRAST_RULES:
        rules.append((re.compile(rx, re.IGNORECASE if "Not X" not in label else 0), label, None))
    return rules


MECHANICAL = [
    (re.compile("—"), "emdash (—)"),
    (re.compile(r"<a\s+href", re.IGNORECASE), "HTML <a href> link"),
    (re.compile(r"\]\((?!\s*\))[^)\s]+[^)]*\)"), "inline link [text](url); use reference-style"),
]
REF_DEF = re.compile(r"^\s*\[[^\]]+\]:\s")
BARE_REF = re.compile(r"\{\{<\s*ref\b")


def scan(article: Path, rules):
    hits = []
    text = article.read_text(encoding="utf-8").splitlines()
    in_fm = bool(text and text[0].strip() == "---")
    fence = None
    for n, line in enumerate(text, 1):
        st = line.strip()
        if in_fm:
            if n > 1 and st == "---":
                in_fm = False
                continue
            if not re.match(r"^(title|description)\s*:", st):
                continue  # only prose fields of front matter are checked
        m = re.match(r"^(```|~~~)", st)
        if m:
            fence = None if fence == m.group(1) else (fence or m.group(1))
            continue
        if fence:
            continue  # code blocks are not prose
        is_def = bool(REF_DEF.match(line))
        for rx, label in MECHANICAL:
            if is_def and "inline link" in label:
                continue
            for mm in rx.finditer(line):
                hits.append((n, mm.start() + 1, label, mm.group(0), None))
        if not is_def and BARE_REF.search(line) and "](" not in line:
            hits.append((n, line.find("{{") + 1, "bare {{< ref >}} in body; use [text][label] + a definition", "{{< ref", None))
        if is_def:
            continue
        for rx, label, src in rules:
            for mm in rx.finditer(line):
                hits.append((n, mm.start() + 1, label, mm.group(0).strip(), src))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("article")
    ap.add_argument("--style")
    ap.add_argument("--list", action="store_true", help="print the extracted ban list and exit")
    a = ap.parse_args()
    article = Path(a.article)
    if not article.is_file():
        print(f"ERROR: {article} not found", file=sys.stderr)
        return 2
    style = Path(a.style) if a.style else find_style(article)
    if not style or not style.is_file():
        print("ERROR: writing-style.md not found; pass --style", file=sys.stderr)
        return 2
    rules = build_rules(style)
    if a.list:
        for _, label, src in rules:
            print(f"{label}" + (f"  (writing-style.md:{src})" if src else ""))
        return 0
    hits = scan(article, rules)
    print(f"# banned-phrase scan: {article}  ({len(rules)} live rules from {style})")
    for n, col, label, match, src in sorted(hits):
        where = f"  [writing-style.md:{src}]" if src else ""
        print(f"BLOCKING {article.name}:{n}:{col}  {label}  -> \"{match}\"{where}")
    print(f"{len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())

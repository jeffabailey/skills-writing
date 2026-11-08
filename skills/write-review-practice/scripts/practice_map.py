#!/usr/bin/env python3
"""Map how a Learn X article and its practice playground line up.

Usage:
    python3 practice_map.py ARTICLE_INDEX_MD [PLAYGROUND_DIR]

PLAYGROUND_DIR defaults to hugo/static/playgrounds/<name>, where <name> comes
from the article's {{< playground "name" >}} shortcode.

Prints a Markdown inventory: the article's outline with anchors, its code
blocks (and which run on the reader's machine), the playground's files, its
exercises, and the mismatches between the two (exercise links to anchors the
article lacks, core sections with no exercise). The inventory is evidence for
the review, not a verdict: a core section with no exercise may be fine.
"""
import json
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^(#{2,4})\s+(.+?)\s*$")
FENCE = re.compile(r"^(\s*)(```+|~~~+)\s*([\w+-]*)\s*(\{[^}]*\})?")
SHORTCODE = re.compile(r'\{\{<\s*playground\s+"([^"]+)"')
EXERCISE = re.compile(r"^(\d+)\.\s+(.*?)(?:\s+[—-]\s+`(.+)`)?\s*$")
EX_FIELD = re.compile(r"^\s+-\s+(\w+):\s*(.*)$")


def slug(text):
    """Approximate Hugo's default (GitHub-style) heading anchor."""
    text = re.sub(r"`|\*\*|\*|_(?=\w)|\[([^\]]*)\]\[[^\]]*\]", r"\1", text)
    text = text.lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def split_front_matter(lines):
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], i + 1
    return [], 0


def parse_article(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    fm, start = split_front_matter(lines)
    meta = {}
    for line in fm:
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            meta[m.group(1)] = m.group(2).strip().strip('"')
    headings, blocks, shortcodes, learn = [], [], [], []
    section, in_fence, fence_mark, in_learn, parent = None, False, "", False, ""
    for n, line in enumerate(lines[start:], start=start + 1):
        if in_fence:
            if line.strip().startswith(fence_mark):
                in_fence = False
            else:
                blocks[-1]["lines"] += 1
            continue
        fm_ = FENCE.match(line)
        if fm_:
            in_fence, fence_mark = True, fm_.group(2)
            attrs = fm_.group(4) or ""
            blocks.append({
                "line": n,
                "lang": fm_.group(3) or "",
                "machine": 'practice="machine"' in attrs,
                "section": section["text"] if section else "",
                "lines": 0,
            })
            continue
        h = HEADING.match(line)
        if h:
            level = len(h.group(1))
            if level == 2:
                parent = h.group(2)
            section = {"level": level, "text": h.group(2), "anchor": slug(h.group(2)), "line": n,
                       "parent": parent if level > 2 else ""}
            headings.append(section)
            in_learn = section["level"] == 2 and "what you" in section["text"].lower()
            continue
        if in_learn and line.lstrip().startswith(("* ", "- ")):
            learn.append(line.strip()[2:])
        for m in SHORTCODE.finditer(line):
            shortcodes.append({"name": m.group(1), "line": n, "section": section["text"] if section else ""})
    return {"meta": meta, "headings": headings, "blocks": blocks, "shortcodes": shortcodes, "learn": learn}


def parse_exercises(path):
    exercises, group = [], ""
    current, field = None, None
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        h = HEADING.match(line)
        if h:
            group, current = h.group(2), None
            continue
        m = EXERCISE.match(line)
        if m:
            current = {"n": int(m.group(1)), "task": m.group(2), "start": m.group(3) or "",
                       "group": group, "line": n, "fields": {}}
            exercises.append(current)
            continue
        f = EX_FIELD.match(line)
        if f and current is not None:
            field = f.group(1)
            current["fields"][field] = f.group(2)
    return exercises


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    article_path = Path(argv[1]).resolve()
    art = parse_article(article_path)
    if len(argv) > 2:
        pg = Path(argv[2]).resolve()
    else:
        hugo = next((p for p in article_path.parents if (p / "static" / "playgrounds").is_dir()), None)
        name = art["shortcodes"][0]["name"] if art["shortcodes"] else None
        pg = (hugo / "static" / "playgrounds" / name) if hugo and name else None

    out = [f"# Practice map: {art['meta'].get('title', article_path.name)}", ""]
    out.append(f"- Article: `{article_path}` (url `{art['meta'].get('url', '?')}`, draft {art['meta'].get('draft', '?')})")
    out.append(f"- Playground: `{pg}`" if pg else "- Playground: none found (no playground shortcode and none given)")
    for sc in art["shortcodes"]:
        out.append(f"- Embedded at line {sc['line']} under \"{sc['section']}\" (`{sc['name']}`)")

    out += ["", "## What You'll Learn (stated outcomes)", ""]
    out += [f"{i}. {item}" for i, item in enumerate(art["learn"], 1)] or ["(none found)"]

    out += ["", "## Article outline", "", "| Line | Heading | Anchor | Code blocks (machine) |", "|---|---|---|---|"]
    for h in art["headings"]:
        own = [b for b in art["blocks"] if b["section"] == h["text"]]
        machine = sum(b["machine"] for b in own)
        indent = "&nbsp;&nbsp;" * (h["level"] - 2)
        out.append(f"| {h['line']} | {indent}{h['text']} | `#{h['anchor']}` | {len(own)} ({machine}) |")

    exercises = []
    if pg and pg.is_dir():
        out += ["", "## Playground files", ""]
        for f in sorted(p for p in pg.rglob("*") if p.is_file() and "engine" not in p.relative_to(pg).parts):
            try:
                count = len(f.read_text(encoding="utf-8").splitlines())
                out.append(f"- `{f.relative_to(pg)}` ({count} lines)")
            except (UnicodeDecodeError, OSError):
                out.append(f"- `{f.relative_to(pg)}` (binary)")
        engine = pg / "engine"
        if engine.is_dir():
            out.append("- `engine/` (program bytes and build recipe; not instructional, skipped)")
        msgs = pg / "messages.json"
        if msgs.is_file():
            try:
                keys = list(json.loads(msgs.read_text(encoding="utf-8")))
                out.append(f"- messages.json keys: {', '.join(keys)}")
            except json.JSONDecodeError as e:
                out.append(f"- messages.json does not parse: {e}")
        ex_file = pg / "practice" / "exercises.md"
        if ex_file.is_file():
            exercises = parse_exercises(ex_file)

    anchors = {h["anchor"] for h in art["headings"]}
    url = art["meta"].get("url", "").rstrip("/")
    if exercises:
        out += ["", "## Exercises (practice/exercises.md)", "",
                "| # | Group | Task | Start | hint | answer | link ok |", "|---|---|---|---|---|---|---|"]
        for e in exercises:
            link = e["fields"].get("link", "")
            if not link:
                ok = "no link"
            else:
                path, _, anchor = link.partition("#")
                ok = "yes" if (path.rstrip("/") == url and anchor in anchors) else f"NO ({link})"
            out.append(f"| {e['n']} | {e['group']} | {e['task']} | `{e['start']}` | "
                       f"{'yes' if 'hint' in e['fields'] else '-'} | {'yes' if 'answer' in e['fields'] else '-'} | {ok} |")
        groups = {e["group"] for e in exercises}
        # The core is the "20% That Does 80%" section; other ### headings are
        # basics, steps, or troubleshooting and rarely carry an exercise.
        h3 = [h for h in art["headings"] if h["level"] == 3 and "20%" in h["parent"]]
        uncovered = [h["text"] for h in h3 if h["text"] not in groups and h["anchor"] not in
                     {e["fields"].get("link", "").partition("#")[2] for e in exercises}]
        out += ["", "## Gaps to check (evidence, not verdicts)", ""]
        out.append("- Core (20%) sections with no exercise: " + (", ".join(f'"{t}"' for t in uncovered) or "none"))
        stray = sorted(groups - {h["text"] for h in art["headings"]})
        out.append("- Exercise groups that match no article heading: " + (", ".join(f'"{g}"' for g in stray) or "none"))
    elif pg:
        out += ["", "## Exercises", "", "No `practice/exercises.md`: the practice is defined elsewhere "
                "(a practice file the program opens, stage scripts or checks in playground.js, or notes). Read playground.js."]

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
"""Set the Hugo cover block in a jeffbaileyblog bundle's front matter.

Writes, unquoted as hugo/AGENTS.md requires:

    cover:
      image: <png>
      alt: <alt>
      caption: ""        (only with --category)

It replaces `image` and `alt` (and `caption` with --category) in an existing
top-level `cover:` block, keeping its other keys such as `relative` or
`hidden`, or appends a new block at the end of the front matter. Every other line is left byte for byte. The alt text is
written bare unless YAML would misread it (a colon-space, a leading special
character, or a value such as "yes"), in which case it is double-quoted. A
replaced block keeps its indentation, and a quoted alt stays quoted.

Usage:
    set-cover-frontmatter.py <index.md|_index.md> <png name> "<alt text>" [--category]
    set-cover-frontmatter.py --batch < lines      # each line: path<TAB>png<TAB>alt[<TAB>category]
"""
import json
import re
import sys


def yaml_scalar(s: str, quote: bool = False) -> str:
    if quote:
        return json.dumps(s, ensure_ascii=False)
    plain = re.fullmatch(r"[A-Za-z0-9][^:#\n]*", s) and ": " not in s and not s.endswith(":")
    if plain and not re.fullmatch(r"(?i)yes|no|true|false|on|off|null|~|[0-9.]+", s):
        return s
    return json.dumps(s, ensure_ascii=False)


def set_cover(path: str, png: str, alt: str, category: bool) -> None:
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        sys.exit(f"{path}: no YAML front matter (expected a leading ---)")
    end = text.find("\n---", 3)
    if end == -1:
        sys.exit(f"{path}: front matter is not closed")
    lines = text[4:end].split("\n")
    ours = {"image", "alt"} | ({"caption"} if category else set())

    def value(key: str, quote_alt: bool) -> str:
        return {"image": png, "alt": yaml_scalar(alt, quote_alt), "caption": '""'}[key]

    out, i, replaced = [], 0, False
    while i < len(lines):
        if re.match(r"cover:\s*$", lines[i]):
            # Replace image/alt (and caption) where they stand, keep every other
            # cover key (relative, hidden, ...), the block's indentation, and a
            # quoted alt's quotes, so YAML stays valid and the diff is minimal.
            out.append(lines[i])
            i += 1
            indent, seen = None, set()
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                key = re.match(r"(\s+)([A-Za-z_]+):\s*(.*)", lines[i])
                if key and indent is None:
                    indent = key.group(1)
                if key and key.group(2) in ours:
                    k = key.group(2)
                    out.append(f"{key.group(1)}{k}: {value(k, key.group(3).startswith(chr(34)))}")
                    seen.add(k)
                else:
                    out.append(lines[i])
                i += 1
            for k in ("image", "alt", "caption"):
                if k in ours and k not in seen:
                    out.append(f"{indent or '  '}{k}: {value(k, False)}")
            replaced = True
            continue
        out.append(lines[i])
        i += 1
    if not replaced:
        out.append("cover:")
        out.extend(f"  {k}: {value(k, False)}" for k in ("image", "alt", "caption") if k in ours)
    open(path, "w", encoding="utf-8").write("---\n" + "\n".join(out) + text[end:])
    print(f"{path}: cover {'replaced' if replaced else 'added'} ({png})")


def main() -> None:
    args = sys.argv[1:]
    if args == ["--batch"]:
        for line in sys.stdin:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            set_cover(parts[0], parts[1], parts[2], len(parts) > 3 and parts[3] == "category")
        return
    category = "--category" in args
    args = [a for a in args if a != "--category"]
    if len(args) != 3:
        sys.exit(__doc__)
    set_cover(*args, category)


if __name__ == "__main__":
    main()

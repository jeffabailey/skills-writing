#!/usr/bin/env python3
"""Read or write the stored cover inspiration text in a bundle's prompts.md.

jeffbaileyblog keeps each category's inspiration text in
content/categories/<slug>/prompts.md under "## Cover Image". Read it before
writing a new text (so the new cover does not repeat the old scene), and write
the new text back after the design is committed (so the file describes the
cover that is actually published).

Usage:
    prompt-store.py get <bundle dir>                  # prints the section body, exit 1 if none
    prompt-store.py set <bundle dir> <inspiration.txt> # replaces (or adds) the section

`set` keeps every other section byte for byte, and creates
"# Prompts\n\n## Cover Image\n\n<text>\n" when the file does not exist.
"""
import os
import re
import sys

HEAD = "## Cover Image"
SECTION = re.compile(r"^## Cover Image[ \t]*\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)


def main() -> None:
    if len(sys.argv) < 3 or sys.argv[1] not in ("get", "set"):
        sys.exit(__doc__)
    path = os.path.join(sys.argv[2], "prompts.md")
    text = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    m = SECTION.search(text)
    if sys.argv[1] == "get":
        if not m or not m.group(1).strip():
            sys.exit(1)
        print(m.group(1).strip())
        return
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    new = open(sys.argv[3], encoding="utf-8").read().strip()
    block = f"{HEAD}\n\n{new}\n"
    if m:
        tail = "\n" if m.end() < len(text) else ""
        text = text[: m.start()] + block + tail + text[m.end():]
    elif text:
        text = text.rstrip("\n") + "\n\n" + block
    else:
        text = "# Prompts\n\n" + block
    open(path, "w", encoding="utf-8").write(text)
    print(f"{path}: {HEAD} {'replaced' if m else 'added'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Extract every fenced code block in a Markdown article so it can be read,
measured, and checked as one program (stdlib only).

Usage:
    python3 extract_code.py <article.md> <out_dir> [--check]
    python3 extract_code.py --find-reviewer

Writes to <out_dir>:
  blocks/NN-<lang>-L<line>.<ext>  one file per block, in article order
  program.<ext>                   all blocks of one language joined in order,
                                  so metrics and duplication checks see the
                                  article's code as a whole
  manifest.json                   per block: index, lang, start/end line
                                  (1-based, the fence lines), kind, file

kind is "code", "output" (text/console/no language, or a shell block whose
lines mostly lack a prompt after the first), or "diagram" (mermaid etc.).
Only "code" blocks are joined into program files.

--check runs a syntax check per code block where a checker is installed
(bash -n, shellcheck, python3 -m py_compile, node --check) and prints one line
per block: OK, FAIL <first error line>, or SKIP <reason>.

When review-maintainability is installed and a program file is in a language
its metrics.py measures, the "Max values" section of metrics.py is printed
after the block table, so no separate metrics call is needed.

--find-reviewer prints the review-maintainability skill directory, or exits 1.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

FENCE_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})\s*(?P<info>[^`]*)$")
EXT = {"bash": "sh", "sh": "sh", "shell": "sh", "zsh": "zsh", "console": "txt",
       "python": "py", "py": "py", "javascript": "js", "js": "js", "typescript": "ts",
       "ts": "ts", "go": "go", "rust": "rs", "ruby": "rb", "yaml": "yaml", "yml": "yaml",
       "json": "json", "toml": "toml", "sql": "sql", "dockerfile": "Dockerfile",
       "hcl": "tf", "terraform": "tf", "lua": "lua", "java": "java", "c": "c",
       "cpp": "cpp", "nu": "nu", "fish": "fish", "makefile": "mk", "html": "html",
       "css": "css"}
OUTPUT_LANGS = {"", "text", "txt", "plain", "plaintext", "output", "console", "log"}
DIAGRAM_LANGS = {"mermaid", "plantuml", "dot", "graphviz", "ascii"}
MEASURED_EXT = {"py", "js", "ts", "go", "rs", "java", "c", "cpp"}  # metrics.py measures functions in these
SHELL_LANGS = {"bash", "sh", "shell", "zsh", "fish", "nu"}
REVIEWER_DIRS = [
    "../review-maintainability",
    "~/.agents/skills/review-maintainability",
    "~/.claude/skills/review-maintainability",
    "~/.cursor/skills/review-maintainability",
    "~/Projects/skills/skills/review-maintainability",
]


def find_reviewer():
    here = Path(__file__).resolve().parent.parent
    for d in REVIEWER_DIRS:
        p = (here / d) if d.startswith("..") else Path(os.path.expanduser(d))
        if (p / "SKILL.md").is_file():
            return p.resolve()
    plugins = Path.home() / ".claude" / "plugins"
    for hit in sorted(plugins.glob("**/review-maintainability/SKILL.md")):
        return hit.parent
    return None


def parse_blocks(lines):
    blocks, i = [], 0
    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        fence, indent = m["fence"], len(m["indent"])
        lang = (m["info"].split() or [""])[0].strip("{}.").lower()
        body, j = [], i + 1
        while j < len(lines):
            close = lines[j].strip()
            if close and close[0] == fence[0] and set(close) == {fence[0]} and len(close) >= len(fence):
                break
            body.append(lines[j][indent:] if lines[j][:indent].strip() == "" else lines[j])
            j += 1
        blocks.append({"lang": lang, "start": i + 1, "end": j + 1, "body": body})
        i = j + 1
    return blocks


def classify(lang, body):
    if lang in DIAGRAM_LANGS:
        return "diagram"
    if lang in OUTPUT_LANGS:
        return "output"
    if lang in SHELL_LANGS:
        rest = [l for l in body[1:] if l.strip()]
        if body and body[0].lstrip().startswith("$ ") and rest:
            prompted = sum(l.lstrip().startswith("$ ") for l in rest)
            if prompted < len(rest) / 2:
                return "output"  # transcript: one command, then its output
    return "code"


def strip_prompts(lang, body):
    if lang not in SHELL_LANGS:
        return body
    return [l.lstrip()[2:] if l.lstrip().startswith("$ ") else l for l in body]


def check(path, lang):
    cmds = []
    if lang in {"bash", "sh", "shell"}:
        cmds = [["bash", "-n", path]]
        if shutil.which("shellcheck"):
            cmds.append(["shellcheck", "-s", "bash", "-S", "warning", path])
    elif lang == "zsh" and shutil.which("zsh"):
        cmds = [["zsh", "-n", path]]
    elif lang in {"python", "py"}:
        cmds = [[sys.executable, "-m", "py_compile", path]]
    elif lang in {"javascript", "js"} and shutil.which("node"):
        cmds = [["node", "--check", path]]
    elif lang == "json":
        cmds = [[sys.executable, "-m", "json.tool", path]]
    if not cmds:
        return "SKIP no checker for " + (lang or "untyped")
    for cmd in cmds:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            err = (r.stderr or r.stdout).strip().splitlines()
            return f"FAIL {cmd[0]}: {err[0] if err else 'exit ' + str(r.returncode)}"
    return "OK"


def main(argv):
    if argv[:1] == ["--find-reviewer"]:
        p = find_reviewer()
        print(p if p else "NOT FOUND: install with `npx skills add jeffabailey/skills`")
        return 0 if p else 1
    if len(argv) < 2:
        print(__doc__)
        return 2
    article, out = Path(argv[0]), Path(argv[1])
    lines = article.read_text(encoding="utf-8").splitlines()
    (out / "blocks").mkdir(parents=True, exist_ok=True)
    manifest, programs = [], {}
    for n, b in enumerate(parse_blocks(lines), 1):
        kind = classify(b["lang"], b["body"])
        ext = EXT.get(b["lang"], "txt")
        name = f"blocks/{n:02d}-{b['lang'] or 'none'}-L{b['start']}.{ext}"
        body = strip_prompts(b["lang"], b["body"]) if kind == "code" else b["body"]
        (out / name).write_text("\n".join(body) + "\n", encoding="utf-8")
        entry = {"index": n, "lang": b["lang"], "start": b["start"], "end": b["end"],
                 "kind": kind, "lines": len(b["body"]), "file": name}
        if kind == "code":
            programs.setdefault(ext, []).append((b, body))
        if "--check" in argv and kind == "code":
            entry["check"] = check(str(out / name), b["lang"])
        manifest.append(entry)
    for ext, parts in programs.items():
        comment = "#" if ext in {"sh", "zsh", "py", "rb", "yaml", "toml", "tf", "mk", "nu", "fish", "Dockerfile"} else "//"
        text = []
        for b, body in parts:
            text.append(f"{comment} --- article lines {b['start']}-{b['end']} ---")
            text.extend(body)
        (out / f"program.{ext}").write_text("\n".join(text) + "\n", encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    for e in manifest:
        status = f"  {e['check']}" if "check" in e else ""
        print(f"{e['index']:>3} L{e['start']}-{e['end']} {e['lang'] or '-':<10} {e['kind']:<7} {e['lines']:>3} lines{status}")
    print(f"PROGRAMS: {', '.join('program.' + x for x in programs) or 'none'}")
    reviewer = find_reviewer()
    print(f"REVIEWER: {reviewer if reviewer else 'NOT FOUND'}")
    measurable = [str(out / f"program.{x}") for x in programs if x in MEASURED_EXT]
    if reviewer and measurable:
        r = subprocess.run([sys.executable, str(reviewer / "scripts" / "metrics.py"), *measurable, "--top", "3"],
                           capture_output=True, text=True)
        text = r.stdout
        start, end = text.find("## Max values"), text.find("## Top")
        print("METRICS (program files; shell and other languages: measure by reading):")
        print(text[start:end].rstrip() if start >= 0 else (r.stderr.strip() or "no output"))
    else:
        print("METRICS: none measurable (measure by reading)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

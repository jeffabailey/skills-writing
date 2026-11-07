#!/usr/bin/env python3
"""Programmatic grader for the write-optimize-code eval cases (stdlib only).

Usage:
    python3 grade.py <case-name> <edited-index.md> [response.md]
    python3 grade.py <iteration-dir>

The first form grades one run and prints each assertion. The second grades a
skill-creator workspace iteration (<iteration-dir>/<case>/<config>/outputs/
{index.md,response.md}) and writes grading.json beside each outputs/ folder.
Assertion text comes from each case's graders/*.md, in file order.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS = Path(__file__).resolve().parent
FENCE = re.compile(r"^```(\w*)\n(.*?)^```", re.S | re.M)


def blocks(md, lang=None):
    return [b for l, b in FENCE.findall(md) if lang is None or l == lang]


def bash_parse(md):
    for b in blocks(md, "bash"):
        with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as f:
            f.write(b)
        if subprocess.run(["bash", "-n", f.name], capture_output=True).returncode:
            return False, b[:80]
    return True, "all bash blocks parse"


def run_csv(md):
    py = [b for b in blocks(md, "python") if "csv" in b and "import" in b]
    if not py:
        return False, "no csv example"
    d = tempfile.mkdtemp()
    Path(d, "spend.csv").write_text("name,amount\ncoffee,4.50\nlunch,12.00\ncoffee,3.75\n")
    Path(d, "x.py").write_text(py[-1])
    r = subprocess.run([sys.executable, "x.py"], cwd=d, capture_output=True, text=True)
    return r.stdout.strip() == "20.25", f"stdout={r.stdout.strip()!r} err={r.stderr.strip()[-120:]!r}"


def count_empty(md):
    bash = blocks(md, "bash")
    if not bash:
        return False, "no bash blocks"
    d = tempfile.mkdtemp()
    os.makedirs(f"{d}/backups")
    r = subprocess.run(["bash", "-c", bash[-1]], cwd=d, capture_output=True, text=True,
                       env={**os.environ, "HOME": d, "BACKUP_DIR": f"{d}/backups", "PROJECT_DIR": f"{d}/site"})
    out = r.stdout.strip()
    return out.split()[:1] == ["0"], f"stdout={out!r}"


def grade(case, md, orig, resp):
    bash = "\n".join(blocks(md, "bash"))
    checks = {
        "bash-cross-block-drift": lambda: [
            (not re.search(r"\$\{?backup_dir", bash) or not re.search(r"\$\{?BACKUP_DIR", bash),
             "backup dir names: " + ",".join(sorted(set(re.findall(r"\$\{?(\w*[Bb][Aa][Cc][Kk][Uu][Pp]\w*)", bash))))),
            (not ("config.yaml" in md and "config.yml" in md.replace("config.yaml", "")),
             "config names found: " + ",".join(sorted(set(re.findall(r"config\.ya?ml", md))))),
            (len(re.findall(r"mkdir -p", bash)) <= 1 and len(re.findall(r"PROJECT_DIR=", bash)) <= 1,
             f"mkdir={len(re.findall('mkdir -p', bash))} PROJECT_DIR= {len(re.findall('PROJECT_DIR=', bash))}"),
            (bool(re.search(r"tar\s+(-\w*z|\w*z\w*\s|.*--gzip|.*-z\b)", bash)),
             "tar line: " + "; ".join(l.strip() for l in bash.splitlines() if "tar " in l)),
            (not re.search(r"for .* in \$\(ls", bash), "ls loop check"),
            bash_parse(md),
            (bool(re.search(r"before", resp, re.I) and re.search(r"after", resp, re.I)
                  and re.search(r"\d+(\.\d)?\s*(/\s*10|→|->|before|after)", resp)), "scores in response"),
            count_empty(md),
        ],
        "python-keeps-before-code": lambda: [
            (blocks(orig, "python")[0] in blocks(md, "python"), "slow-way block identical"),
            ("class SpendCalculator" not in md and "_parse_amount" not in md, "class/helper removed"),
            ("DictReader" in md, "DictReader present"),
            (not re.search(r"except( Exception)?:\s*\n\s*pass", md), "no swallowed except"),
            run_csv(md),
            (blocks(orig, "mermaid") == blocks(md, "mermaid"), "mermaid identical"),
            (any("round(" in b for b in blocks(md, "python") if "DictReader" in b), "round() in csv example"),
        ],
        "clean-article-unchanged": lambda: [
            (md == orig, "identical" if md == orig else "file changed"),
            (bool(re.search(r"nothing needed chang|unchanged|no (code )?changes|already (as )?simple|left (it )?unchanged"
                            r"|nothing to (change|simplify)|didn.t (change|edit)|no edits", resp, re.I)),
             "response says no change needed"),
        ],
    }[case]()
    return checks


def assertions(case):
    out = []
    for g in sorted((EVALS / case / "graders").glob("*.md")):
        out.append(re.sub(r"\A---\n.*?\n---\n", "", g.read_text(), flags=re.S).strip())
    return out


def grade_run(case, md, resp):
    orig = (EVALS / case / "files" / "index.md").read_text()
    res = grade(case, md, orig, resp)
    exps = [{"text": t, "passed": bool(ok), "evidence": ev} for t, (ok, ev) in zip(assertions(case), res)]
    n = sum(e["passed"] for e in exps)
    return {"expectations": exps,
            "summary": {"passed": n, "failed": len(exps) - n, "total": len(exps), "pass_rate": round(n / len(exps), 2)}}


def read(p):
    return p.read_text() if p.exists() else ""


def main(argv):
    if len(argv) >= 2:
        g = grade_run(argv[0], read(Path(argv[1])), read(Path(argv[2])) if len(argv) > 2 else "")
        for e in g["expectations"]:
            print(f"{'PASS' if e['passed'] else 'FAIL'}  {e['text'][:90]}\n      {e['evidence']}")
        print(f"{g['summary']['passed']}/{g['summary']['total']}")
        return 0 if g["summary"]["failed"] == 0 else 1
    if len(argv) != 1:
        print(__doc__)
        return 2
    for case_dir in sorted(p for p in Path(argv[0]).iterdir() if p.is_dir() and (EVALS / p.name).is_dir()):
        for run in sorted(p.parent for p in case_dir.glob("**/outputs")):
            g = grade_run(case_dir.name, read(run / "outputs" / "index.md"), read(run / "outputs" / "response.md"))
            (run / "grading.json").write_text(json.dumps(g, indent=2))
            marks = " ".join("✓" if e["passed"] else "✗" for e in g["expectations"])
            print(f"{case_dir.name:28} {run.relative_to(case_dir)!s:14} {g['summary']['passed']}/{g['summary']['total']}  {marks}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

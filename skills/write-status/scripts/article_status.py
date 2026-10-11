#!/usr/bin/env python3
"""Which writing skills have already run on an article, and which are missing.

Usage:
  article_status.py check [ARTICLE] [--json] [--since-days N]
  article_status.py record SKILL ARTICLE [--note TEXT]
  article_status.py review latest ARTICLE   # newest saved write-review report
  article_status.py review new ARTICLE      # path to save a new report to

ARTICLE is a path to a page bundle's index.md (or its folder). With no ARTICLE,
check uses write-review's last-article.sh (the last article created or changed).

Evidence, strongest first:
  ledger      ~/.local/state/jbb-writing/runs.jsonl, written by `record`. Durable.
  transcript  a Skill call or /slash command in ~/.claude/projects/*/*.jsonl whose
              arguments name the article's folder. Claude deletes transcripts after
              cleanupPeriodDays (default 30), so absence here is weak evidence.
  inferred    a transcript call with no arguments, attributed to the first article
              that session read afterwards.
  artifact    a file-level sign (cover image exists, SEO front matter is complete).
              Shows the work is there, not that the skill ran.

A run is "stale" when the article's last commit (or mtime, if uncommitted) is
newer than the run.

Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Skills that act on one article, in the order an author usually runs them.
SKILLS = [
    "write-review",
    "write-review-apply",
    "write-seo",
    "write-validate-article",
    "write-check-links",
    "write-run-markdown-lint",
    "hugo-agents-compliance",
    "generate-cover-image",
]
# Skills whose result is a check of the text: a later edit makes the result stale.
# The others (SEO, cover) leave their work in the file, so later edits don't undo them.
CHECKS = {"write-review", "write-validate-article", "write-check-links",
          "write-run-markdown-lint", "hugo-agents-compliance"}
ALIASES = {
    "write-internal-link-optimize": "write-seo",
    "write-cover": "generate-cover-image",
    "hugo-agents": "hugo-agents-compliance",
}

STATE = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state")) / "jbb-writing"
LEDGER = STATE / "runs.jsonl"
REVIEWS = STATE / "reviews"
PROJECTS = Path.home() / ".claude/projects"
SKILL_DIR = Path(__file__).resolve().parent.parent
LAST_ARTICLE = SKILL_DIR.parent / "write-review/scripts/last-article.sh"


def norm_skill(name: str) -> str | None:
    """Map 'jbb-writing-skills:write-review', '/write:review', 'write-review' to one key."""
    n = name.strip().lstrip("/").lower()
    if n.startswith("write:") or n.startswith("hugo:"):
        n = n.replace(":", "-", 1)
    elif ":" in n:
        n = n.rsplit(":", 1)[1]
    n = ALIASES.get(n, n)
    return n if n in SKILLS else None


def resolve_article(arg: str | None) -> Path:
    if arg:
        p = Path(arg).expanduser().resolve()
        if p.is_dir():
            p = p / "index.md"
        if not p.is_file():
            sys.exit(f"article not found: {p}")
        return p
    if not LAST_ARTICLE.is_file():
        sys.exit("no article given and write-review's last-article.sh is not installed")
    out = subprocess.run([str(LAST_ARTICLE)], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(out.stderr.strip() or "last-article.sh found no article")
    return Path(out.stdout.split("\t")[0].strip())


def git_root(p: Path) -> Path | None:
    out = subprocess.run(["git", "-C", str(p.parent), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.returncode == 0 else None


def article_key(p: Path) -> str:
    """Repo-relative path when in git, else absolute. Used as the ledger key."""
    root = git_root(p)
    return str(p.relative_to(root)) if root else str(p)


def last_changed(p: Path) -> dt.datetime:
    """Mtime when the file has uncommitted changes, else its last commit time."""
    root = git_root(p)
    mtime = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc)
    if not root:
        return mtime
    dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--", str(p)],
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        return mtime
    ts = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%cI", "--", str(p)],
                        capture_output=True, text=True).stdout.strip()
    return dt.datetime.fromisoformat(ts) if ts else mtime


def parse_ts(s: str) -> dt.datetime | None:
    try:
        t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
    except (ValueError, AttributeError):
        return None


# ---------- evidence sources ----------

def ledger_runs(key: str, folder: str) -> list[dict]:
    runs = []
    if not LEDGER.is_file():
        return runs
    for line in LEDGER.read_text().splitlines():
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        a = r.get("article", "")
        if a == key or Path(a).parent.name == folder:
            s = norm_skill(r.get("skill", ""))
            t = parse_ts(r.get("ts", ""))
            if s and t:
                runs.append({"skill": s, "ts": t, "source": "ledger", "where": r.get("note", "")})
    return runs


CMD_NAME = re.compile(r"<command-name>(.*?)</command-name>")
CMD_ARGS = re.compile(r"<command-args>(.*?)</command-args>", re.S)
INDEX_MD = re.compile(r"content/(?:[^\s\"']+/)?([^/\s\"']+)/index\.md")


def transcript_runs(folder: str, since: dt.datetime | None) -> list[dict]:
    runs = []
    for f in glob.glob(str(PROJECTS / "*/*.jsonl")):
        if since and dt.datetime.fromtimestamp(os.path.getmtime(f), dt.timezone.utc) < since:
            continue
        pending = []  # (skill, ts) invoked with no args; attribute to the next article read
        try:
            fh = open(f, errors="ignore")
        except OSError:
            continue
        with fh:
            for line in fh:
                quick = '"Skill"' in line or "<command-name>" in line
                if not quick and not (pending and "index.md" in line):
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = parse_ts(d.get("timestamp", ""))
                content = (d.get("message") or {}).get("content")
                calls = []  # (skill, args)
                if isinstance(content, str) and "<command-name>" in content:
                    m = CMD_NAME.search(content)
                    a = CMD_ARGS.search(content)
                    if m:
                        calls.append((m.group(1), a.group(1) if a else ""))
                elif isinstance(content, list):
                    for b in content:
                        if not isinstance(b, dict) or b.get("type") != "tool_use":
                            continue
                        inp = b.get("input") or {}
                        if b.get("name") == "Skill":
                            calls.append((inp.get("skill", ""), inp.get("args", "") or ""))
                        elif pending:
                            m = INDEX_MD.search(json.dumps(inp))
                            if m:
                                for s, t in pending:
                                    if m.group(1) == folder:
                                        runs.append({"skill": s, "ts": t, "source": "inferred",
                                                     "where": Path(f).name[:8]})
                                pending = []
                for name, args in calls:
                    s = norm_skill(name)
                    if not s or not ts:
                        continue
                    if not args.strip():
                        pending.append((s, ts))
                    elif re.search(rf"(?<![\w-]){re.escape(folder)}(?![\w-])", args):
                        runs.append({"skill": s, "ts": ts, "source": "transcript",
                                     "where": Path(f).name[:8]})
    return runs


def front_matter(p: Path) -> str:
    text = p.read_text(errors="ignore")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def artifact_signs(p: Path) -> dict[str, str]:
    fm = front_matter(p)
    signs = {}
    m = re.search(r"^cover:\s*\n(?:\s+.*\n)*?\s+image:\s*\"?([^\"\n]+)", fm + "\n", re.M)
    if m and (p.parent / m.group(1).strip()).is_file():
        signs["generate-cover-image"] = f"cover {m.group(1).strip()} exists"
    desc = re.search(r'^description:\s*"?(.*?)"?\s*$', fm, re.M)
    kw = re.search(r"^keywords:\s*\n((?:\s+-.*\n?)+)", fm + "\n", re.M)
    n_kw = len(re.findall(r"^\s+-", kw.group(1), re.M)) if kw else 0
    if desc and len(desc.group(1)) <= 160 and 4 <= n_kw <= 7:
        signs["write-seo"] = f"front matter complete ({n_kw} keywords, description {len(desc.group(1))} chars)"
    return signs


# ---------- commands ----------

def check(args) -> int:
    p = resolve_article(args.article)
    key, folder = article_key(p), p.parent.name
    changed = last_changed(p)
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.since_days)
             if args.since_days else None)
    runs = ledger_runs(key, folder) + transcript_runs(folder, since)
    signs = artifact_signs(p)
    rank = {"ledger": 0, "transcript": 1, "inferred": 2}

    rows = []
    for s in SKILLS:
        mine = [r for r in runs if r["skill"] == s]
        if mine:
            last = max(mine, key=lambda r: (r["ts"], -rank[r["source"]]))
            status = "stale" if s in CHECKS and last["ts"] < changed else "ran"
            rows.append({"skill": s, "status": status, "last_run": last["ts"].isoformat(timespec="minutes"),
                         "source": last["source"], "runs": len(mine),
                         "detail": f"session {last['where']}" if last["source"] != "ledger" else last["where"]})
        elif s in signs:
            rows.append({"skill": s, "status": "artifact", "last_run": None,
                         "source": "artifact", "runs": 0, "detail": signs[s]})
        else:
            rows.append({"skill": s, "status": "missing", "last_run": None,
                         "source": None, "runs": 0, "detail": ""})

    result = {"article": str(p), "folder": folder, "changed": changed.isoformat(timespec="minutes"),
              "ledger": str(LEDGER), "transcripts_kept_days": transcript_retention(), "skills": rows}
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    print(f"Article: {p}")
    print(f"Last changed: {result['changed']}")
    w = max(len(s) for s in SKILLS)
    for r in rows:
        when = r["last_run"] or "-"
        print(f"  {r['skill']:<{w}}  {r['status']:<8}  {when:<22}  {r['source'] or '-':<10}  {r['detail']}".rstrip())
    return 0


def transcript_retention() -> int:
    try:
        cfg = json.loads((Path.home() / ".claude/settings.json").read_text())
        return int(cfg.get("cleanupPeriodDays", 30))
    except (OSError, ValueError):
        return 30


def record(args) -> int:
    s = norm_skill(args.skill)
    if not s:
        sys.exit(f"unknown skill {args.skill!r}; expected one of {', '.join(SKILLS)}")
    p = Path(args.article).expanduser().resolve()
    if p.is_dir():
        p = p / "index.md"
    if not p.is_file():
        sys.exit(f"article not found: {p}")
    STATE.mkdir(parents=True, exist_ok=True)
    entry = {"ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
             "skill": s, "article": article_key(p), "note": args.note or ""}
    with LEDGER.open("a") as fh:
        fh.write(json.dumps(entry) + "\n")
    print(f"recorded {s} on {entry['article']}")
    return 0


def review(args) -> int:
    """Saved write-review reports live in REVIEWS/<bundle folder>/<UTC stamp>.md."""
    p = Path(args.article).expanduser().resolve()
    if p.is_dir():
        p = p / "index.md"
    if not p.is_file():
        sys.exit(f"article not found: {p}")
    d = REVIEWS / p.parent.name
    if args.action == "new":
        d.mkdir(parents=True, exist_ok=True)
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        print(d / f"{stamp}.md")
        return 0
    found = sorted(d.glob("*.md")) if d.is_dir() else []
    if not found:
        print(f"no saved review for {p.parent.name}", file=sys.stderr)
        return 1
    newest = found[-1]
    ran = dt.datetime.strptime(newest.stem, "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc)
    changed = last_changed(p)
    state = "stale" if ran < changed else "current"
    print(f"{newest}\t{state}\treviewed {ran.isoformat(timespec='minutes')}, "
          f"article changed {changed.isoformat(timespec='minutes')}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("article", nargs="?")
    c.add_argument("--json", action="store_true")
    c.add_argument("--since-days", type=int, default=0,
                   help="only scan transcripts modified in the last N days (faster)")
    c.set_defaults(fn=check)
    r = sub.add_parser("record")
    r.add_argument("skill")
    r.add_argument("article")
    r.add_argument("--note")
    r.set_defaults(fn=record)
    v = sub.add_parser("review")
    v.add_argument("action", choices=["latest", "new"])
    v.add_argument("article")
    v.set_defaults(fn=review)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())

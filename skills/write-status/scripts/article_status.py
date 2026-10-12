#!/usr/bin/env python3
"""Which writing skills have already run on an article, and which are missing.

Usage:
  article_status.py check [ARTICLE] [--json] [--since-days N]
  article_status.py record SKILL ARTICLE [--note TEXT] [--force]
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

write-validate-article runs lychee, markdownlint-cli2 and an AGENTS.md pass, so
its run also counts for write-check-links, write-run-markdown-lint and
hugo-agents-compliance ("covered") unless one of those has a newer run of its own,
or the validate note says a step was NOT RUN.

SEO artifact rule (from hugo/content/prompts/seo-front-matter.md): quoted-or-not
description of at most 160 characters and 4-7 keywords.

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
# write-validate-article runs these as its own steps (lychee, markdownlint-cli2,
# AGENTS.md pass), so a current validate run covers them.
COVERED_BY = {"write-check-links": "write-validate-article",
              "write-run-markdown-lint": "write-validate-article",
              "hugo-agents-compliance": "write-validate-article"}
SEO_DESC_MAX = 160
SEO_KW_MIN, SEO_KW_MAX = 4, 7
DEDUPE_MINUTES = 10
DEFAULT_BLOG = Path.home() / "Projects/websites/jeffbaileyblog"
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


def blog_root_source() -> str:
    """Which rule last-article.sh will use to pick the repo (mirrors its pick_root)."""
    br = os.environ.get("BLOG_ROOT")
    if br and git_root(Path(br) / "x"):
        return f"BLOG_ROOT={br}"
    cwd = git_root(Path.cwd() / "x")
    if cwd and ((cwd / "content").is_dir() or (cwd / "hugo/content").is_dir()):
        return f"cwd repo {cwd}"
    return f"default {DEFAULT_BLOG} (BLOG_ROOT unset, cwd is not a blog repo)"


def resolve_article(arg: str | None) -> tuple[Path, str]:
    """Return the article and a one-line note on how it was picked."""
    if arg:
        p = Path(arg).expanduser().resolve()
        if p.is_dir():
            p = p / "index.md"
        if not p.is_file():
            sys.exit(f"article not found: {p}")
        return p, "named by the user"
    if not LAST_ARTICLE.is_file():
        sys.exit("no article given and write-review's last-article.sh is not installed; "
                 "pass the article path")
    root = blog_root_source()
    out = subprocess.run([str(LAST_ARTICLE)], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit((out.stderr.strip() or "last-article.sh found no article") + f" [repo from {root}]")
    path, _, how = out.stdout.strip().partition("\t")
    return Path(path.strip()), f"last-article.sh ({how or 'unknown'}); repo from {root}"


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
    n_desc = len(desc.group(1)) if desc else 0
    if desc and n_desc <= SEO_DESC_MAX and SEO_KW_MIN <= n_kw <= SEO_KW_MAX:
        signs["write-seo"] = f"front matter complete ({n_kw} keywords, description {n_desc} chars)"
    else:
        why = []
        if not desc:
            why.append("no description")
        elif n_desc > SEO_DESC_MAX:
            why.append(f"description {n_desc} chars > {SEO_DESC_MAX}")
        if not SEO_KW_MIN <= n_kw <= SEO_KW_MAX:
            why.append(f"{n_kw} keywords, needs {SEO_KW_MIN}-{SEO_KW_MAX}")
        signs["write-seo-why"] = "front matter incomplete: " + ", ".join(why)
    return signs


# ---------- commands ----------

def check(args) -> int:
    p, picked = resolve_article(args.article)
    key, folder = article_key(p), p.parent.name
    changed = last_changed(p)
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.since_days)
             if args.since_days else None)
    runs = ledger_runs(key, folder) + transcript_runs(folder, since)
    signs = artifact_signs(p)
    rank = {"ledger": 0, "transcript": 1, "inferred": 2}

    def latest(skill):
        mine = [r for r in runs if r["skill"] == skill]
        return (max(mine, key=lambda r: (r["ts"], -rank[r["source"]])), len(mine)) if mine else (None, 0)

    rows = []
    for s in SKILLS:
        last, n = latest(s)
        parent = COVERED_BY.get(s)
        plast = latest(parent)[0] if parent else None
        if plast and "not run" in plast["where"].lower():
            plast = None  # validate skipped a step; don't claim coverage
        if plast and (not last or plast["ts"] > last["ts"]):
            stale = s in CHECKS and plast["ts"] < changed
            rows.append({"skill": s, "status": "stale" if stale else "covered",
                         "last_run": plast["ts"].isoformat(timespec="minutes"),
                         "source": plast["source"], "runs": n,
                         "detail": f"by {parent}" + (" (article changed since)" if stale else "")})
        elif last:
            status = "stale" if s in CHECKS and last["ts"] < changed else "ran"
            rows.append({"skill": s, "status": status, "last_run": last["ts"].isoformat(timespec="minutes"),
                         "source": last["source"], "runs": n,
                         "detail": f"session {last['where']}" if last["source"] != "ledger" else last["where"]})
        elif s in signs:
            rows.append({"skill": s, "status": "artifact", "last_run": None,
                         "source": "artifact", "runs": 0, "detail": signs[s]})
        else:
            rows.append({"skill": s, "status": "missing", "last_run": None,
                         "source": None, "runs": 0, "detail": signs.get(f"{s}-why", "")})

    by = {st: [r["skill"] for r in rows if r["status"] == st]
          for st in ("missing", "stale", "covered", "artifact")}
    result = {"article": str(p), "folder": folder, "picked_by": picked,
              "changed": changed.isoformat(timespec="minutes"),
              "ledger": str(LEDGER), "transcripts_kept_days": transcript_retention(),
              "skills": rows, "summary": by}
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    print(f"Article: {p}")
    print(f"Picked by: {picked}")
    print(f"Last changed: {result['changed']}")
    w = max(len(s) for s in SKILLS)
    for r in rows:
        when = r["last_run"] or "-"
        print(f"  {r['skill']:<{w}}  {r['status']:<8}  {when:<22}  {r['source'] or '-':<10}  {r['detail']}".rstrip())
    stale_txt = ", ".join(f"{r['skill']} ({r['last_run'][:16].replace('T', ' ')})"
                          for r in rows if r["status"] == "stale")
    print(f"Missing: {', '.join(by['missing']) or 'none'}. Stale: {stale_txt or 'none'}."
          + (f" Covered by write-validate-article: {', '.join(by['covered'])}." if by["covered"] else ""))
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
    now = dt.datetime.now(dt.timezone.utc)
    # Microseconds, so a record made in the same second as an edit doesn't read as stale.
    entry = {"ts": now.isoformat(timespec="microseconds"),
             "skill": s, "article": article_key(p), "note": args.note or ""}
    if not args.force:
        for r in reversed(ledger_runs(entry["article"], p.parent.name)):
            if r["skill"] == s and now - r["ts"] < dt.timedelta(minutes=DEDUPE_MINUTES):
                print(f"already recorded {s} on {entry['article']} at "
                      f"{r['ts'].isoformat(timespec='seconds')}; skipped (use --force to add another)")
                return 0
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
    r.add_argument("--force", action="store_true",
                   help=f"append even if the same skill was recorded on this article in the last {DEDUPE_MINUTES} min")
    r.set_defaults(fn=record)
    v = sub.add_parser("review")
    v.add_argument("action", choices=["latest", "new"])
    v.add_argument("article")
    v.set_defaults(fn=review)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())

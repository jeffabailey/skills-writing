#!/usr/bin/env python3
"""Check a comparison article (content/blog/x-vs-x/<slug>/index.md) for the
comparison-specific rules in SKILL.md, and optionally build it with Hugo.

Usage:
  check_comparison.py path/to/index.md            # Markdown checks only
  check_comparison.py path/to/index.md --build    # + hugo -D build to a temp dir
  check_comparison.py path/to/index.md --json

Exit codes: 0 = no FAIL, 1 = at least one FAIL, 3 = required tool missing.
WARN lines are judgement calls for the writer; FAIL lines must be fixed.
"""
import argparse
import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ORDER = [
    "The short answer", "The contenders", "At a glance", "How these were compared",
    "Head-to-head", "Which should you choose?", "Strengths and trade-offs", "Cost",
    "The bottom line", "FAQ", "References", "Related Content",
]
OPTIONAL = {"Cost", "Which should you choose?"}
results = []


def add(level, check, detail=""):
    results.append({"level": level, "check": check, "detail": detail})


def split_front_matter(md):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.DOTALL)
    return (m.group(1), m.group(2)) if m else ("", md)


def fm_value(fm, key):
    m = re.search(rf"^{key}:\s*(.+?)\s*$", fm, re.MULTILINE)
    return m.group(1).strip().strip('"') if m else None


def sections(body):
    parts = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
    out = {"Intro": parts[0]}
    for i in range(1, len(parts), 2):
        out[parts[i].strip()] = parts[i + 1]
    return [p.strip() for p in parts[1::2]], out


def strip_code(text):
    return re.sub(r"^(```|~~~).*?^\1\s*$", "", text, flags=re.MULTILINE | re.DOTALL)


def cards(text):
    m = re.search(r"\{\{<\s*cards\s*>\}\}(.*?)\{\{<\s*/cards\s*>\}\}", text, re.DOTALL)
    return [c.strip() for c in m.group(1).split("--card--")] if m else []


LABEL = re.compile(r"^\* \*\*(.+?)\.\*\* \S", re.MULTILINE)


def check_structure(fm, body):
    if fm_value(fm, "articletype") == "comparison":
        add("PASS", "front matter articletype: comparison")
    else:
        add("FAIL", "front matter articletype: comparison", "missing or different")
    if fm_value(fm, "diataxis") == "explanation":
        add("PASS", "front matter diataxis: explanation")
    else:
        add("FAIL", "front matter diataxis: explanation", "missing or different")
    desc = fm_value(fm, "description") or ""
    if len(desc) > 160:
        add("FAIL", "description <= 160 chars", f"{len(desc)} chars")

    h2, sec = sections(body)
    if not h2 or h2[0] != "The short answer":
        add("FAIL", "first H2 is 'The short answer'", f"first H2: {h2[:1]}")
    else:
        add("PASS", "first H2 is 'The short answer'")
    known = [h for h in h2 if h in ORDER]
    missing = [h for h in ORDER if h not in h2 and h not in OPTIONAL]
    if missing:
        add("FAIL", "required sections present", "missing: " + ", ".join(missing))
    if known != sorted(known, key=ORDER.index):
        add("FAIL", "sections in canonical order", " > ".join(known))
    elif not missing:
        add("PASS", "required sections present and in canonical order")

    contenders = cards(sec.get("The contenders", ""))
    n = len(contenders) or None
    sa = sec.get("The short answer", "")
    choose = re.findall(r"\*\*Choose .+? if", sa)
    if not cards(sa):
        add("FAIL", "short answer uses cards")
    if n and len(choose) != n:
        add("FAIL", "one 'Choose X if' per option", f"{len(choose)} vs {n} contenders")
    elif choose:
        add("PASS", "one 'Choose X if' per option", str(len(choose)))

    glance = cards(sec.get("At a glance", ""))
    if not glance:
        add("FAIL", "At a glance uses cards")
    else:
        labels = [LABEL.findall(c) for c in glance]
        if n and len(glance) != n:
            add("FAIL", "one scorecard card per option", f"{len(glance)} vs {n}")
        if not labels[0]:
            add("FAIL", "scorecard fields use '* **Label.** value'")
        elif all(lab == labels[0] for lab in labels):
            ok = 4 <= len(labels[0]) <= 7 and labels[0][-1] == "Best for"
            add("PASS" if ok else "WARN", "scorecard labels identical across cards",
                ", ".join(labels[0]) + ("" if ok else " (want 5-6 fields ending in 'Best for')"))
        else:
            add("FAIL", "scorecard labels identical across cards", json.dumps(labels))

    meth = LABEL.findall(sec.get("How these were compared", ""))
    hh = sec.get("Head-to-head", "")
    crit = [c.strip() for c in re.findall(r"^### (.+)$", hh, re.MULTILINE)]
    if meth and meth == crit:
        add("PASS", "Head-to-head ### match methodology criteria", ", ".join(crit))
    else:
        add("FAIL", "Head-to-head ### match methodology criteria",
            f"methodology {meth} vs head-to-head {crit}")
    subs = re.split(r"^### .+$", hh, flags=re.MULTILINE)[1:]
    bad = [crit[i] for i, s in enumerate(subs) if not s.strip().startswith("Winner here:")]
    add("FAIL" if bad else "PASS", "each Head-to-head ### opens with 'Winner here:'",
        ", ".join(bad))

    procons = len(re.findall(r"\{\{<\s*procon\s*>\}\}", body))
    if n and procons < n:
        add("FAIL", "one procon block per option", f"{procons} vs {n}")
    elif procons:
        add("PASS", "one procon block per option", str(procons))
    if re.search(r"\|\s*-{3,}", strip_code(body)):
        add("FAIL", "no Markdown tables (use cards)")
    if "category_footer" in body:
        add("FAIL", "no category_footer partial in body",
            "layouts/_default/single.html already renders it; remove the line")
    if "—" in body:
        add("FAIL", "no emdashes", f"{body.count(chr(0x2014))} found")
    return sec


FIRST_PERSON = re.compile(r"\b(I|I'm|I've|I'll|I'd|[Mm]y|[Ww]e|[Ww]e're|[Ww]e've|[Oo]ur|[Oo]urs|us)\b")


def check_voice(body):
    hits = []
    text = strip_code(body)
    for ln, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        # Reader-voice FAQ questions ("Do I need to pay?") are not author voice.
        if re.match(r"^(\*\*|###? ).*\?(\*\*)?$", s):
            continue
        if s.startswith("[") and "]:" in s:
            continue
        if FIRST_PERSON.search(s):
            hits.append(s[:100])
    add("FAIL" if hits else "PASS", "no first-person author voice (FAQ questions exempt)",
        " | ".join(hits[:5]))


CLAIM = re.compile(
    r"(\bv?\d+\.\d+(\.\d+)?\b|[$€£]\s?\d|\b\d+(\.\d+)?\s?%|"
    r"\b\d[\d,]*\s?(employees|resources|users|seats|stars|downloads|GB|MB|ms)\b|"
    r"\b(Apache|MIT|GPL|AGPL|LGPL|MPL|BSL|BUSL|SSPL)\b|\b(Source|Public) License\b)")
# Summary sections restate claims; the claim must be sourced where the body makes it.
SUMMARY = {"The short answer", "At a glance", "Which should you choose?", "The bottom line",
           "FAQ", "References", "Related Content"}


def check_sources(sec):
    unsourced = []
    for name, text in sec.items():
        if name in SUMMARY:
            continue
        for line in strip_code(text).splitlines():
            s = line.strip()
            if not s or s.startswith(("#", "{{<", "[")) and "]:" in s or s.startswith("{{<"):
                continue
            for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z*])", s):
                if CLAIM.search(sent) and not re.search(r"\]\[|\]\(|TODO verify", sent):
                    unsourced.append(f"[{name}] {sent[:110]}")
    add("WARN" if unsourced else "PASS",
        "version/price/license claims carry a link or 'TODO verify'",
        f"{len(unsourced)} unsourced: " + " | ".join(unsourced[:8]) if unsourced else "")


def hugo_list(hugo_dir):
    try:
        out = subprocess.run(["hugo", "list", "all"], cwd=hugo_dir, capture_output=True,
                             text=True, timeout=120).stdout
        return list(csv.DictReader(io.StringIO(out)))
    except Exception:
        return []


def check_refs(body, hugo_dir, rows):
    refs = sorted(set(re.findall(r"\{\{<\s*ref\s+\"([^\"]+)\"\s*>\}\}", body)))
    if not refs:
        add("WARN", "internal links", "no {{< ref >}} links; add Related Content links")
        return
    for r in refs:
        key = r.strip("/").removesuffix("/index.md").removesuffix(".md")
        match = [row for row in rows if re.search(
            rf"(^|/){re.escape(key)}(/index|/_index)?\.md$", row["path"])]
        if not rows:
            path = os.path.join(hugo_dir, "content")
            found = [os.path.join(d, f) for d, _, fs in os.walk(path) for f in fs
                     if os.path.join(d, f).endswith((f"/{key}/index.md", f"/{key}.md"))]
            match = [{"path": f, "draft": "true" if re.search(
                r"^draft:\s*true", open(f).read(), re.MULTILINE) else "false"} for f in found]
        if not match:
            add("FAIL", f"ref \"{r}\" resolves",
                "no content path ends with this name (refs resolve by path/folder, not slug)")
        elif match[0]["draft"] == "true":
            add("WARN", f"ref \"{r}\" target is a draft",
                f"{match[0]['path']}: builds only with -D; once this article is published "
                "the normal build fails REF_NOT_FOUND. Link a published post instead.")
        else:
            add("PASS", f"ref \"{r}\" resolves to published {match[0]['path']}")


def build(hugo_dir, fm, body):
    out = tempfile.mkdtemp(prefix="cmp-build-")
    p = subprocess.run(["hugo", "--gc", "--minify", "-D", "-d", out], cwd=hugo_dir,
                       capture_output=True, text=True, timeout=900)
    log = p.stdout + p.stderr
    if p.returncode != 0 or "REF_NOT_FOUND" in log:
        add("FAIL", "hugo --gc --minify -D builds", log[-800:])
        return
    add("PASS", "hugo --gc --minify -D builds", out)
    url = (fm_value(fm, "url") or "").strip("/")
    page = os.path.join(out, url, "index.html")
    if not url or not os.path.exists(page):
        add("FAIL", "rendered page HTML exists", page)
        return
    html = open(page, encoding="utf-8").read()
    add("PASS", "rendered page HTML exists", page)
    for needle in ("card-grid", "md-procon"):
        add("PASS" if needle in html else "FAIL", f"rendered HTML contains {needle}")
    if "```mermaid" in body:
        ok = re.search(r'class="?mermaid', html)
        add("PASS" if ok else "FAIL", "mermaid decision tree rendered")
    leaks = len(re.findall(r"\{\{(&lt;|<|%)", re.sub(r"<pre.*?</pre>", "", html, flags=re.DOTALL)))
    add("FAIL" if leaks else "PASS", "no raw shortcode text in HTML", str(leaks))
    footers = len(re.findall(r"<h2[^>]*>\s*Related Articles by Category", html))
    add("FAIL" if footers > 1 else "PASS", "category footer renders once", str(footers))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("index_md")
    ap.add_argument("--hugo-dir", help="Hugo site root (default: nearest parent with config.toml)")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    hugo_dir = a.hugo_dir
    if not hugo_dir:
        d = os.path.dirname(os.path.abspath(a.index_md))
        while d != "/" and not os.path.exists(os.path.join(d, "config.toml")):
            d = os.path.dirname(d)
        hugo_dir = d if d != "/" else None
    have_hugo = shutil.which("hugo") is not None
    if a.build and not have_hugo:
        print("TOOL MISSING: hugo (install: brew install hugo). Build not run; this is not a check failure.")
        sys.exit(3)

    md = open(a.index_md, encoding="utf-8").read()
    fm, body = split_front_matter(md)
    sec = check_structure(fm, body)
    check_voice(body)
    check_sources(sec)
    if hugo_dir:
        check_refs(body, hugo_dir, hugo_list(hugo_dir) if have_hugo else [])
        if a.build:
            build(hugo_dir, fm, body)
    else:
        add("WARN", "Hugo site root", "no config.toml above the article; refs and build skipped")

    if a.json:
        print(json.dumps(results, indent=1))
    else:
        for r in results:
            print(f"{r['level']:4}  {r['check']}" + (f"  -- {r['detail']}" if r["detail"] else ""))
    sys.exit(1 if any(r["level"] == "FAIL" for r in results) else 0)


if __name__ == "__main__":
    main()

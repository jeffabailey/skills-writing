#!/usr/bin/env python3
"""Read-only index of jeffbaileyblog posts and categories for ideation.

Usage (run from anywhere; --root defaults to the nearest hugo/ dir or
~/Projects/websites/jeffbaileyblog/hugo):

  blog_index.py [--hugo] posts [--section learn-x] [--published-only]
      TSV: title, slug, section, path, draft, words, description
  blog_index.py categories
      TSV: slug, title  (front matter uses the title; folder is the slug)
  blog_index.py match "idea title or keywords" [-n 5]
      Closest existing posts by token overlap on title, slug, description.
      Flags draft stubs (draft: true, < 200 body words) as FINISH-INSTEAD.
  blog_index.py coverage "kw1, kw2, kw3"
      Every post whose title/slug/description/categories mention any keyword,
      grouped by section, so you can see how covered an area already is.

Slug falls back to the last segment of url:, then the bundle folder name.
The path column is what {{< ref >}} needs, not the slug.
"""
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:  # PyYAML missing: use the tiny fallback parser
    yaml = None

STOP = set(["a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how", "i", "in", "into", "is", "it", "its", "of", "on", "or", "the", "to", "vs", "what", "when", "where", "which", "who", "why", "with", "your", "you", "x", "my", "do", "does", "should", "can", "guide", "intro", "introduction", "learn", "fundamentals", "am", "me", "we", "our", "this", "that", "not", "did", "need", "be", "after"])
STUB_WORDS = 200


def find_root(arg):
    if arg:
        return Path(arg).expanduser()
    here = Path.cwd()
    for p in [here, *here.parents]:
        if (p / "content" / "blog").is_dir():
            return p
        if (p / "hugo" / "content" / "blog").is_dir():
            return p / "hugo"
    return Path("~/Projects/websites/jeffbaileyblog/hugo").expanduser()


def split_front_matter(text):
    text = text.lstrip("﻿").lstrip()
    if not text.startswith("---"):
        return "", text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return "", text
    fm = parts[0][3:]
    body = parts[1].split("\n", 1)[1] if "\n" in parts[1] else ""
    return fm, body


def parse_fm(fm):
    if yaml is not None:
        try:
            data = yaml.safe_load(fm) or {}
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    data, key = {}, None
    for line in fm.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val in (">", ">-", "|", "|-", ""):
                data[key] = [] if val == "" else ""
            else:
                data[key] = val.strip("'\"")
            continue
        if key and line.startswith((" ", "\t")):
            s = line.strip()
            if s.startswith("- ") and isinstance(data.get(key), list):
                data[key].append(s[2:].strip("'\""))
            elif isinstance(data.get(key), str):
                data[key] = (data[key] + " " + s).strip()
    return data


def clean(v):
    if v is None:
        return ""
    return re.sub(r"\s+", " ", str(v)).strip()


def load_posts(root):
    blog = root / "content" / "blog"
    posts = []
    for f in sorted(blog.rglob("index.md")):
        rel = f.relative_to(root)
        parts = f.relative_to(blog).parts
        if len(parts) < 2:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm, body = split_front_matter(text)
        d = parse_fm(fm)
        slug = clean(d.get("slug"))
        if not slug and d.get("url"):
            slug = clean(d.get("url")).rstrip("/").split("/")[-1]
        if not slug:
            slug = f.parent.name
        cats = d.get("categories") or []
        if isinstance(cats, str):
            cats = [cats]
        draft = str(d.get("draft", False)).lower() == "true"
        posts.append({
            "title": clean(d.get("title")) or f.parent.name,
            "slug": slug,
            "section": parts[0] if len(parts) > 2 else "(blog root)",
            "path": str(rel),
            "draft": draft,
            "words": len(re.findall(r"\w+", body)),
            "description": clean(d.get("description")),
            "categories": [clean(c) for c in cats],
        })
    return posts


def overlay_hugo(root, posts):
    """Use `hugo list all` draft flags (the source of truth) when hugo exists."""
    import csv
    import io
    import shutil
    import subprocess
    if not shutil.which("hugo"):
        print("blog_index: hugo not found (brew install hugo); using front matter draft flags", file=sys.stderr)
        return
    try:
        out = subprocess.run(["hugo", "list", "all"], cwd=root, capture_output=True, text=True, timeout=120).stdout
    except Exception as e:
        print(f"blog_index: hugo list all failed ({e}); using front matter", file=sys.stderr)
        return
    flags = {r["path"]: r["draft"] == "true" for r in csv.DictReader(io.StringIO(out)) if r.get("path")}
    for p in posts:
        if p["path"] in flags:
            p["draft"] = flags[p["path"]]


def load_categories(root):
    out = []
    cdir = root / "content" / "categories"
    for d in sorted(p for p in cdir.iterdir() if p.is_dir()):
        title = d.name
        idx = d / "_index.md"
        if idx.exists():
            fm, _ = split_front_matter(idx.read_text(encoding="utf-8", errors="replace"))
            title = clean(parse_fm(fm).get("title")) or d.name
        out.append((d.name, title))
    return out


def stem(w):
    for suf in ("ing", "ies", "es", "s", "ed"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def tokens(s):
    return {stem(w) for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 1}


def score(q, p, df=None):
    t = tokens(p["title"]) | tokens(p["slug"].replace("-", " "))
    d = tokens(p["description"])
    if not q:
        return 0.0
    title_hit = len(q & t) / len(q)
    jac = len(q & t) / len(q | t) if (q | t) else 0
    desc_hit = len(q & d) / len(q)
    base = 0.5 * title_hit + 0.3 * jac + 0.2 * desc_hit
    # A short existing title wholly inside a longer idea ("Learn OpenTelemetry"
    # inside "Learn OpenTelemetry collector pipelines") is still a near-dup.
    # Only when they share a rare word, so "Learn AI" or "How Do I Learn
    # Code" do not swallow every idea that mentions AI or code.
    contained = len(q & t) / len(t) if t else 0
    if contained == 1 and df is not None and any(df.get(w, 0) <= 5 for w in q & t):
        base = max(base, 0.75)
    return round(base, 3)


def flag(p):
    if p["draft"] and p["words"] < STUB_WORDS:
        return "FINISH-INSTEAD (draft stub)"
    if p["draft"]:
        return "DRAFT (unpublished, in progress)"
    return "published"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="Hugo site dir (contains content/blog)")
    ap.add_argument("--hugo", action="store_true", help="take draft flags from `hugo list all`")
    sub = ap.add_subparsers(dest="cmd")
    sp = sub.add_parser("posts")
    sp.add_argument("--section")
    sp.add_argument("--published-only", action="store_true")
    sub.add_parser("categories")
    sm = sub.add_parser("match")
    sm.add_argument("query")
    sm.add_argument("-n", type=int, default=5)
    sc = sub.add_parser("coverage")
    sc.add_argument("keywords")
    a = ap.parse_args()
    root = find_root(a.root)
    if not (root / "content" / "blog").is_dir():
        sys.exit(f"blog_index: no content/blog under {root}; pass --root path/to/hugo")

    if a.cmd == "categories":
        print("slug\ttitle")
        for s, t in load_categories(root):
            print(f"{s}\t{t}")
        return
    posts = load_posts(root)
    if a.hugo:
        overlay_hugo(root, posts)
    if a.cmd == "match":
        q = tokens(a.query)
        df = {}
        for p in posts:
            for w in tokens(p["title"]) | tokens(p["slug"].replace("-", " ")):
                df[w] = df.get(w, 0) + 1
        for p in posts:
            p["score"] = score(q, p, df)
        ranked = sorted(posts, key=lambda p: p["score"], reverse=True)[: a.n]
        print("score\tstatus\ttitle\tsection\tpath\tdescription")
        for p in ranked:
            print(f"{p['score']}\t{flag(p)}\t{p['title']}\t{p['section']}\t{p['path']}\t{p['description'][:140]}")
        return
    if a.cmd == "coverage":
        kws = [k.strip().lower() for k in re.split(r"[,;]", a.keywords) if k.strip()]
        hits = {}
        for p in posts:
            hay = " ".join([p["title"], p["slug"], p["description"], " ".join(p["categories"])]).lower()
            m = [k for k in kws if re.search(r"\b" + re.escape(k), hay)]
            if m:
                hits.setdefault(p["section"], []).append((p, m))
        total = sum(len(v) for v in hits.values())
        print(f"# coverage for: {', '.join(kws)} -> {total} posts")
        for sec in sorted(hits):
            print(f"\n## {sec} ({len(hits[sec])})")
            for p, m in hits[sec]:
                print(f"- {p['title']} [{flag(p)}] {p['path']} (matched: {', '.join(m)})")
        return
    # default: posts
    print("title\tslug\tsection\tpath\tdraft\twords\tdescription")
    for p in posts:
        if a.section and p["section"] != a.section:
            continue
        if a.published_only and p["draft"]:
            continue
        print(f"{p['title']}\t{p['slug']}\t{p['section']}\t{p['path']}\t{str(p['draft']).lower()}\t{p['words']}\t{p['description']}")


if __name__ == "__main__":
    main()

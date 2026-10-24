#!/usr/bin/env python3
"""List the author's source material that sits beside an article's index.md.

Page bundles often hold the author's research next to the draft: notes.md, links.md,
or other sibling text files full of pasted URLs (many of them LinkedIn posts), with
duplicates, trailing commas and parentheses, and tracking parameters. This prints each
sibling file and one clean, de-duplicated URL list so the agent fetches every source
once.

Usage:
  source_links.py BUNDLE_DIR            # BUNDLE_DIR holds index.md (or pass index.md itself)

Output: one "file" line per sibling (name, line count, URL count, prose line count),
then one line per unique URL: "<domain>\t<url>\t<first sibling it appeared in>".
URLs already cited in index.md are marked "(already cited)" so they can be skipped.
Exits 1 when the bundle has no sibling source files.
"""
import os
import re
import sys
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SOURCE_EXTS = {".md", ".markdown", ".txt"}
URL_RE = re.compile(r"https?://[^\s<>\"'`\]]+")
TRAILING = ").,;:!?]>*_'\""
TRACKING = re.compile(r"^(utm_.*|rcm|trk|trackingId|triedRedirect|r|ref|ref_src|fbclid|gclid|mc_cid|mc_eid|si|igshid)$")


def clean(url):
    url = url.rstrip(TRAILING)
    parts = urlsplit(url)
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not TRACKING.match(k)])
    host = parts.netloc.lower().removeprefix("www.")
    return urlunsplit((parts.scheme.lower(), host, parts.path.rstrip("/") or "/", query, ""))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    bundle = sys.argv[1]
    if os.path.isfile(bundle):
        bundle = os.path.dirname(os.path.abspath(bundle))
    index = os.path.join(bundle, "index.md")
    cited = set()
    if os.path.isfile(index):
        with open(index, encoding="utf-8", errors="replace") as fh:
            cited = {clean(u) for u in URL_RE.findall(fh.read())}

    siblings = sorted(
        name for name in os.listdir(bundle)
        if name != "index.md" and os.path.splitext(name)[1].lower() in SOURCE_EXTS
        and os.path.isfile(os.path.join(bundle, name))
    )
    if not siblings:
        print(f"no sibling source files in {bundle}")
        return 1

    seen = {}
    for name in siblings:
        with open(os.path.join(bundle, name), encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
        urls = 0
        prose = 0
        for line in lines:
            found = URL_RE.findall(line)
            urls += len(found)
            for raw in found:
                seen.setdefault(clean(raw), name)
            rest = URL_RE.sub("", re.sub(r"\[[^\]]*\]\(\s*https?://[^)]*\)", "", line)).strip(" -*[]()#>`|,:")
            if rest and rest != "---" and not re.match(r"^(draft|title|date)\s*:", rest):
                prose += 1
        print(f"file\t{name}\t{len(lines)} lines\t{urls} urls\t{prose} prose lines")

    new = sum(1 for u in seen if u not in cited)
    print(f"unique\t{len(seen)} urls\t{new} not yet cited in index.md")
    for url, name in sorted(seen.items(), key=lambda kv: (urlsplit(kv[0]).netloc, kv[0])):
        mark = "\t(already cited)" if url in cited else ""
        print(f"{urlsplit(url).netloc}\t{url}\t{name}{mark}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

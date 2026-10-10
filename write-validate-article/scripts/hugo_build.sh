#!/usr/bin/env bash
# Hugo build gate for one article. Builds the whole site into a throwaway dir
# (never the repo's public/), adds --buildDrafts when the article is a draft
# (the default build skips drafts, so it would "pass" without rendering them),
# then confirms the article's page was actually rendered.
#
# Usage: hugo_build.sh path/to/index.md
# Exit:  0 BUILD OK | 1 BUILD FAILED for this article (an error names it, or its page did not render)
#        3 SITE BUILD BROKEN by other files only (no error names this article) | 2 usage/site not found | 127 hugo missing
set -uo pipefail

f="${1:-}"
[[ -f "$f" ]] || { echo "usage: hugo_build.sh path/to/index.md" >&2; exit 2; }
command -v hugo >/dev/null || { echo "TOOL MISSING: hugo (install: brew install hugo)"; exit 127; }

abs="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"
root="$(dirname "$abs")"
while [[ "$root" != "/" ]]; do
  for c in hugo.toml hugo.yaml hugo.json config.toml config.yaml config.json; do
    [[ -f "$root/$c" && -d "$root/content" ]] && break 2
  done
  root="$(dirname "$root")"
done
[[ "$root" == "/" ]] && { echo "Hugo site root not found above $f" >&2; exit 2; }

fm="$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f' "$abs")"
draft=false; grep -qE '^draft:[[:space:]]*true' <<<"$fm" && draft=true
url="$(sed -nE 's/^url:[[:space:]]*["'\'']?([^"'\'']+)["'\'']?[[:space:]]*$/\1/p' <<<"$fm" | head -1)"

out="$(mktemp -d)"
flags=(--gc --minify -d "$out")
$draft && flags+=(--buildDrafts)
echo "SITE: $root"
echo "CMD:  hugo ${flags[*]}   (draft=$draft)"
log="$out.log"
start=$SECONDS
( cd "$root" && hugo "${flags[@]}" ) >"$log" 2>&1
rc=$?
echo "TIME: $((SECONDS-start))s  EXIT: $rc"

errs="$(grep -E 'ERROR|REF_NOT_FOUND' "$log" || true)"
[[ -n "$errs" ]] && { echo "--- errors ---"; echo "$errs" | head -40; }

page=""
if [[ -n "$url" ]]; then
  page="$out/${url#/}"; page="${page%/}/index.html"
else
  rel="${abs#"$root/content/"}"; rel="$(dirname "$rel")"
  page="$(find "$out" -path "*/$(basename "$rel")/index.html" | head -1)"
fi

rel_target="${abs#"$root/content/"}"
if [[ $rc -ne 0 || -n "$errs" ]]; then
  if grep -qF "$rel_target" <<<"$errs"; then
    echo "BUILD FAILED: errors in this article (log: $log)"; exit 1
  fi
  if [[ -n "$errs" ]]; then
    [[ -n "$page" && -f "$page" ]] && echo "PAGE: $page" || echo "PAGE: not confirmed (Hugo stopped before rendering it)"
    echo "SITE BUILD BROKEN by other files; no error names $rel_target. Fix or move those files, then re-run (log: $log)"; exit 3
  fi
  echo "BUILD FAILED: hugo exited $rc with no ERROR line (log: $log)"; exit 1
fi
if [[ -z "$page" || ! -f "$page" ]]; then
  echo "BUILD FAILED: page not rendered (expected ${page:-<unknown url>}). Check draft:, url:, and future dates."; exit 1
fi
echo "PAGE: $page"
echo "BUILD OK"

#!/usr/bin/env bash
# Print the absolute path of the last article created or adjusted in a Hugo blog repo.
#
# Usage: last-article.sh [repo-dir]
#   repo-dir defaults to $BLOG_ROOT, then the git root of the current directory
#   (when it has content/ or hugo/content/), then ~/Projects/websites/jeffbaileyblog.
#
# Only Hugo page bundles count as articles: content/**/index.md (any depth, so
# hugo/content/... matches too). README, notes, SKILL.md, prompts, and other
# Markdown never match.
#
# Order: 1) newest uncommitted or untracked article in the working tree (by mtime);
#        2) most recent commit touching an article; if that commit touched several,
#           the one with the most changed lines wins.
# Output (stdout): "<absolute path>\t<source>"  where source is "working-tree" or
#                  "commit <short-sha>". Exit 1 with a message on stderr if nothing found.
set -euo pipefail

has_content() { [ -d "$1/content" ] || [ -d "$1/hugo/content" ]; }

pick_root() {
  local cand
  for cand in "${1:-}" "${BLOG_ROOT:-}"; do
    [ -n "$cand" ] || continue
    cand=$(git -C "$cand" rev-parse --show-toplevel 2>/dev/null) || continue
    echo "$cand"; return 0
  done
  if cand=$(git rev-parse --show-toplevel 2>/dev/null) && has_content "$cand"; then
    echo "$cand"; return 0
  fi
  cand="$HOME/Projects/websites/jeffbaileyblog"
  if [ -d "$cand/.git" ]; then echo "$cand"; return 0; fi
  return 1
}

R=$(pick_root "${1:-}") || { echo "no blog repo found: pass a repo dir or set BLOG_ROOT" >&2; exit 1; }
SPEC=(':(glob)content/**/index.md' ':(glob)**/content/**/index.md')

# 1) Working tree: modified or untracked, newest mtime first.
files=()
while IFS= read -r -d '' f; do [ -f "$R/$f" ] && files+=("$R/$f"); done \
  < <(git -C "$R" ls-files -z -m -o --exclude-standard -- "${SPEC[@]}")
wt=""
if [ "${#files[@]}" -gt 0 ]; then wt=$(ls -t "${files[@]}" | head -1); fi
if [ -n "$wt" ]; then printf '%s\tworking-tree\n' "$wt"; exit 0; fi

# 2) Last commit that touched an article; pick its most-changed existing article.
sha=$(git -C "$R" log -1 --pretty=format:%H -- "${SPEC[@]}" 2>/dev/null || true)
if [ -n "$sha" ]; then
  best=$(git -C "$R" show --numstat --pretty=format: "$sha" -- "${SPEC[@]}" \
    | awk -F'\t' 'NF==3 { n=($1=="-"?0:$1)+($2=="-"?0:$2); print n "\t" $3 }' \
    | sort -t$'\t' -k1,1nr \
    | while IFS=$'\t' read -r _ f; do [ -f "$R/$f" ] && { echo "$R/$f"; break; }; done || true)
  if [ -n "$best" ]; then printf '%s\tcommit %s\n' "$best" "${sha:0:7}"; exit 0; fi
fi

echo "no article (content/**/index.md) found in working tree or history of $R" >&2
exit 1

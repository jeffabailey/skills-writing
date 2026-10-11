#!/usr/bin/env bash
# Build the jeffbaileyblog Hugo site into throwaway dirs and confirm one page renders.
#
# Shared by hugo-agents-compliance (authoring) and write-validate-article (the
# read-only gate, which calls it by sibling path). Keep one copy.
#
# Usage: verify-build.sh path/to/content/.../index.md
#
# - Always runs the production build (hugo --gc --minify), the one CI runs.
# - If the file has draft: true, ALSO runs with --buildDrafts, because the
#   production build skips drafts and would pass even if the draft has a
#   REF_NOT_FOUND or broken shortcode. The page is confirmed in that build.
# - Confirms <out>/<url>/index.html exists (without url:, finds it by bundle dir).
# - Splits failures: an ERROR that names this file is the article's fault;
#   ERRORs that never name it mean other files broke the site.
# - Never writes public/ in the repo: output goes to mktemp dirs.
#
# Exit: 0 BUILD OK | 1 BUILD FAILED for this article (an error names it, hugo
#       failed without an ERROR line, or its page did not render)
#       3 SITE BUILD BROKEN by other files only | 2 usage / site root not found
#       127 hugo missing
set -uo pipefail

case "${1:-}" in -h|--help) sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;; esac
f="${1:-}"
[[ -f "$f" ]] || { echo "usage: verify-build.sh path/to/index.md" >&2; exit 2; }
command -v hugo >/dev/null 2>&1 || { echo "TOOL MISSING: hugo (install: brew install hugo)"; exit 127; }

abs="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"
root="$(dirname "$abs")"
while [[ "$root" != "/" ]]; do
  for c in hugo.toml hugo.yaml hugo.json config.toml config.yaml config.json; do
    [[ -f "$root/$c" && -d "$root/content" ]] && break 2
  done
  root="$(dirname "$root")"
done
[[ "$root" == "/" ]] && { echo "ERROR: no Hugo site root (config + content/) above $f" >&2; exit 2; }

fm="$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f' "$abs")"
draft=false; grep -qE '^draft:[[:space:]]*["'\'']?true' <<<"$fm" && draft=true
url="$(sed -nE 's/^url:[[:space:]]*["'\'']?([^"'\'']+)["'\'']?[[:space:]]*$/\1/p' <<<"$fm" | head -1)"
rel_target="${abs#"$root/content/"}"
echo "site root: $root"
echo "target: content/$rel_target  draft=$draft  url=${url:-unset}"

all_errs=""
hugo_failed=0
run_build() { # $1 label, rest = extra flags; sets LAST_OUT
  local label="$1"; shift
  local out; out="$(mktemp -d)"
  local log="$out.log"
  local start=$SECONDS
  ( cd "$root" && hugo --gc --minify -d "$out" "$@" ) >"$log" 2>&1
  local rc=$?
  local errs; errs="$(grep -E 'ERROR|REF_NOT_FOUND' "$log" || true)"
  echo "[$label] cmd: hugo --gc --minify -d $out $*  exit=$rc  time=$((SECONDS-start))s  log=$log"
  [[ -n "$errs" ]] && { printf '%s\n' "$errs" | head -40 | sed 's/^/  /'; all_errs+="$errs"$'\n'; }
  [[ $rc -ne 0 ]] && hugo_failed=1
  LAST_OUT="$out"
}

run_build production
check_out="$LAST_OUT"
if $draft; then
  run_build drafts --buildDrafts
  check_out="$LAST_OUT"
fi

if [[ -n "$url" ]]; then
  page="$check_out/${url#/}"; page="${page%/}/index.html"
else
  page="$(find "$check_out" -path "*/$(basename "$(dirname "$abs")")/index.html" | head -1)"
fi

if [[ -n "$all_errs" ]] && grep -qF "$rel_target" <<<"$all_errs"; then
  echo "BUILD FAILED: errors in this article"; exit 1
fi
if [[ -n "$all_errs" ]]; then
  [[ -n "$page" && -f "$page" ]] && echo "PAGE: $page" || echo "PAGE: not confirmed (Hugo stopped before rendering it)"
  echo "SITE BUILD BROKEN by other files; no error names content/$rel_target. Fix or move those files, then re-run."
  exit 3
fi
if [[ $hugo_failed -ne 0 ]]; then
  echo "BUILD FAILED: hugo exited non-zero with no ERROR line (see log)"; exit 1
fi
if [[ -z "$page" || ! -f "$page" ]]; then
  echo "BUILD FAILED: page not rendered (expected ${page:-<unknown: no url and no matching bundle dir>}). Check draft:, url:, and future dates."
  exit 1
fi
echo "PAGE OK: $page"
echo "BUILD OK"

#!/usr/bin/env bash
# Build the jeffbaileyblog Hugo site to throwaway dirs and confirm a page renders.
#
# Usage: verify-build.sh path/to/content/.../index.md
#
# - Always runs the production build (hugo --gc --minify), the one CI runs.
# - If the file has draft: true, ALSO runs with --buildDrafts, because the
#   production build skips drafts (buildDrafts=false) and would pass even if the
#   draft has a REF_NOT_FOUND or broken shortcode.
# - Confirms <out>/<url>/index.html exists for the build that should render it.
# - Never writes public/ in the repo: output goes to mktemp dirs.
# Exit: 0 ok, 1 build failed or page missing, 3 tool missing.
set -u
f="${1:?usage: verify-build.sh path/to/index.md}"
if ! command -v hugo >/dev/null 2>&1; then
  echo "TOOL MISSING: hugo (install: brew install hugo)"; exit 3
fi
abs="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"
root="$(dirname "$abs")"
while [ "$root" != "/" ] && ! { [ -f "$root/config.toml" ] && [ -d "$root/content" ]; }; do
  root="$(dirname "$root")"
done
[ "$root" = "/" ] && { echo "ERROR: no Hugo site root (config.toml + content/) above $f"; exit 1; }

fm="$(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$abs")"
draft="$(printf '%s\n' "$fm" | sed -n 's/^draft:[[:space:]]*//p' | tr -d '"'"'" | head -1)"
url="$(printf '%s\n' "$fm" | sed -n 's/^url:[[:space:]]*//p' | tr -d '"'"'" | head -1)"
echo "site root: $root"
echo "target: ${abs#$root/}  draft=${draft:-unset}  url=${url:-unset}"

status=0
run_build() { # $1 label, rest = extra flags
  local label="$1"; shift
  local out; out="$(mktemp -d)"
  local log="$out.log"
  (cd "$root" && hugo --gc --minify -d "$out" "$@") >"$log" 2>&1
  local rc=$?
  local errs; errs="$(grep -E 'ERROR|REF_NOT_FOUND' "$log")"
  echo "[$label] exit=$rc  log=$log  out=$out"
  [ -n "$errs" ] && printf '%s\n' "$errs" | sed 's/^/  /'
  [ $rc -ne 0 ] && status=1
  LAST_OUT="$out"
}

run_build production
prod_out="$LAST_OUT"
check_out="$prod_out"
if [ "${draft:-false}" = "true" ]; then
  run_build drafts --buildDrafts
  check_out="$LAST_OUT"
fi

if [ -n "${url:-}" ]; then
  page="$check_out/${url#/}"; page="${page%/}/index.html"
  if [ -f "$page" ]; then echo "PAGE OK: $page"
  else echo "PAGE MISSING: $page"; status=1; fi
else
  echo "WARN: no url in front matter; locate the page with: hugo list all | grep '${abs#$root/}'"
fi
[ $status -eq 0 ] && echo "BUILD OK" || echo "BUILD FAILED"
exit $status

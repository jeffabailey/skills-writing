#!/usr/bin/env bash
# Lint one Markdown file with markdownlint-cli2 and the user's config.
#
# Usage: lint.sh <file.md> [--config <path>]
#
# Exit codes:
#   0   lint passed
#   1   lint ran and found problems
#   2   usage error (bad args, file or config not found)
#   127 tool missing (neither markdownlint-cli2 nor npx is available)
#
# Never falls back to `markdownlint` (markdownlint-cli v1): it treats the
# cli2 file's top-level "config" key as an unknown rule, silently drops every
# setting, and lints with defaults (MD013 at 80 cols, MD052, MD004 "consistent").
set -u

CLI2_VERSION="0.18.1"
file=""
config=""

while [ $# -gt 0 ]; do
  case "$1" in
    --config) config="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
    *) if [ -z "$file" ]; then file="$1"; shift; else echo "USAGE ERROR: unexpected argument: $1" >&2; exit 2; fi ;;
  esac
done

if [ -z "$file" ]; then echo "USAGE ERROR: no file given. Usage: lint.sh <file.md> [--config <path>]" >&2; exit 2; fi
if [ ! -f "$file" ]; then echo "USAGE ERROR: file not found: $file" >&2; exit 2; fi

# --- Tool preflight ---------------------------------------------------------
if command -v markdownlint-cli2 >/dev/null 2>&1; then
  tool=(markdownlint-cli2); tool_desc="markdownlint-cli2 ($(command -v markdownlint-cli2))"
elif command -v npx >/dev/null 2>&1; then
  tool=(npx -y "markdownlint-cli2@${CLI2_VERSION}"); tool_desc="npx -y markdownlint-cli2@${CLI2_VERSION} (not on PATH; using npx)"
else
  echo "TOOL MISSING: markdownlint-cli2 is not installed and npx is not available."
  if command -v markdownlint >/dev/null 2>&1; then
    echo "Found markdownlint (markdownlint-cli v1) at $(command -v markdownlint); NOT using it because it ignores the cli2 config."
  fi
  echo "Install one of:"
  echo "  brew install markdownlint-cli2"
  echo "  npm install -g markdownlint-cli2@${CLI2_VERSION}"
  echo "  (or install Node.js so 'npx -y markdownlint-cli2@${CLI2_VERSION}' works)"
  echo "No lint was run. This is not a lint failure."
  exit 127
fi

# --- Config discovery -------------------------------------------------------
# Order: explicit --config, then the nearest .markdownlint-cli2.{jsonc,yaml}
# walking up from the file (stopping at the git root), then ~/Shell.
config_src="explicit --config"
if [ -z "$config" ]; then
  dir="$(cd "$(dirname "$file")" && pwd -P)"
  stop="$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null || echo /)"
  while :; do
    for name in .markdownlint-cli2.jsonc .markdownlint-cli2.yaml; do
      if [ -f "$dir/$name" ]; then config="$dir/$name"; config_src="project (nearest to file)"; break 2; fi
    done
    [ "$dir" = "$stop" ] || [ "$dir" = "/" ] && break
    dir="$(dirname "$dir")"
  done
fi
if [ -z "$config" ] && [ -f "$HOME/Shell/.markdownlint-cli2.jsonc" ]; then
  config="$HOME/Shell/.markdownlint-cli2.jsonc"; config_src="user default (~/Shell)"
fi
if [ -n "$config" ] && [ ! -f "$config" ]; then echo "USAGE ERROR: config not found: $config" >&2; exit 2; fi

echo "TOOL:   $tool_desc"
if [ -n "$config" ]; then
  resolved="$config"; [ -L "$config" ] && resolved="$config -> $(readlink "$config")"
  echo "CONFIG: $resolved [$config_src]"
else
  echo "CONFIG: none found; markdownlint-cli2 built-in defaults apply (expect MD013 at 80 cols)"
fi
echo "FILE:   $file"
echo "----"

# --- Run --------------------------------------------------------------------
args=()
if [ -n "$config" ]; then
  config="$(cd "$(dirname "$config")" && pwd -P)/$(basename "$config")"
  args+=(--config "$config")
fi
# Run from the file's directory with a literal (":"-prefixed) basename so
# odd characters in the name are not treated as globs and paths print short.
out="$(cd "$(dirname "$file")" && "${tool[@]}" "${args[@]}" ":$(basename "$file")" 2>&1)"; rc=$?
printf '%s\n' "$out"
echo "----"

findings="$(printf '%s\n' "$out" | grep -E ':[0-9]+(:[0-9]+)? MD[0-9]{3}/' || true)"
if [ "$rc" -eq 0 ]; then
  echo "RESULT: PASS (0 findings)"
  exit 0
fi
if [ -z "$findings" ]; then
  echo "RESULT: TOOL ERROR (exit $rc, no rule findings parsed). Read the output above; this is not a lint result."
  exit 2
fi

count="$(printf '%s\n' "$findings" | wc -l | tr -d ' ')"
echo "RESULT: FAIL ($count findings)"
echo "BY RULE:"
printf '%s\n' "$findings" | sed -E 's/.*:[0-9]+(:[0-9]+)? (MD[0-9]{3}\/[a-z0-9-]+).*/\2/' | sort | uniq -c | sort -rn
if printf '%s\n' "$findings" | grep -qE ' MD(013|052)/'; then
  if [ -n "$config" ] && grep -qE '"MD052"[[:space:]]*:[[:space:]]*false|"line_length"[[:space:]]*:[[:space:]]*[0-9]{4}' "$config"; then
    echo "WARNING: MD013/MD052 fired, but the config in use disables MD052 or raises MD013 well past 80 cols."
    echo "         The config was NOT applied. Treat these results as unreliable, not as real issues."
  else
    echo "NOTE: MD013/MD052 fired. The user's ~/Shell config raises MD013 to 1200 cols and disables MD052;"
    echo "      if that config was expected here, it was not applied (see CONFIG above)."
  fi
fi
exit 1

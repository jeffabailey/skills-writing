#!/usr/bin/env bash
# Run a minimal repro against the buggy tree and a fixed copy, and report
# whether it is verified: it must FAIL (non-zero exit) on the buggy tree and
# PASS (exit 0) on the fixed copy.
#
# Usage:
#   verify_repro.sh <buggy_dir> <fixed_dir> -- <command...>
#
# The command runs with each directory as its working directory, so write the
# repro to import or call code relative to that directory (or take the
# directory from $REPRO_ROOT, which is set for each run).
#
# Example:
#   verify_repro.sh ./sandbox ./sandbox-fixed -- python3 -I /path/to/repro.py
#
# Exit codes: 0 verified, 1 not verified, 2 usage error.
set -u

if [ $# -lt 4 ] || [ "$3" != "--" ]; then
  echo "usage: $0 <buggy_dir> <fixed_dir> -- <command...>" >&2
  exit 2
fi

buggy=$1
fixed=$2
shift 3

for d in "$buggy" "$fixed"; do
  if [ ! -d "$d" ]; then
    echo "error: not a directory: $d" >&2
    exit 2
  fi
done

if [ "$(cd "$buggy" && pwd -P)" = "$(cd "$fixed" && pwd -P)" ]; then
  echo "error: buggy and fixed directories are the same; apply the fix to a copy" >&2
  exit 2
fi

run() {
  local label=$1 dir=$2
  echo "=== $label: $dir"
  echo "\$ ${*:3}"
  (cd "$dir" && REPRO_ROOT=$(pwd -P) "${@:3}") 2>&1
  local rc=$?
  echo "--- exit $rc"
  return $rc
}

run buggy "$buggy" "$@"
buggy_rc=$?
echo
run fixed "$fixed" "$@"
fixed_rc=$?
echo

if [ "$buggy_rc" -ne 0 ] && [ "$fixed_rc" -eq 0 ]; then
  echo "VERIFIED: repro fails on buggy (exit $buggy_rc) and passes on fixed (exit 0)"
  exit 0
fi

if [ "$buggy_rc" -eq 0 ]; then
  echo "NOT VERIFIED: repro passes on the buggy tree, so it does not reproduce the bug"
else
  echo "NOT VERIFIED: repro still fails on the fixed copy (exit $fixed_rc), so the fix is incomplete or the repro tests something else"
fi
exit 1

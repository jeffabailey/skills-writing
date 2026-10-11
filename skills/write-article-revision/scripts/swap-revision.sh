#!/usr/bin/env bash
# Swap a Hugo bundle's index.revised.md in as index.md for validation, then restore.
#   swap-revision.sh in     <bundle-dir>  back up index.md outside the bundle, copy index.revised.md -> index.md
#   swap-revision.sh out    <bundle-dir>  restore the original index.md (fixes made meanwhile go to index.revised.md)
#   swap-revision.sh accept <bundle-dir>  make the revision permanent: index.revised.md -> index.md, drop the backup
# The backup lives under ${TMPDIR:-/tmp}/swap-revision/, never in the bundle, because Hugo
# copies every non-page file in a bundle into the built site.
set -euo pipefail
mode=${1:-}; dir=${2:-}
[[ -n $mode && -d $dir ]] || { echo "usage: $0 in|out|accept <bundle-dir>" >&2; exit 2; }
dir=$(cd "$dir" && pwd -P)
key=$(printf '%s' "$dir" | shasum | cut -c1-16)
bak="${TMPDIR:-/tmp}/swap-revision/$key/index.md"
cd "$dir"
case $mode in
  in)
    [[ -f index.revised.md ]] || { echo "no index.revised.md in $dir" >&2; exit 1; }
    [[ ! -e $bak ]] || { echo "backup exists ($bak): already swapped in? run 'out' first" >&2; exit 1; }
    mkdir -p "$(dirname "$bak")"
    cp -p index.md "$bak"
    cp index.revised.md index.md
    echo "swapped in: index.md is the revision; original backed up to $bak" ;;
  out)
    [[ -f $bak ]] || { echo "nothing to restore (no backup at $bak)" >&2; exit 1; }
    cmp -s index.md index.revised.md || cp index.md index.revised.md
    cp -p "$bak" index.md && rm "$bak"
    echo "restored original index.md; revision (with any fixes) is in index.revised.md" ;;
  accept)
    if [[ -f $bak ]]; then cmp -s index.md index.revised.md || cp index.md index.revised.md; rm "$bak"; fi
    mv index.revised.md index.md
    echo "accepted: index.md is now the revision" ;;
  *) echo "unknown mode: $mode" >&2; exit 2 ;;
esac

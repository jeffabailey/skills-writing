#!/usr/bin/env bash
# Download Canva cover exports, compress them, and check their size.
#
# Reads one cover per line on stdin: "<output.png> <download_url>".
# For each, downloads the URL over the output file, quantizes it in place with
# pngquant (skipped, keeping the Canva file, if pngquant is missing or would not
# shrink it), crops to 1200x630 if the export is another size, and prints
# "<output.png> <width>x<height> <bytes>". Exits 1 if any download failed.
#
# Usage: printf '%s %s\n' bundle/slug.png 'https://...' | bash scripts/fetch-covers.sh
set -uo pipefail

have_pngquant=1
command -v pngquant >/dev/null || { have_pngquant=0; echo "pngquant not installed (brew install pngquant); keeping Canva files" >&2; }

failed=0
while read -r out url; do
  [ -z "${out:-}" ] && continue
  if ! curl -fsSL -o "$out" "$url"; then
    echo "FAIL: download for $out (export URLs expire after about an hour)" >&2
    failed=1
    continue
  fi
  if [ "$have_pngquant" -eq 1 ]; then
    pngquant --quality=70-90 --strip --speed 1 --skip-if-larger -f --ext .png "$out"
    rc=$?
    # 98 and 99 mean pngquant skipped the file; the Canva file is kept.
    if [ "$rc" -ne 0 ] && [ "$rc" -ne 98 ] && [ "$rc" -ne 99 ]; then
      echo "WARN: pngquant exited $rc for $out; keeping the Canva file" >&2
    fi
  fi
  size="$(magick identify -format '%wx%h' "$out")"
  if [ "$size" != "1200x630" ]; then
    magick "$out" -resize '1200x630^' -gravity center -extent 1200x630 "$out"
  fi
  magick identify -format "$out %wx%h %b\n" "$out"
done

exit "$failed"

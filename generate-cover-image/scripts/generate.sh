#!/usr/bin/env bash
# Generate a 1200x630 PNG cover image from the bundled prompt plus an input text.
#
# Usage: generate.sh <input-text-file> <output.png>
#
# Requires OPENAI_API_KEY, curl, jq, python3, and ImageMagick (magick).
# The model returns 1536x1024; the image is scaled to 1200 wide and
# center-cropped to exactly 1200x630.
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "usage: $0 <input-text-file> <output.png>" >&2
  exit 2
fi

input=$1
output=$2
here=$(cd "$(dirname "$0")/.." && pwd)
prompt_file="$here/references/cover-prompt.md"
model=${COVER_IMAGE_MODEL:-gpt-image-1}

[ -n "${OPENAI_API_KEY:-}" ] || { echo "OPENAI_API_KEY is not set" >&2; exit 3; }
[ -s "$input" ] || { echo "input text file is empty or missing: $input" >&2; exit 2; }
for tool in curl jq python3 magick; do
  command -v "$tool" >/dev/null || { echo "missing required tool: $tool" >&2; exit 3; }
done

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

cat "$prompt_file" "$input" > "$tmp/prompt.txt"

jq -n --arg model "$model" --rawfile prompt "$tmp/prompt.txt" \
  '{model: $model, prompt: $prompt, size: "1536x1024", quality: "high", n: 1}' \
  > "$tmp/request.json"

http_status=$(curl -sS -o "$tmp/response.json" -w '%{http_code}' \
  https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data @"$tmp/request.json")

if [ "$http_status" != "200" ]; then
  echo "image API returned HTTP $http_status:" >&2
  jq -r '.error.message // .' "$tmp/response.json" >&2 || cat "$tmp/response.json" >&2
  exit 4
fi

jq -r '.data[0].b64_json' "$tmp/response.json" > "$tmp/image.b64"
python3 -c 'import base64,sys; sys.stdout.buffer.write(base64.b64decode(open(sys.argv[1]).read()))' \
  "$tmp/image.b64" > "$tmp/raw.png"

mkdir -p "$(dirname "$output")"
magick "$tmp/raw.png" -resize '1200x630^' -gravity center -extent 1200x630 -strip "PNG24:$output"

size=$(magick identify -format '%wx%h' "$output")
[ "$size" = "1200x630" ] || { echo "unexpected output size: $size" >&2; exit 5; }
echo "$output ($size)"

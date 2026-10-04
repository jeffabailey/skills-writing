# Canva Brand Template: jeffbaileyblog feature image

jeffbaileyblog covers are the generated artwork composited into a new design made from a Canva brand template that adds the title and the blog logo. Use the Canva MCP tools (`mcp__claude_ai_Canva__*`).

The brand template is the source and stays untouched. Every cover is a new design created from it, named after the article slug, and filed in the destination folder.

| Item | Value |
|------|-------|
| Brand kit | `kAEqeQflWyc` |
| Brand template | `jbb-feature-image-template`, ID `EAHXEEDJKs0` |
| Destination folder | `FAFgCl26Zkg` |
| Page size | 1200x630 |

The template has no autofill fields (`get-brand-template-dataset` returns `{}`), so fill it with `edit-design`, not `autofill-design`.

## Template layout

Read the locator IDs from the design each time; do not hardcode them. Copies of the template have kept these so far:

* **Background**: the page background image (`isMediaReplaceable: true`). Its locator is the page locator, e.g. `PBkT0q69sJJFq6lW`.
* **Title**: a text element with three regions, all bold, 130.659 px, centered:
  * `"Topic "` in white `#ffffff` (lead)
  * `"key point"` in yellow `#ffde59` (highlight)
  * `"?"` in white (trail)
* **Logo**: a small image rect above the byline. Leave it alone.
* **Byline**: `"Jeff Bailey’s Blog "`. Leave it alone.

## Splitting the title

Use the short cover title (see SKILL.md step 5), not a long front matter `title:`. Pick the highlight: the subject the article is about, usually its last noun phrase (`What Are ` + `AI Evals` + `?`; `Fundamentals of ` + `Containerization` + empty; `Learn ` + `Nushell` + empty). Everything before it is the lead, everything after it (including punctuation) is the trail. End the lead with a line break instead of a space, so the lead and the highlight sit on separate lines (`"Learn\n"` + `Tmux`).

## Steps

1. **Create the design.** `create-design-from-brand-template` with `brand_template_id: EAHXEEDJKs0`. Keep the returned design ID (`D...`).

2. **Read it.** `read-design` with `open_transaction: true` and `filter.fields: ["design_content", "thumbnails"]`. Take the `transaction_id`, the page `id` and `locator_id`, the title element's `locator_id` (the text element whose regions are `Topic `, `key point`, `?`), the logo rect's `locator_id`, and the byline's `locator_id`.

3. **Upload the shade.** The artwork is already a Canva media ID from `generate-image` (SKILL.md step 3), so it needs no upload. Upload the shade overlay from `<skill-dir>/assets/cover-shade.png`: call `create-upload-url`, then send the PNG's raw bytes in one POST:

   ```bash
   curl -sS -X POST -H "Content-Type: application/octet-stream" \
     --data-binary @<skill-dir>/assets/cover-shade.png '<upload_url>'
   ```

   The response is `{"mediaId":"M..."}`; keep it. Each URL works once; get a new one to retry. See [Shading the background](#shading-the-background).

4. **Edit.** One `edit-design` call with `finalize: "keep_open"`, `page_index: 1`, and these operations:

   * `update_fill` on the page locator, `asset_type: image`, `asset_id: <artwork mediaId>`, `alt_text: <cover alt text>`
   * `find_and_replace_text` on the title locator: `"Topic "` → lead (ending in `\n`)
   * `find_and_replace_text` on the title locator: `"key point"` → highlight
   * `find_and_replace_text` on the title locator: `"?"` → trail (an empty string removes the region)
   * `update_title` → the article slug
   * `insert_fill` with `page_id: <page id>`, `asset_type: image`, `asset_id: <shade mediaId>`, `alt_text: ""`, `top: 0`, `left: 0`, `width: 1200`, `height: 630`
   * `layer_element` `position: front` on the logo, then the byline, then the title, so all three sit above the shade

   Replace the regions in that order, so a lead or highlight containing `?` is not hit by the last replacement.

5. **Check.** Confirm in the returned `document` that the background `mediaId` is the generated artwork, the shade is a full-page image element listed before the logo, byline, and title (earlier elements draw underneath), and the title regions read lead, highlight, trail. In the thumbnail, the artwork should be clearly darker with black edges, and the title, logo, and byline at full brightness. Draft thumbnails often draw text twice, slightly offset; trust the `document` for text and the thumbnail for layout. If the title runs past three lines or touches the logo, apply `format_text` with a smaller `font_size` to the title locator and check again.

6. **Commit.** Show the user the thumbnail and the draft's edit URL, and commit with `edit-design` `finalize: "commit"` once they approve (or straight away if they said to skip review). To abandon, use `finalize: "cancel"`.

7. **File it.** `move-item-to-folder` with the design ID and `to_folder_id: FAFgCl26Zkg`.

8. **Export and compress.** `export-design` with `format: {type: png, width: 1200, height: 630}`. Keep Canva's default lossless export; do not set `lossless: false`, because `pngquant` compresses better from the lossless source and Canva's lossy pass only adds a second round of loss. Download the returned URL over the bundle's `<slug>.png`, quantize it in place, and check the size:

   ```bash
   curl -sSL -o <bundle>/<slug>.png '<download_url>'
   pngquant --quality=70-90 --strip --speed 1 --skip-if-larger -f --ext .png <bundle>/<slug>.png
   magick identify -format '%wx%h %b\n' <bundle>/<slug>.png   # 1200x630, about 100 KB
   ```

   `pngquant` took the Learn Tmux cover from 592 KB to 88 KB with no visible banding. It exits 98 or 99 when it skips the file (already smaller, or below the quality floor); that is fine, keep the Canva file. If `pngquant` is not installed, keep the Canva file and tell the user (`brew install pngquant`). Look at the final PNG for banding in the dark gradients; if it shows, re-export and use `--quality=80-95`.

   If the export is not 1200x630, crop it with `magick <in> -resize '1200x630^' -gravity center -extent 1200x630 <out>`.

## Shading the background

The covers use the background artwork darkened, with a strong vignette, so the title stands out. In the Canva editor that is the image's Adjust settings **Brightness -55** and **Vignette 100**. The Canva connector cannot set image adjustments (`edit-design` has no adjust operation, and `read-design` does not report them), so the skill approximates them with a shade layer instead.

`assets/cover-shade.png` is a 1200x630 black PNG whose opacity is 45% at the center and rises smoothly to about 85% at the corners. Placed over the background and under the text, it gives roughly the same look and stays editable in Canva: select it to change its transparency or delete it. If the user would rather match the exact Canva adjustments, they can delete the shade and apply Brightness -55 and Vignette 100 to the background by hand, then export again.

To rebuild the asset with a different strength, change the base (`0.45`) and the edge increase (`0.4`):

```bash
magick -size 1200x630 xc: -fx 'dd=hypot((i-w/2)/(w/2),(j-h/2)/(h/2))/1.4142; 0.45+0.4*dd*dd*(3-2*dd)' /tmp/alpha.png
magick -size 1200x630 xc:black /tmp/alpha.png -alpha off -compose CopyOpacity -composite -strip PNG32:assets/cover-shade.png
```

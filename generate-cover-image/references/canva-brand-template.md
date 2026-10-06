# Canva Brand Template: jeffbaileyblog feature image

jeffbaileyblog covers are the generated artwork composited into a new design made from a Canva brand template that adds the title and the blog logo. Use the Canva MCP tools (`mcp__claude_ai_Canva__*`).

The brand template is the source and stays untouched. Each article has one cover design, named after the article slug and filed in the destination folder. If that design already exists, overwrite it in place; create a new design from the template only when there is none.

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

1. **Find or create the design.** `list-folder-items` with `folder_id: FAFgCl26Zkg`, `item_types: ["design"]`, and follow `continuation` until a design titled exactly `<slug>` turns up or the pages run out.

   * **Found:** keep its design ID (`D...`) and overwrite it. If more than one design has the slug title, use the most recently modified one and tell the user about the others.
   * **Not found:** `create-design-from-brand-template` with `brand_template_id: EAHXEEDJKs0`. Keep the returned design ID.

2. **Read it.** `read-design` with `open_transaction: true` and `filter.fields: ["design_content", "thumbnails"]`. Take the `transaction_id`, the page `locator_id`, and the title element's `locator_id`. In a new design the title is the text element whose regions are `Topic `, `key point`, `?`. In an existing cover it is the large bold text element whose regions hold the old lead, highlight, and trail; note each region's current text.

   An existing cover made before the skill stopped shading the background has a full-page image element above the background, under the logo, byline, and title. Note its `locator_id` so the edit can delete it.

3. **Edit.** One `edit-design` call with `finalize: "keep_open"`, `page_index: 1`, and these operations:

   * `update_fill` on the page locator, `asset_type: image`, `asset_id: <artwork mediaId>`, `alt_text: <cover alt text>`
   * `find_and_replace_text` on the title locator: `"Topic "` → lead (ending in `\n`)
   * `find_and_replace_text` on the title locator: `"key point"` → highlight
   * `find_and_replace_text` on the title locator: `"?"` → trail (an empty string removes the region)
   * `update_title` → the article slug

   Replace the regions in that order, so a lead or highlight containing `?` is not hit by the last replacement.

   For an existing cover, the same operations apply with these changes:

   * Find each region's current text instead of the template placeholders (`"Learn\n"` → new lead, `"Tmux"` → new highlight, old trail → new trail). Skip a region whose text is not changing. If an old region's text also appears in another region, use `replace_text` on the title locator with the full new title, then `format_text` the highlight back to `#ffde59`.
   * Leave out `update_title`; the design already has the slug.
   * Add `delete_element` on the old shade element, if step 2 found one.

4. **Check.** Confirm in the returned `document` that the background `mediaId` is the generated artwork and the title regions read lead, highlight, trail. Draft thumbnails often draw text twice, slightly offset; trust the `document` for text and the thumbnail for layout. If the title runs past three lines or touches the logo, apply `format_text` with a smaller `font_size` to the title locator and check again.

5. **Commit.** Show the user the thumbnail and the draft's edit URL, and commit with `edit-design` `finalize: "commit"` once they approve (or straight away if they said to skip review). When overwriting, say so: the commit replaces the existing cover and cannot be undone through the connector (Canva's version history in the editor still has the old one). To abandon, use `finalize: "cancel"`.

6. **File it.** For a new design, `move-item-to-folder` with the design ID and `to_folder_id: FAFgCl26Zkg`. An existing cover is already there; skip this step.

7. **Export and compress.** `export-design` with `format: {type: png, width: 1200, height: 630}`. Keep Canva's default lossless export; do not set `lossless: false`, because `pngquant` compresses better from the lossless source and Canva's lossy pass only adds a second round of loss. Download the returned URL over the bundle's `<slug>.png`, quantize it in place, and check the size:

   ```bash
   curl -sSL -o <bundle>/<slug>.png '<download_url>'
   pngquant --quality=70-90 --strip --speed 1 --skip-if-larger -f --ext .png <bundle>/<slug>.png
   magick identify -format '%wx%h %b\n' <bundle>/<slug>.png   # 1200x630, about 100 KB
   ```

   `pngquant` took the Learn Tmux cover from 592 KB to 88 KB with no visible banding. It exits 98 or 99 when it skips the file (already smaller, or below the quality floor); that is fine, keep the Canva file. If `pngquant` is not installed, keep the Canva file and tell the user (`brew install pngquant`). Look at the final PNG for banding in the dark gradients; if it shows, re-export and use `--quality=80-95`.

   If the export is not 1200x630, crop it with `magick <in> -resize '1200x630^' -gravity center -extent 1200x630 <out>`.

## Background adjustments

Do not darken the background or add a vignette. The Canva connector cannot set image adjustments (`edit-design` has no adjust operation), and approximating them with a black overlay layer makes the artwork look muddy. Use the generated artwork as is.

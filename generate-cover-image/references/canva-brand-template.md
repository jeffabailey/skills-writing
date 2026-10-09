# Canva Brand Template: jeffbaileyblog feature image

jeffbaileyblog covers are the generated artwork composited into a new design made from a Canva brand template that adds the title and the blog logo. Use the Canva MCP tools (`mcp__claude_ai_Canva__*`).

The brand template is the source and stays untouched. Each article has one cover design, named after the article (its design name, see SKILL.md) and filed in the destination folder. If that design already exists, overwrite it in place; create a new design from the template only when there is none.

| Item | Value |
|------|-------|
| Brand kit | `kAEqeQflWyc` |
| Brand template | `jbb-feature-image-template`, ID `EAHXEEDJKs0` |
| Destination folder | `FAFgCl26Zkg` |
| Page size | 1200x630 |

The template has no autofill fields (`get-brand-template-dataset` returns `{}`), so fill it with `edit-design`, not `autofill-design`. Autofill was considered and rejected: an autofill text field replaces a whole element's text, so the two-color title (white lead, yellow highlight in one element) would have to become two elements with a new layout, the background is a page fill rather than a taggable image element, and the saving is only about two calls per cover.

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

## Sizing the title

Set the font size in the first edit, not after looking at the result. The font renders in capitals, and the 1087 px title box holds about 12 characters per line at the template's 130.659 px. Take the longest line of the title (lead, or highlight plus trail), counting spaces, and use:

`font_size = min(130, floor(1560 / longest line))`

So 12 characters keep the template size, `1000 Life Giving` (16) gets 97, and `Software Engineering` (20) gets 78. Keep it at 72 or more: if a line would need less, break it at a space into two lines. Use at most three lines in total, and at most 100 px when there are three, so the title stays clear of the logo. Skip `format_text` when the result is 130.

## Steps

1. **Find or create the design.** `list-folder-items` with `folder_id: FAFgCl26Zkg`, `item_types: ["design"]`, and follow `continuation` until a design titled exactly `<design name>` turns up or the pages run out. For more than one cover, list the folder once, keep a title-to-ID map for the whole run, and add each new design to it; do not list or search per cover.

   * **Found:** keep its design ID (`D...`) and overwrite it. If more than one design has that title, use the most recently modified one and tell the user about the others.
   * **Not found:** `create-design-from-brand-template` with `brand_template_id: EAHXEEDJKs0`. Keep the returned design ID.

2. **Read it.** `read-design` with `open_transaction: true` and `filter.fields: ["design_content", "thumbnails"]`. For a new design, leave out `"thumbnails"`: the before state is always the template placeholder, and the edit returns the after thumbnail. Take the `transaction_id`, the page `locator_id`, and the title element's `locator_id`. In a new design the title is the text element whose regions are `Topic `, `key point`, `?`. In an existing cover it is the large bold text element whose regions hold the old lead, highlight, and trail; note each region's current text.

   An existing cover made before the skill stopped shading the background has a full-page image element above the background, under the logo, byline, and title. Note its `locator_id` so the edit can delete it.

3. **Edit.** One `edit-design` call with `finalize: "keep_open"`, `page_index: 1`, and these operations:

   * `update_fill` on the page locator, `asset_type: image`, `asset_id: <artwork mediaId>`, `alt_text: <cover alt text>`
   * `find_and_replace_text` on the title locator: `"Topic "` → lead (ending in `\n`)
   * `find_and_replace_text` on the title locator: `"key point"` → highlight
   * `find_and_replace_text` on the title locator: `"?"` → trail (an empty string removes the region)
   * `format_text` on the title locator with the `font_size` from [Sizing the title](#sizing-the-title), unless it is 130
   * `update_title` → the design name

   Replace the regions in that order, so a lead or highlight containing `?` is not hit by the last replacement.

   For an existing cover, the same operations apply with these changes:

   * Find each region's current text instead of the template placeholders (`"Learn\n"` → new lead, `"Tmux"` → new highlight, old trail → new trail). Skip a region whose text is not changing. If an old region's text also appears in another region, use `replace_text` on the title locator with the full new title, then `format_text` the highlight back to `#ffde59`.
   * Leave out `update_title`; the design already has its name.
   * Add `delete_element` on the old shade element, if step 2 found one.

4. **Check.** Confirm in the returned `document` that the background `mediaId` is the generated artwork and the title regions read lead, highlight, trail. Draft thumbnails often draw text twice, slightly offset; trust the `document` for text and the thumbnail for layout. The size set in step 3 should already fit. Only if the title still runs past three lines or touches the logo, apply `format_text` with a smaller `font_size` and check again, and note the title so the sizing rule can be tuned.

5. **Commit.** Show the user the thumbnail and the draft's edit URL, and commit with `edit-design` `finalize: "commit"` once they approve (or straight away if they said to skip review). When overwriting, say so: the commit replaces the existing cover and cannot be undone through the connector (Canva's version history in the editor still has the old one). To abandon, use `finalize: "cancel"`.

6. **File it.** For a new design, `move-item-to-folder` with the design ID and `to_folder_id: FAFgCl26Zkg`. An existing cover is already there; skip this step.

7. **Export and compress.** `export-design` with `format: {type: png, width: 1200, height: 630}`. Keep Canva's default lossless export; do not set `lossless: false`, because `pngquant` compresses better from the lossless source and Canva's lossy pass only adds a second round of loss. Download the returned URL over the bundle's `<slug>.png`, quantize it in place, and check the size:

   ```bash
   printf '%s %s\n' <bundle>/<slug>.png '<download_url>' | bash scripts/fetch-covers.sh
   ```

   `scripts/fetch-covers.sh` downloads each URL, runs `pngquant --quality=70-90 --strip --speed 1 --skip-if-larger`, crops to 1200x630 if needed, and prints the size (about 100 to 300 KB). Feed it one line per cover to fetch a whole batch in one call. Export URLs expire after about an hour, so fetch each batch soon after exporting it.

   `pngquant` took the Learn Tmux cover from 592 KB to 88 KB with no visible banding. It exits 98 or 99 when it skips the file (already smaller, or below the quality floor); that is fine, keep the Canva file. If `pngquant` is not installed, the script keeps the Canva file and says so (`brew install pngquant`). Look at the final PNG for banding in the dark gradients; if it shows, re-export and use `--quality=80-95`.

## Background adjustments

Do not darken the background or add a vignette. The Canva connector cannot set image adjustments (`edit-design` has no adjust operation), and approximating them with a black overlay layer makes the artwork look muddy. Use the generated artwork as is.

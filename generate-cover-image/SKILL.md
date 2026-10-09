---
name: generate-cover-image
description: Generates a 1200x630 PNG cover image for an article from its meaning, using the bundled cover prompt (dark, futuristic, human-and-system artwork with no text). For jeffbaileyblog it overwrites the article's existing Canva cover design, or creates one from the jbb-feature-image-template brand template (never editing the template itself), swaps in the artwork as the background, sets the title, names the design after the article slug, files it in the blog covers folder, and exports it next to the article with the Hugo cover front matter set. Also covers category term bundles, and has a batch mode for many covers at once. Use when the user says /write:cover, asks for a cover image, hero image, or social/OG image for an article, or when write-article finishes a jeffbaileyblog draft.
---

# Generate Cover Image

Create a cover image whose composition comes from what the article means, not from its keywords. The prompt is bundled in `references/cover-prompt.md`; it ends with `Use the text below as the central inspiration:` and a `---` line, and the inspiration text is appended after it.

## Inputs

- **Article**: a Markdown file path, or the draft in the conversation.
- **Output path**: for jeffbaileyblog, `<page bundle>/<slug>.png` next to the bundle's `index.md` (the slug is the front matter `slug:`). Elsewhere, ask.
- **Category term bundles** (jeffbaileyblog `hugo/content/categories/<slug>/_index.md`) take covers too. The slug is the directory name, and the output is `<slug>.png` beside `_index.md`. Read the bundle's `title` and `description` and the titles of the category's posts for the inspiration text. The cover title is the category `title`.

For jeffbaileyblog, the generated artwork is only the background. The published `<slug>.png` is the export of a Canva design with the title on it, so the artwork stays in Canva as a media ID and never goes into the bundle.

Every jeffbaileyblog cover is its own Canva design:

| Item | Value |
|------|-------|
| Brand template (source, read-only) | `jbb-feature-image-template`, ID `EAHXEEDJKs0`, in brand kit `kAEqeQflWyc` |
| Destination folder | `FAFgCl26Zkg` |
| Design name | the front matter `slug:`, e.g. `learn-nushell`; for a category, `category-<slug>`, e.g. `category-laws`, so it never collides with an article cover |

Never open, edit, or publish the brand template. Edits go to the article's cover design: the existing one with its design name, or a new one from `create-design-from-brand-template`.

## Workflow

1. **Read the article.** Take its title, description, and body.

2. **Write the inspiration text.** In 80 to 150 words of plain prose, state the article's core idea, its emotional tone, and the metaphors, contrasts, or tensions it uses. Describe meaning, not layout. Leave out product names, logos, commands, and quoted code, because the prompt forbids text in the image and names pull models toward literal renderings. Show it to the user only if they asked to review prompts.

3. **Generate with the Canva connector.** Join the prompt and the inspiration text (`cat references/cover-prompt.md <inspiration.txt>`) and send the result to Canva `generate-image` with `aspectRatio: LANDSCAPE_2_1`. Poll `get-generate-image-job` with the returned `jobId` until it returns `SUCCESS`. The result is a Canva media ID (`M...`); it is the background asset in step 5. Canva crops it to fill the 1200x630 page.

   Do not call the OpenAI Images API or any other image service. If the Canva tools are not connected or the job fails, write the joined prompt to `<output>.prompt.txt`, tell the user why, and stop. Never draw a placeholder or a substitute graphic.

4. **Look at the artwork.** Read the preview `get-generate-image-job` returns. Regenerate once with a sharper inspiration text if it contains any letters, numbers, code, or UI chrome, or if it ignores the article's meaning. After a second miss, keep the better image and tell the user what is wrong with it.

5. **Create or overwrite the cover design in Canva (jeffbaileyblog).** Follow `references/canva-brand-template.md`. In short:

   1. Look in folder `FAFgCl26Zkg` for a design titled with the design name. If it exists, edit that design in place. Otherwise `create-design-from-brand-template` with `EAHXEEDJKs0` to make a new one.
   2. Set the artwork's media ID as that design's page background.
   3. Replace the placeholder title with the short cover title. Leave the background's brightness alone: no shade layer, no vignette.
   4. Rename a new design to the design name.
   5. Show the user the preview and commit once they approve.
   6. Move a new design to folder `FAFgCl26Zkg`.
   7. Export it as a 1200x630 PNG to `<page bundle>/<slug>.png`, compress it with `pngquant`, and look at the exported PNG before going on.

   The cover title is short, not the full front matter `title:`. The template sets it at about 130 px, which fits roughly two lines of 12 characters; set a smaller size for longer lines in the same edit, using the rule in `references/canva-brand-template.md`. Use the title's lead phrase (`Learn Nushell` for "Learn Nushell: Tables, Pipelines, ..."; `What Are AI Evals?`). If the title is already short, use it as is. Put the lead and the highlight on separate lines (`Learn` above `Nushell`).

   If a Canva step fails, stop and tell the user which step failed and why; leave the existing `<slug>.png` in place. Other destinations skip this step; give the user the generated image's "Open generated image" link and media ID instead.

6. **Wire it up (jeffbaileyblog).** Set the front matter unquoted, as `hugo/AGENTS.md` requires:

   ```yaml
   cover:
     image: <slug>.png
     alt: <one sentence describing what the image shows>
   ```

   The alt text describes the picture itself, not the article. On a Canva cover, include the title as it appears on the image. Category bundles are the exception: they set `alt` to the category `title` and add `caption: ""`, matching `categories/laws/_index.md`.

7. **Report.** Give the image path, its size, the alt text, the artwork's Canva media ID, and for jeffbaileyblog the Canva design's name, edit URL, and folder. Keep the inspiration text in the reply so the image can be regenerated later.

## Batch mode

Use this for more than about three covers, such as every category. It needs about eight connector calls per cover (generate, poll, create, read, edit, commit, move, export) instead of a dozen, and one review per batch instead of one per cover.

1. **Agree on review first.** Batch mode saves new designs without a per-cover approval, so get the user's go-ahead for that up front. It never overwrites an existing cover design without asking: list those designs and get approval for them separately.
2. **Write every inspiration text first,** one scratch file per cover, so generation is not waiting on reading.
3. **List the folder once.** Build the title-to-ID map with `list-folder-items` and reuse it for the whole run.
4. **Generate in batches of five.** Start five `generate-image` calls in one turn, then poll each job once; poll again only the ones still `PENDING`. While they run, create the five designs from the brand template. The job IDs are quota tokens, so if a call is refused for quota, stop and tell the user how many covers are left.
5. **Edit each design once.** Read it without thumbnails, then make one `edit-design` call with the background, the three title regions, the computed `font_size`, and the design name. Check the returned `document` and thumbnail, then commit, move, and export.
6. **Fetch the batch in one call.** Pipe the five `<output> <url>` lines to `scripts/fetch-covers.sh`.
7. **Review the batch on one sheet.** `magick montage <the five PNGs> -tile 1x -geometry 600x315+0+8 -background '#111' /tmp/covers-sheet.png`, then look at the sheet. Redo only the covers that fail step 4's checks or show a cramped title.
8. **Wire up the front matter for the batch with one script,** then build the site once per batch and check that each page's `og:image` points at its cover.

Report the batch as a table: output path, design name and edit URL, artwork media ID, and size. Keep the inspiration texts in the scratch directory and list its path, so any cover can be regenerated later.

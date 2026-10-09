---
name: generate-cover-image
description: Generates a 1200x630 PNG cover image from what an article means, using the bundled prompt (dark, futuristic, human-and-system artwork with no text) and the Canva connector. For jeffbaileyblog it builds or overwrites the article's own Canva cover design from the jbb-feature-image-template brand template, sets the title, files and exports it beside the article, and sets the Hugo cover front matter; it also covers category pages and runs in batches for many covers at once. Use whenever someone wants a cover, hero, featured, header, OG, social-preview, or share image for a blog post, article, or category page, says /write:cover, asks to redo or refresh an existing cover, or when write-article finishes a jeffbaileyblog draft, even if they don't say "cover".
---

# Generate Cover Image

A cover works when its composition comes from what the article means, not from its keywords. Everything below serves that: the inspiration text carries the meaning, the bundled prompt (`references/cover-prompt.md`) carries the style, and Canva supplies the artwork and the title.

The prompt ends with `Use the text below as the central inspiration:` and a `---` line; append the inspiration text after it.

## Inputs

- **Article**: a Markdown file path, or the draft in the conversation.
- **Output**: for jeffbaileyblog, `<page bundle>/<slug>.png` beside the bundle's `index.md`, where the slug is the front matter `slug:`. Elsewhere, ask.
- **Category pages** (jeffbaileyblog `hugo/content/categories/<slug>/_index.md`) take covers too. The slug is the directory name, the output is `<slug>.png` beside `_index.md`, and the cover title is the bundle's `title`. A category has no body, so read its `description` and the titles and descriptions of up to ten of its newest posts (on its built page, or in the posts that list it) for the inspiration text. Ten is enough to find what the category is about; reading every post in a large one adds nothing to the picture.

For jeffbaileyblog, the generated artwork is only the background. The published PNG is the export of a Canva design with the title on it; the artwork stays in Canva as a media ID.

| Item | Value |
|------|-------|
| Brand template (source, read-only) | `jbb-feature-image-template`, ID `EAHXEEDJKs0`, brand kit `kAEqeQflWyc` |
| Destination folder | `FAFgCl26Zkg` |
| Design name | the article's `slug:`; for a category, `category-<slug>`, so it never collides with an article cover |

Never open, edit, or publish the brand template: every cover on the blog is built from it. Edits go to the cover's own design, found by its design name, or to a new one made with `create-design-from-brand-template`.

## Workflow

0. **When the complaint is about a share preview** ("the preview looks off when I share it", "the card is wrong"), find out what is wrong before drawing anything, because a new image fixes only one of the causes. Check the built page's `og:image` and `twitter:image` (do they point at the bundle's PNG?) and the PNG's size (1200x630?). If both are right, ask the user what looks off: the artwork, the title, or the crop. If they are fine with the cover itself, the likely cause is a cached card: sites cache link previews, and jeffbaileyblog serves HTML with a long cache lifetime and deploys by hand, so a new image shows only after a deploy and a re-share. Say so rather than regenerating. If the user says the artwork or title itself is the problem, go on to step 1.

1. **Read the article.** Take its title, description, and body. When replacing a cover, look at the old one too, so the new picture does not repeat it.

2. **Write the inspiration text.** In 80 to 150 words of plain prose, state the article's core idea, its emotional tone, and the metaphors, contrasts, or tensions it uses, carried by one central scene: a person doing something in a place that embodies the idea (for example, a crew building a bridge whose shape mirrors the crews). A single concrete scene gives the model something to compose; a list of abstract metaphors gets a generic figure in front of a glowing network. Describe the meaning of the scene, not the layout of the image. Leave out product names, logos, commands, and quoted code: the prompt forbids text in the image, and names pull the model toward literal renderings. Show it to the user only if they asked to review prompts.

3. **Generate with the Canva connector.** Send the joined prompt (`cat references/cover-prompt.md <inspiration.txt>`) to `generate-image` with `aspectRatio: LANDSCAPE_2_1`, then poll `get-generate-image-job` until `SUCCESS`. The result is a media ID (`M...`), the background for step 5. Canva crops it to fill the 1200x630 page.

   Use only Canva; do not call the OpenAI Images API or any other image service. If Canva is not connected or the job fails, write the joined prompt to `<output>.prompt.txt`, tell the user why, and stop. Never draw a placeholder or substitute graphic.

4. **Judge the artwork from the job's preview,** before building anything on it. Regenerate once with a sharper inspiration text if it shows letters, numbers, code, or UI chrome (icons in circles count), or if it ignores the article's meaning. After a second miss, keep the better image and tell the user what is wrong with it. Checking here, not after export, means a bad image costs one generation instead of a whole design.

   Write the alt text now, from the preview you are looking at: the `update_fill` in step 5 needs it. Canva's `alt_text` always describes the artwork itself. The front matter alt in step 6 follows its own rule.

5. **Build the cover design in Canva (jeffbaileyblog).** Follow `references/canva-brand-template.md`, which has the locators, the title split and size rules, and the exact operations. In outline:

   1. Find the design by name in folder `FAFgCl26Zkg`, or create one from template `EAHXEEDJKs0`.
   2. In one `edit-design` call, set the artwork as the page background, set the short cover title (split and sized per the reference), and name a new design.
   3. Show the user the preview and edit URL, and commit once they approve. When overwriting, say so: the commit cannot be undone through the connector. A bundle that already has a `<slug>.png` but no design by that name is an overwrite too, because the export replaces its PNG: ask before creating its design.
   4. Move a new design to the folder, export it as a 1200x630 PNG, and fetch it with `scripts/fetch-covers.sh`, which compresses it with `pngquant`. Look at the result.

   Leave the background's brightness alone: no shade layer, no vignette. If a Canva step fails, stop, tell the user which step and why, and leave any existing PNG in place. Outside jeffbaileyblog, skip this step and give the user the generated image's "Open generated image" link and media ID.

6. **Set the front matter (jeffbaileyblog)** with `scripts/set-cover-frontmatter.py <bundle file> <png name> "<alt>"`. It writes the cover block unquoted, as `hugo/AGENTS.md` requires, replacing any old one:

   ```yaml
   cover:
     image: <slug>.png
     alt: <alt text>
   ```

   For an article, the alt text is one sentence describing the picture itself, including the title as written, not in the capitals the font draws. The script keeps an existing alt's quotes and the block's other keys. For a category, pass `--category`: the alt text is the category `title` and the script adds `caption: ""`.

   Then build the site (`hugo --quiet -D -d /tmp/<dir>` from `hugo/`; `-D` renders drafts) and check that the page's `og:image` is the new PNG.

7. **Report** the image path and size, the alt text, the artwork's media ID, and the design's name, edit URL, and folder. Include the inspiration text so the cover can be regenerated later.

## Batch mode

Use this for more than about three covers, such as every category. It needs about eight connector calls per cover (generate, poll, create, read, edit, commit, move, export) instead of a dozen, and one review per batch instead of one per cover. The steps above still apply to each cover; batch mode changes their order and grouping, not the checks.

1. **Agree on review first.** Batch mode commits new designs without showing each preview, so get the user's go-ahead for that up front. It never overwrites an existing cover without asking: before creating anything, list the covers that already have a design or a PNG, and get approval for those separately.
2. **List the folder once.** Build a title-to-ID map with `list-folder-items` and reuse it for the run, adding each new design to it.
3. **Write every inspiration text before generating,** one scratch file per cover, named by slug. Then read them side by side. Texts written in one sitting drift toward the same picture (a lone figure before a glowing network), and a page of identical covers is a quality failure even when each one is fine alone. Give each cover its own central image, drawn from what that article or category is about, and rewrite any two that would produce the same composition.
4. **Work in batches of five.** Five fit in one turn, can be judged together, and are fetched long before their export URLs expire (about an hour). For each batch:
   1. Start five `generate-image` calls in one turn, and create the five designs from the template while they run.
   2. Poll each job once; poll again only the ones still `PENDING`. Judge each preview as in step 4 and regenerate the misses now, before editing.
   3. For each cover: read the design without thumbnails, make the single `edit-design` call, check the returned `document` and thumbnail, then commit, move, and export.
   4. Pipe the five `<output> <url>` lines to `scripts/fetch-covers.sh`.
   5. Look at all five on one sheet: `magick montage <pngs> -tile 1x -geometry 600x315+0+8 -background '#111' /tmp/covers-sheet.png`. Redo any cover whose title is cramped or overlaps the logo, or that repeats an earlier cover's composition.
   6. Set the front matter for the five with `scripts/set-cover-frontmatter.py --batch` (one `path<TAB>png<TAB>alt[<TAB>category]` line each), build the site, and check that each page's `og:image` is its cover.

   If a call is refused for quota, stop and tell the user how many covers are left.

Report the batch as a table: output path, design name and edit URL, artwork media ID, and size. Keep the inspiration texts in the scratch directory and give its path, so any cover can be regenerated later.

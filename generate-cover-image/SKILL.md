---
name: generate-cover-image
description: Generates a 1200x630 PNG cover image for an article from its meaning, using the bundled cover prompt (dark, futuristic, human-and-system artwork with no text). For jeffbaileyblog it creates a new Canva design from the jbb-feature-image-template brand template (never editing the template itself), swaps in the artwork as the background, sets the title, names the design after the article slug, files it in the blog covers folder, and exports it next to the article with the Hugo cover front matter set. Use when the user says /write:cover, asks for a cover image, hero image, or social/OG image for an article, or when write-article finishes a jeffbaileyblog draft.
---

# Generate Cover Image

Create a cover image whose composition comes from what the article means, not from its keywords. The prompt is bundled in `references/cover-prompt.md`; it ends with `Use the text below as the central inspiration:` and a `---` line, and the inspiration text is appended after it.

## Inputs

- **Article**: a Markdown file path, or the draft in the conversation.
- **Output path**: for jeffbaileyblog, `<page bundle>/<slug>.png` next to the bundle's `index.md` (the slug is the front matter `slug:`). Elsewhere, ask.

For jeffbaileyblog, the generated artwork is only the background. The published `<slug>.png` is the export of a Canva design with the title on it, so the artwork stays in Canva as a media ID and never goes into the bundle.

Every jeffbaileyblog cover is its own Canva design:

| Item | Value |
|------|-------|
| Brand template (source, read-only) | `jbb-feature-image-template`, ID `EAHXEEDJKs0`, in brand kit `kAEqeQflWyc` |
| Destination folder | `FAFgCl26Zkg` |
| Design name | the front matter `slug:`, e.g. `learn-nushell` |

Never open, edit, or publish the brand template. `create-design-from-brand-template` makes a new design, and all edits go to that design.

## Workflow

1. **Read the article.** Take its title, description, and body.

2. **Write the inspiration text.** In 80 to 150 words of plain prose, state the article's core idea, its emotional tone, and the metaphors, contrasts, or tensions it uses. Describe meaning, not layout. Leave out product names, logos, commands, and quoted code, because the prompt forbids text in the image and names pull models toward literal renderings. Show it to the user only if they asked to review prompts.

3. **Generate with the Canva connector.** Join the prompt and the inspiration text (`cat references/cover-prompt.md <inspiration.txt>`) and send the result to Canva `generate-image` with `aspectRatio: LANDSCAPE_2_1`. Poll `get-generate-image-job` with the returned `jobId` until it returns `SUCCESS`. The result is a Canva media ID (`M...`); it is the background asset in step 5. Canva crops it to fill the 1200x630 page.

   Do not call the OpenAI Images API or any other image service. If the Canva tools are not connected or the job fails, write the joined prompt to `<output>.prompt.txt`, tell the user why, and stop. Never draw a placeholder or a substitute graphic.

4. **Look at the artwork.** Read the preview `get-generate-image-job` returns. Regenerate once with a sharper inspiration text if it contains any letters, numbers, code, or UI chrome, or if it ignores the article's meaning. After a second miss, keep the better image and tell the user what is wrong with it.

5. **Create the cover design in Canva (jeffbaileyblog).** Follow `references/canva-brand-template.md`. In short:

   1. `create-design-from-brand-template` with `EAHXEEDJKs0` to make a new design.
   2. Set the artwork's media ID as that design's page background.
   3. Darken the background: upload `assets/cover-shade.png` and place it full-page over the background, then bring the logo, byline, and title to the front. This stands in for the Canva Adjust settings Brightness -55 and Vignette 100, which the connector cannot set.
   4. Replace the placeholder title with the short cover title.
   5. Rename the design to the slug.
   6. Show the user the preview and commit once they approve.
   7. Move the design to folder `FAFgCl26Zkg`.
   8. Export it as a 1200x630 PNG to `<page bundle>/<slug>.png`, compress it with `pngquant`, and look at the exported PNG before going on.

   The cover title is short, not the full front matter `title:`. The template sets it at about 130 px, which fits roughly two lines of 12 characters. Use the title's lead phrase (`Learn Nushell` for "Learn Nushell: Tables, Pipelines, ..."; `What Are AI Evals?`). If the title is already short, use it as is. Put the lead and the highlight on separate lines (`Learn` above `Nushell`).

   If an older design with the same slug name exists in the folder, leave it; the new design replaces it as the cover, and the user can delete the old one.

   If a Canva step fails, stop and tell the user which step failed and why; leave the existing `<slug>.png` in place. Other destinations skip this step; give the user the generated image's "Open generated image" link and media ID instead.

6. **Wire it up (jeffbaileyblog).** Set the front matter unquoted, as `hugo/AGENTS.md` requires:

   ```yaml
   cover:
     image: <slug>.png
     alt: <one sentence describing what the image shows>
   ```

   The alt text describes the picture itself, not the article. On a Canva cover, include the title as it appears on the image.

7. **Report.** Give the image path, its size, the alt text, the artwork's Canva media ID, and for jeffbaileyblog the Canva design's name, edit URL, and folder. Keep the inspiration text in the reply so the image can be regenerated later.

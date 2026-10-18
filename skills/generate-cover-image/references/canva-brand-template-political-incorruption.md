# Canva Brand Template: Political Incorruption feature image

Political Incorruption covers are built the same way as jeffbaileyblog covers: the generated artwork becomes the page background of the article's own design, made from a brand template that adds the title and the site's logo. Follow the steps in `canva-brand-template.md`, with the differences below. Where that file names the jeffbaileyblog template, folder, or title regions, use these instead.

| Item | Value |
|------|-------|
| Brand template | `political-incorruption-feature-image-template`, ID `EAHYZHOADOI` |
| Template source design | `DAHYZDjaJgE` (edit this and publish it again to change the template; never edit a cover to change it) |
| Destination folder | `FAEsL_JzVxg` (`Political Incorruption`), shared with the filed artwork |
| Page size | 1200x630 |
| Prompt | `references/cover-prompt-political-incorruption.md` |

The template has no autofill fields, so fill it with `edit-design`.

## Template layout

Read the locator IDs from the design each time; do not hardcode them.

* **Background**: the page background image (`isMediaReplaceable: true`). Its locator is the page locator.
* **Title**: one text element with one region, placeholder `"Cover Title"`: white `#ffffff`, normal weight, 138.322 px, centered, line height 1.4, in an 877 px wide box at left 161.6. The font draws capitals and carries a black outline effect that the connector cannot see or change; it survives `find_and_replace_text` and `format_text`. The title is one color: there is no highlight region.
* **Logo**: a small flashlight image rect at top 547, above the wordmark. Leave it alone.
* **Wordmark**: `"Political Incorruption"`, bold, 19.4 px. Leave it alone.

## The cover title

Use the short cover title: the front matter `title:` up to and including its first `?`, or up to its first `:` (`Trust the Plan?` from "Trust the Plan? Read Project 2025's CDC Pages Before You Vote"), or the title as is when it is already short. Keep its spelling and case; the font draws capitals either way.

Break it into lines yourself with `\n`, two lines when it can, three at most, so the wrap never lands mid-word: `"Trust the\nPlan?"`, `"Why Was\nTrump\nReelected?"`. Then size it:

```bash
python3 scripts/title-size.py --site political-incorruption "<line 1>" "<line 2>"   # "Trust the" "Plan?" -> 138
```

It caps the size at the template's 138 and fits three lines between the top edge and the logo (116 at most). When it exits 2, break the long line again. When two splits read equally well, keep the one it sizes larger.

## Edit

One `edit-design` call with `finalize: "keep_open"` and `page_index: 1`:

* `update_fill` on the page locator with the artwork media ID and its alt text
* `find_and_replace_text` on the title locator: `"Cover Title"` → the title with its line breaks (for an existing cover, find the current title text instead)
* `format_text` on the title locator with `font_size` from the script, unless it prints 138
* `update_title` → the design name (the slug), for a new design only

Then center the title. The template sets the box's top at 135.8 for two lines at 138 px, which centers it on the page (y = 315). Read the title's `height` from the returned `document`, and if it is not about 358 (two lines at 138), add a `position_element` with `top = 315 - height / 2` and `left` unchanged in the same transaction, but never lower than `545 - height`, so the bottom stays above the logo. Check the result thumbnail: the title must not touch the logo or the frame edges.

## File it

Move a new design to `FAEsL_JzVxg` after the commit. Older Political Incorruption covers (such as `trump-derangement-syndrome` and `why-was-trump-reelected`) were made by hand and may live elsewhere; leave them where they are.

## Front matter

`hugo/AGENTS.md` asks for a `cover:` block with `image: <slug>.png` and `relative: true`. `scripts/set-cover-frontmatter.py` writes `image` and adds `alt`, keeping `relative: true`. The site's Hugo config is `hugo/config/_default/hugo.yaml`; build from `hugo/` as on jeffbaileyblog.

---
name: hugo-agents-compliance
description: Enforces jeffbaileyblog Hugo Markdown rules by reading and applying AGENTS.md in document order (top to bottom), including nested AGENTS.md and writing-style.md. Use when editing or creating content under the Hugo site (hugo/content/), drafting blog posts, fixing Hugo build errors, or the user says /hugo:agents, "apply AGENTS.md", "Hugo blog rules", or "compliance with hugo AGENTS".
---

# Hugo site: AGENTS.md compliance

When you create or edit Markdown for the **jeffbaileyblog** Hugo site, treat the rules in **`AGENTS.md`** as mandatory. **Do not rely on memory or summaries alone** — read the file each session and work through it **from the first line to the last**, in the order its headings appear.

## Where the rules live

- **Site-wide:** `<hugo-site-root>/AGENTS.md` (the `hugo/` folder in the blog repo).
- **Section or series overrides:** any `AGENTS.md` **closer to the file** you are editing (for example `content/blog/fundamentals-x/AGENTS.md`). Read the global file first, then the nearest `AGENTS.md` on the path from `content/` down to the bundle. **Nearer files add or override** where they say they do.

## Post shape and categories: no exploration needed

Do NOT read sibling posts to "establish the shape" of a post, and do NOT grep the content tree to discover categories. Both are already available deterministically:

- **Front-matter shape:** the **`## Front matter (blog posts)`** section of `AGENTS.md` is the canonical, complete shape. Use it directly (plus any nearer `AGENTS.md` overrides). A sibling post adds nothing and may itself be non-compliant.
- **Categories in use:** run, from the Hugo site root:

  ```bash
  ./scripts/generate-site-metadata.py
  ```

  It prints JSON with every category in use (`categories`) and per-category post counts (`category_counts`, sorted by frequency — prefer higher-count categories when several fit). If you cannot run the script, read `data/site-metadata.json` (its last written output) instead; add `--write` when running the script to refresh that file.

## Workflow (always in this order)

1. **Open and read** `<hugo-site-root>/AGENTS.md` from top to bottom. Note every `##` section; your compliance pass must cover each section that applies to the task.
2. **If the target path sits under a subtree that has its own `AGENTS.md`**, read that file the same way (top to bottom) and merge its requirements with the global rules.
3. **Apply rules in the same order they appear in `AGENTS.md`** (front matter → cover → writing style → post structure → content guidelines → formatting → links → build verification → SEO checklist → publishing checklist). If a section does not apply (e.g. no cover image), skip it explicitly in your reasoning or checklist.
4. **`## Writing style` in `AGENTS.md`** points at **`content/prompts/writing-style.md`**. Read and follow that file for voice, tone, formatting, SEO prose rules, and pitfalls. **When `AGENTS.md` and `writing-style.md` disagree, follow `writing-style.md`.**
5. **Banned phrase scan (mandatory, not optional).** `writing-style.md` enumerates banned phrases in two places: a "**## Writing Style: Things to NOT Do**" section near the bottom, AND inline `Skip "..."` / `Using these words: "..."` markers scattered earlier in the file. **"Read and follow" is not enough** — extract every banned token from the current version of `writing-style.md`, then `grep` your edited content for each. Treat any hit as a blocker, not a suggestion. Categories to extract:

   - **Inline `Skip "..."` markers** (e.g. `load bearing` / `load-bearing`, `the whole trick`, `nightmare scenarios`, `gets really ugly`).
   - **"Do NOT use performative or AI-coded phrases"** list (e.g. `no fluff`, `shouting into the void`, `and honestly`, `you're not imagining this`, `that's rare`, `here's the kicker`, `the best part?`, `the important part is this`, `read this twice`, `quietly [doing something]`, `key takeaway`, `let me ground you`, `you're thinking about this exactly the right way`).
   - **"Using these words:"** entries (e.g. `fostering`).
   - **Contrast-framing patterns** in "Do NOT rely on contrast framing as a crutch" (`it's not X, it's Y`, `not chaos. clarity.`).
   - **Banned punctuation/markup:** emdashes (`—`), HTML `<a href>` tags, inline `[text](url)` for internal refs, bare `{{< ref >}}` in body.

   **Re-run this scan after every editing pass**, including external prose tools, AI rewriters, and human revisions. Those workflows reliably reintroduce banned phrases because they optimize for fluency over the project's specific bans.

   Example grep catching common bans in one pass (extract the live list from `writing-style.md`, this is illustrative only):

   ```bash
   grep -niE "—|load.bearing|the whole trick|fostering|no fluff|key takeaway|here'?s the kicker|the best part\?|read this twice|quietly |shouting into the void|nightmare scenario|and honestly|you'?re not imagining this|that'?s rare|let me ground you|the important part is this|gets really ugly" path/to/index.md
   ```

   Do NOT skip this step on the grounds that the prose "looks fine" or that you wrote it yourself this session. Author-blindness is exactly why this step exists.

6. **After substantive Markdown or content changes**, run from the Hugo site root:

   ```bash
   hugo --gc --minify
   ```

   Fix all reported issues (including **`REF_NOT_FOUND`** from invalid `{{< ref >}}`) before you stop.

## Compliance habits

- **Front matter:** Match the shape, date format, slug/url alignment, and fields `AGENTS.md` specifies unless a nearer `AGENTS.md` overrides them.
- **Front matter — NEVER quote `url` or `slug`:** Write `url: /blog/YYYY/MM/DD/my-slug` and `slug: my-slug` (bare, no double quotes). Quoted values like `url: "/blog/..."` or `slug: "my-slug"` are forbidden. Other string fields (`title`, `description`) may still be quoted per the usual YAML rules.
- **Front matter — ALWAYS include `cover.image`, unquoted, slug-matched, `.png`:** Every post's front matter must have:

  ```yaml
  cover:
      image: my-slug.png
  ```

  Where `my-slug` matches the `slug` value exactly, the extension is `.png`, and the value is bare (no double quotes). Example: for `slug: how-long-should-a-function-be`, use `image: how-long-should-a-function-be.png`.
- **Front matter — `categories:` MUST contain at least one entry (never missing, never empty):** Every content file the pass touches — blog posts AND pages under `content/` — must declare a `categories:` list with **at least one** category. A missing `categories:` block, an empty list, or `categories: []` is a compliance failure. Do NOT skip this check because the file is `type: page` instead of `type: post`; "the front-matter shape section only covers posts" is not an exemption. If the file has no categories, add the best fit from categories already in use on the site — get the list with:

  ```bash
  ./scripts/generate-site-metadata.py
  ```

  Only invent a new category when nothing existing fits, and say so explicitly in your summary.
- **Front matter — prefer existing categories, and never restate the site's context in a category name:** The whole site is about software development, so every category already implies it. Category names that spell it out are redundant. When choosing, ALWAYS prefer the short existing form over a "software"/"development"-qualified variant:

  - "Software Development" → use **Software**.
  - "Development Tools" → use **Tools**.

  Apply the same test to any candidate: strip the words "software" and "development" and check whether an existing category already covers what remains. Pick from the existing category list first; inventing a new category (especially a qualified variant of an existing one) is a last resort.
- **Front matter — `categories:` and `keywords:` must fit the target article:** On every create or edit pass, review both lists against the article's actual content and update them so they stay relevant. Pick `categories:` from categories already in use on the site (run `./scripts/generate-site-metadata.py` from the site root) rather than inventing new ones. For `keywords:`, follow the single SEO prompt at `hugo/content/prompts/seo-front-matter.md` — primary keyword first, 4–7 long-tail phrases the article substantively covers, no category duplication.
- **Front matter — `title:` and `description:` follow the SEO prompt:** Apply `hugo/content/prompts/seo-front-matter.md`, the one place SEO rules live (based on Google's SEO Starter Guide) — unique, accurate titles that front-load the primary keyword with any type or series label after it, and a succinct one- or two-sentence description that leads with the same keyword and matches the content.
- **Front matter — update `lastmod:` when updating an article:** Any substantive edit to an existing post must set `lastmod:` to today's date (same `YYYY-MM-DD` format as `date:`). Leave `date:` unchanged — it records original publication.
- **Formatting:** No Markdown tables for comparisons or structured lists where `AGENTS.md` requires the `cards` shortcode; no `` ```text `` diagrams — use Mermaid as specified.
- **Links:** Internal links use **`{{< ref "slug" >}}`** with slug only unless the file already follows another established pattern; external links and **`## References`** follow the reference rules at the end of the doc.
- **Voice — NEVER sanitize profanity:** A compliance pass fixes structure, front matter, and banned phrases. It does NOT clean up swearing. If the source draft says "fuck", the compliant rewrite says "fuck". Profanity is part of the site's authentic voice per `writing-style.md`; removing or softening it is a compliance failure, not a courtesy.
- **Checklists:** Before you consider the work done, run through the **SEO** and **Publishing** checklists in `AGENTS.md` for anything user-visible or publish-related.
- **Banned phrases:** Re-grep against the `writing-style.md` ban list (see workflow step 5) after every edit pass. Author-blindness and prose-tool regression both make this a recurring failure, not a one-time check.

## When this skill does not apply

Skip it for non-Hugo repos, non-Markdown assets with no `AGENTS.md` expectations, or tasks the user limits to unrelated files.

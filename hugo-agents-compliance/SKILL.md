---
name: hugo-agents-compliance
description: Enforces jeffbaileyblog Hugo Markdown rules by reading and applying AGENTS.md in document order (top to bottom), including nested AGENTS.md and writing-style.md. Use when editing or creating content under the Hugo site (hugo/content/), drafting blog posts, fixing Hugo build errors, or the user says /hugo:agents, "apply AGENTS.md", "Hugo blog rules", or "compliance with hugo AGENTS".
---

# Hugo site: AGENTS.md compliance

When you create or edit Markdown for the **jeffbaileyblog** Hugo site, treat the rules in **`AGENTS.md`** as mandatory. **Do not rely on memory or summaries alone** — read the file each session and work through it **from the first line to the last**, in the order its headings appear.

## Where the rules live

- **Site-wide:** `<hugo-site-root>/AGENTS.md` (the `hugo/` folder in the blog repo).
- **Section or series overrides:** any `AGENTS.md` **closer to the file** you are editing (for example `content/blog/fundamentals-x/AGENTS.md`). Read the global file first, then the nearest `AGENTS.md` on the path from `content/` down to the bundle. **Nearer files add or override** where they say they do.

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
- **Formatting:** No Markdown tables for comparisons or structured lists where `AGENTS.md` requires the `cards` shortcode; no `` ```text `` diagrams — use Mermaid as specified.
- **Links:** Internal links use **`{{< ref "slug" >}}`** with slug only unless the file already follows another established pattern; external links and **`## References`** follow the reference rules at the end of the doc.
- **Checklists:** Before you consider the work done, run through the **SEO** and **Publishing** checklists in `AGENTS.md` for anything user-visible or publish-related.
- **Banned phrases:** Re-grep against the `writing-style.md` ban list (see workflow step 5) after every edit pass. Author-blindness and prose-tool regression both make this a recurring failure, not a one-time check.

## When this skill does not apply

Skip it for non-Hugo repos, non-Markdown assets with no `AGENTS.md` expectations, or tasks the user limits to unrelated files.

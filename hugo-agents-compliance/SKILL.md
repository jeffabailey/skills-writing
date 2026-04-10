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
5. **After substantive Markdown or content changes**, run from the Hugo site root:

   ```bash
   hugo --gc --minify
   ```

   Fix all reported issues (including **`REF_NOT_FOUND`** from invalid `{{< ref >}}`) before you stop.

## Compliance habits

- **Front matter:** Match the shape, date format, slug/url alignment, and fields `AGENTS.md` specifies unless a nearer `AGENTS.md` overrides them.
- **Formatting:** No Markdown tables for comparisons or structured lists where `AGENTS.md` requires the `cards` shortcode; no `` ```text `` diagrams — use Mermaid as specified.
- **Links:** Internal links use **`{{< ref "slug" >}}`** with slug only unless the file already follows another established pattern; external links and **`## References`** follow the reference rules at the end of the doc.
- **Checklists:** Before you consider the work done, run through the **SEO** and **Publishing** checklists in `AGENTS.md` for anything user-visible or publish-related.

## When this skill does not apply

Skip it for non-Hugo repos, non-Markdown assets with no `AGENTS.md` expectations, or tasks the user limits to unrelated files.

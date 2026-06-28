---
name: write-validate-article
description: Validates a Markdown article for the jeffbaileyblog Hugo site by enforcing AGENTS.md + writing-style.md compliance (read top to bottom, including nested AGENTS.md), running a banned-phrase scan, verifying the Hugo build, then running link checking (lychee) and Markdown linting (markdownlint). Use when the user says /write:validate-article or /hugo:agents, wants to validate an article, check article quality, run all checks on a Markdown file, "apply AGENTS.md", "Hugo blog rules", "compliance with hugo AGENTS", drafting blog posts, or fixing Hugo build errors.
---

# Validate Article

Run every validation check against a Markdown article for the **jeffbaileyblog** Hugo site: AGENTS.md compliance, a banned-phrase scan, Hugo build verification, link checking, and Markdown linting. The goal is one publishable file that passes all gates.

## Workflow (always in this order)

1. **Identify the target file** -- The user provides a file path as the argument. If none is given, ask which file to validate.

2. **Apply AGENTS.md + writing-style.md compliance** -- See "AGENTS.md compliance" below. Read the rules each session and apply them in document order. Do not rely on memory or summaries alone.

3. **Run the banned-phrase scan** -- Mandatory, not optional. See "Banned phrase scan" below. Re-run it after every editing pass.

4. **Verify the Hugo build** -- From the Hugo site root run `hugo --gc --minify` (add `-D` when the post is `draft: true`, so `{{< ref >}}` links still resolve). Fix all reported issues, including `REF_NOT_FOUND` from an invalid `{{< ref >}}`.

5. **Run link checking** -- Invoke the `write-check-links` skill against the target file (lychee with the Hugo site's `lychee.toml`).

6. **Run Markdown linting** -- Invoke the `write-run-markdown-lint` skill against the target file (markdownlint-cli2 with the user's config).

7. **Report results** -- Summarize the combined results across all checks. If everything passes, confirm the article is valid. If anything fails, present all errors together, grouped by check, and offer to fix them.

## AGENTS.md compliance

When you create or edit Markdown for the jeffbaileyblog Hugo site, treat the rules in **`AGENTS.md`** as mandatory. Read the file each session and work through it **from the first line to the last**, in the order its headings appear.

### Where the rules live

- **Site-wide:** `<hugo-site-root>/AGENTS.md` (the `hugo/` folder in the blog repo).
- **Section or series overrides:** any `AGENTS.md` **closer to the file** you are editing (for example `content/blog/fundamentals-x/AGENTS.md`). Read the global file first, then the nearest `AGENTS.md` on the path from `content/` down to the bundle. **Nearer files add or override** where they say they do.

### How to apply

1. **Open and read** `<hugo-site-root>/AGENTS.md` top to bottom. Note every `##` section; your compliance pass must cover each section that applies to the task.
2. **If the target path sits under a subtree that has its own `AGENTS.md`**, read that file the same way (top to bottom) and merge its requirements with the global rules.
3. **Apply rules in the same order they appear in `AGENTS.md`** (front matter → cover → writing style → post structure → content guidelines → formatting → links → build verification → SEO checklist → publishing checklist). If a section does not apply (e.g. no cover image), skip it explicitly in your reasoning or checklist.
4. **`## Writing style` in `AGENTS.md`** points at **`content/prompts/writing-style.md`**. Read and follow that file for voice, tone, formatting, SEO prose rules, and pitfalls. **When `AGENTS.md` and `writing-style.md` disagree, follow `writing-style.md`.**

### Compliance habits

- **Front matter:** Match the shape, date format, slug/url alignment, and fields `AGENTS.md` specifies unless a nearer `AGENTS.md` overrides them.
- **Front matter — NEVER quote `url` or `slug`:** Write `url: /blog/YYYY/MM/DD/my-slug` and `slug: my-slug` (bare, no double quotes). Quoted values like `url: "/blog/..."` or `slug: "my-slug"` are forbidden. Other string fields (`title`, `description`) may still be quoted per the usual YAML rules.
- **Front matter — ALWAYS include `cover.image`, unquoted, slug-matched, `.png`:** Every post's front matter must have:

  ```yaml
  cover:
      image: my-slug.png
  ```

  Where `my-slug` matches the `slug` value exactly, the extension is `.png`, and the value is bare (no double quotes). Example: for `slug: how-long-should-a-function-be`, use `image: how-long-should-a-function-be.png`.
- **Voice — Diátaxis articles use no first person:** For tutorials, how-to guides, reference, and explanation content, `writing-style.md` requires second person ("you") and imperative voice, not "I"/"my". This overrides any create-prompt that asks for first person.
- **Formatting:** No Markdown tables for comparisons or structured lists where `AGENTS.md` requires the `cards` shortcode; no `` ```text `` diagrams — use Mermaid as specified (prefer `graph TB`).
- **Links:** Internal links use **`{{< ref "slug" >}}`** with slug only unless the file already follows another established pattern; external links and **`## References`** follow the reference rules at the end of the doc. Verify link targets are not `draft: true` (linking to a draft fails the build).
- **Checklists:** Before you consider the work done, run through the **SEO** and **Publishing** checklists in `AGENTS.md` for anything user-visible or publish-related.

## Banned phrase scan

`writing-style.md` enumerates banned phrases in two places: a "**## Writing Style: Things to NOT Do**" section near the bottom, AND inline `Skip "..."` / `Using these words: "..."` markers scattered earlier in the file. **"Read and follow" is not enough** — extract every banned token from the current version of `writing-style.md`, then `grep` the edited content for each. Treat any hit as a blocker, not a suggestion. Categories to extract:

- **Inline `Skip "..."` markers** (e.g. `load bearing` / `load-bearing`, `the whole trick`, `nightmare scenarios`, `gets really ugly`, `failure modes` when talking about possible failures).
- **"Do NOT use performative or AI-coded phrases"** list (e.g. `no fluff`, `shouting into the void`, `and honestly`, `you're not imagining this`, `that's rare`, `here's the kicker`, `the best part?`, `the important part is this`, `read this twice`, `quietly [doing something]`, `key takeaway`, `let me ground you`, `you're thinking about this exactly the right way`).
- **"Using these words:"** entries (e.g. `fostering`).
- **Contrast-framing patterns** in "Do NOT rely on contrast framing as a crutch" (`it's not X, it's Y`, `not chaos. clarity.`).
- **Banned punctuation/markup:** emdashes (`—`), HTML `<a href>` tags, inline `[text](url)` for internal refs, bare `{{< ref >}}` in body.

**Re-run this scan after every editing pass**, including external prose tools, AI rewriters, and human revisions. Those workflows reliably reintroduce banned phrases because they optimize for fluency over the project's specific bans.

Example grep catching common bans in one pass (extract the live list from `writing-style.md`; this is illustrative only):

```bash
grep -niE "—|load.bearing|the whole trick|fostering|no fluff|key takeaway|here'?s the kicker|the best part\?|read this twice|quietly |shouting into the void|nightmare scenario|and honestly|you'?re not imagining this|that'?s rare|let me ground you|the important part is this|gets really ugly" path/to/index.md
```

Do NOT skip this step on the grounds that the prose "looks fine" or that you wrote it yourself this session. Author-blindness is exactly why this step exists.

## When the compliance rules do not apply

Skip AGENTS.md compliance for non-Hugo repos, non-Markdown assets with no `AGENTS.md` expectations, or tasks the user limits to unrelated files. The link-check and Markdown-lint steps still apply to any Markdown file the user asks to validate.

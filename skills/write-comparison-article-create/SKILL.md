---
name: write-comparison-article-create
description: Creates clean, decision-first comparison articles (X vs Y vs Z) that render well in Hugo — verdict up top, scorecard cards, per-criterion deep dive, use-case recommendations, and sourced version/price/license claims. Use when the user says /write:comparison-article-create, asks to write a comparison or "vs" page, "X vs Y", "which should I pick", or compare tools/frameworks/products. Articles live in content/blog/x-vs-x/.
---

# Comparison Article Create

Creates a **comparison article**: a page that helps a reader *decide* between several options (frameworks, tools, products, approaches). Self-contained; no hosted prompt to fetch. Articles live in `hugo/content/blog/x-vs-x/<slug>/index.md` in jeffbaileyblog.

A great comparison page is **decision-first, not description-first**. The reader arrives with a choice to make and wants the answer fast, then evidence if they keep reading.

## Scope

This skill adds only what is specific to comparison articles: the decision-first rules, the section order, the shortcodes, the sourcing rule, and a checker. The site's general rules come from two canonical files; read them, and when they disagree with this skill they win:

- **`hugo/content/prompts/writing-style.md`**. The rules that matter most here: no emdashes; reference-style links only (`[text][label]` plus a definition, never inline or HTML links); the Diátaxis voice override (no first-person author voice, second person for guidance); `## References` for factual claims; no Markdown tables (use `cards`); the "Things to NOT Do" list.
- **`hugo/content/prompts/seo-front-matter.md`** for `title`, `description` (160 characters or fewer), and `keywords`.
- **`hugo/AGENTS.md`** for front-matter shape, cover-image fields, and cards syntax. Its build command does not render drafts; use step 8 below instead.

A comparison is a neutral **Diátaxis explanation**. The only comparison-specific front-matter fields are `diataxis: explanation` and `articletype: comparison`. Keep `draft: true` (the AGENTS.md default) unless the user says to publish.

## What makes a comparison page good (non-negotiable)

1. **Bottom line up top.** The verdict, segmented by use case ("Choose X if…"), appears before any deep dive. Each deep-dive section also opens with its own outcome.
2. **Segment the verdict; don't crown one universal winner.** "Best for a solo founder" / "best for a large team" serves more readers and reads as more honest. Declare an overall pick only when the evidence supports one.
3. **Earn objectivity; don't claim it.** Show how the comparison was made (versions, dates, criteria). Name real strengths of every option and real weaknesses of the favored one. Use specifics (numbers, versions, feature names), not marketing adjectives.
4. **Decision drivers over feature trivia.** Every scorecard field and criterion must be something a reader would actually decide on.

## Facts and sourcing

Comparison pages go stale and get quoted, so wrong facts do real damage.

- **Never invent** versions, release dates, prices, license terms, benchmarks, adoption numbers, or first-person test results. Research them (web search, official docs, release notes, pricing pages) or leave a placeholder.
- **Every version, price, date, license, and numeric claim** in the intro or a body section (Contenders, methodology, Head-to-head, Strengths, Cost) carries a reference-style link to its source in the same sentence, or the literal text `TODO verify`. Reuse a label when the same source backs a later sentence. The summary sections (Short answer, At a glance, Which should you choose, Bottom line, FAQ) may restate a claim that is linked in the body; a new fact first stated in one of them still needs its link. The checker catches versions, prices, percentages, counts with units (employees, resources, seats), and license names, so review other numbers (employee thresholds, dates, benchmarks) by eye.
- **Prefer the official source** (vendor pricing page, release notes, LICENSE file). When sources disagree, cite the official one, mention the other, and add `TODO verify`.
- **Derived figures** (a total you computed from a price page) cite their inputs' source in the same sentence and show the arithmetic once. A URL you did not open in this session gets `TODO verify` next to it.
- Date fast-moving figures ("as of October 2026") in the methodology and the Cost section.
- List every `TODO verify` in the delivery note so the user knows what to confirm.

## Canonical section order

Produce these sections in this order. Omit a section only when it genuinely does not apply (only Cost and the decision-tree part of "Which should you choose?" are optional).

1. **Front matter**: AGENTS.md shape plus `diataxis: explanation` and `articletype: comparison`. Categories start with `X vs X`.
2. **Framing intro** (2–4 short paragraphs, no heading): who is choosing, why it's hard, what changed recently.
3. **`## The short answer`**: one `**Choose X if…**` card per option in a `cards` block, plus an optional overall pick and its caveat. The single most important section.
4. **`## The contenders`**: one card per option: what it is, who it's for, its one-line differentiator. The card count here defines the option count the checker uses.
5. **`## At a glance`**: the scorecard, one card per option. See the scorecard format below.
6. **`## How these were compared`**: versions and dates (linked), then the criteria as `* **Criterion.** why it matters` bullets, then a re-verify caveat. The criteria names must equal the Head-to-head `###` headings, in the same order.
7. **`## Head-to-head`**: one `###` per criterion. Each subsection's first paragraph starts with `Winner here: X, because…` (or `Winner here: tie, …`), then evidence, then a one-line mini-verdict.
8. **`## Which should you choose?`**: 3–5 "Best for [persona/scenario]" cards, each a pick plus a one-line why; optionally a ` ```mermaid ` `graph TD` decision tree with plain nodes (no emoji, no rainbow fills).
9. **`## Strengths and trade-offs`**: one `### Option` plus `{{< procon >}}` block per option (`pros --cons-- cons`, bullet lists each side, including gotchas).
10. **`## Cost`** (*conditional*): a real total-cost comparison for paid tools/SaaS, dated and sourced. Pick one or two reference sizes that fit the audience (for example 5 seats or 2,000 managed resources), show the per-tier arithmetic, and name what is excluded (support, overages, self-hosting labor). Include it when any option has a paid tier the reader may hit (for example a free engine with a paid desktop app above a company-size threshold), and then do not also make cost a Head-to-head criterion. When every option is free, fold cost of ownership into Head-to-head and omit this section.
11. **`## The bottom line`**: restate the segmented recommendation, now earned. End with a next step or further reading, not a hard sell.
12. **`## FAQ`**: 3–5 natural "People Also Ask" questions as `**Question?**` lines, 2–4 sentence answers.
13. **`## References`**: one bullet per external source, `* [Title][label], for what it supports.` Required by writing-style.md for factual claims.
14. **`## Related Content`**: 2–4 internal links to published posts, then all link reference definitions at the end of the file.

Do **not** add `{{< partial "category_footer" >}}`. `layouts/_default/single.html` already renders the category footer, so adding it shows "Related Articles by Category" twice.

### Scorecard format

Pick 5–6 fields that drive this decision (for example: Architecture or Type, Learning curve, Language, License, Ecosystem, Performance, Pricing model, Hosting, CI fit), ending with **Best for**. Every card uses the exact same labels in the same order, one bullet each, in this format so the checker can compare them:

```markdown
{{< cards >}}
**Option A**
* **Architecture.** Client plus root daemon.
* **Learning curve.** Lowest; the default in most docs.
* **Best for.** Mixed-OS teams.
--card--
**Option B**
* **Architecture.** Daemonless, fork-exec per container.
* **Learning curve.** Low for Option A users.
* **Best for.** Linux-first teams.
{{< /cards >}}
```

Descriptive cells beat checkmarks. Keep each cell under about 15 words; 3–4 options with 6 fields is already long on a phone.

## Internal links

`{{< ref "…" >}}` resolves by content path or bundle folder name, not by front-matter `slug` (some published posts have a slug that differs from their folder). Find link targets with `hugo list all` run in `hugo/` (or `scripts/site-search` from the repo root, per AGENTS.md "Searching existing posts"), keep rows with `draft` = `false`, and use the folder name from the `path` column.

**Do not link to draft posts.** A ref to a draft builds only with `-D`; once this article is published, the normal build fails with `REF_NOT_FOUND`. If the only relevant post is a draft, leave it out and mention it in the delivery note.

## Workflow

1. **Gather inputs**: the options (2–4 works best on mobile), the audience, and the criteria that matter for this decision. Infer defaults from the request; ask once, in one message, only for what you cannot infer (usually just confirming the options). Pick the slug as `a-vs-b[-vs-c]`.
2. **Research facts**: current versions and release dates, license, pricing (if paid), notable recent changes. Record a source URL for each. Anything you cannot confirm becomes `TODO verify`.
3. **Pick 4–6 decision-driving criteria.** Discard trivia.
4. **Draft in canonical order**, verdict-first throughout, applying the sourcing rule as you write.
5. **Apply writing-style.md** (links, voice, no tables, no emdashes, the "Things to NOT Do" list).
6. **Run the checker** (needs `python3`; `hugo` for ref and build checks):

   ```bash
   python3 <skill-dir>/scripts/check_comparison.py hugo/content/blog/x-vs-x/<slug>/index.md
   ```

   It checks front matter, section order, one "Choose X if" and one scorecard card per option, identical scorecard labels, methodology criteria = Head-to-head `###`, every `###` opening with `Winner here:`, procon count, no tables / emdashes / category_footer, first-person author voice (reader-voice FAQ questions such as "Do I need to pay for Docker?" are exempt), unsourced version/price/license sentences, and that each `ref` resolves to a published post. Fix every FAIL; resolve or justify each WARN.
7. **Remove AI tells**: invoke the `ai-sanitize` skill (`jbb-skills:ai-sanitize` as a plugin) on the draft in edit mode. Comparison pages attract hollow verdicts ("a powerful, seamless choice"). Keep the canonical section headings (including "The bottom line") even if ai-sanitize flags them; the checker depends on them. If it is not installed, say so in the delivery note and skip this step. Re-run step 6 afterward.
8. **Build and confirm the page renders.** The new post is `draft: true` and the site does not build drafts, so plain `hugo --gc --minify` exits 0 without rendering it. Run:

   ```bash
   python3 <skill-dir>/scripts/check_comparison.py hugo/content/blog/x-vs-x/<slug>/index.md --build
   ```

   This runs `hugo --gc --minify -D -d <tempdir>` in `hugo/` (never writing `public/`), then confirms `<tempdir>/<url>/index.html` exists and contains `card-grid` and `md-procon`, the mermaid tree if one was written, no raw `{{<` shortcode text, and exactly one category footer. Exit 3 means `hugo` is missing (`brew install hugo`), which is a tool problem, not a failed check. To do it by hand: `hugo --gc --minify -D -d "$(mktemp -d)"`, then grep the page's `index.html`.
9. **Deliver**: the file path, the checker result, the list of `TODO verify` items, any draft posts you chose not to link, and the cover image TODO (`cover.image: <slug>.png`; the `generate-cover-image` skill can make it).

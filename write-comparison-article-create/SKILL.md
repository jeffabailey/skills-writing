---
name: write-comparison-article-create
description: Creates clean, decision-first comparison articles (X vs Y vs Z) that render well in Hugo — verdict up top, scorecard cards, per-criterion deep dive, and use-case recommendations. Use when the user says /write:comparison-article-create, asks to write a comparison or "vs" page, or compare tools/frameworks/products. Articles live in content/blog/comparison-x/.
---

# Comparison Article Create

Direct shortcut to create a **comparison article** — a page that helps a reader *decide* between several options (frameworks, tools, products, approaches). Self-contained; no hosted prompt to fetch.

A great comparison page is **decision-first, not description-first**. The reader arrives with a choice to make and wants the answer fast, then evidence if they keep reading. Articles live in `content/blog/comparison-x/<slug>/index.md`.

## Scope of this skill (what it does and does NOT cover)

This skill adds **only what is specific to comparison articles**: the decision-first principles, the section order, and which shortcode renders which section.

It deliberately does **not** restate the site's general rules, so it can never drift from them. Voice, front matter, SEO, internal-link style, "no Markdown tables → use `cards`", and Mermaid conventions are all governed by the canonical sources — apply them as-is:

- **`hugo/content/prompts/writing-style.md`** — voice (including the Diátaxis no-first-person override), formatting, links, SEO, front-matter SEO fields. When it disagrees with anything here, it wins.
- **`hugo/AGENTS.md`** — front-matter shape, cover-image rules, build verification.

A comparison article is a neutral **Diátaxis explanation**: apply the writing-style Diátaxis voice override (no first-person author voice; second person for reader guidance — "Choose React if you…"). The only comparison-specific front-matter fields are `diataxis: explanation` and `articletype: comparison`.

## What makes a comparison page good (non-negotiable)

These four rules come from studying the best comparison pages on the web. Break them and the page reads as thin, biased content.

1. **Bottom line up top.** The verdict — segmented by use case ("Choose X if…") — appears above the fold, before any deep dive. Never make the reader scroll 2,000 words to learn who wins. Each deep-dive section *also* opens with its own mini-verdict (inverted pyramid, twice over).
2. **Segment the verdict; don't crown one universal winner.** "Best for a solo founder" / "best for a large team" serves more readers and reads as more honest than a single decree. Only declare an overall pick when the evidence genuinely supports one.
3. **Earn objectivity — don't claim it.** Show *how* the comparison was made (versions, dates, criteria, weighting). Name the genuine strengths of every option and the real weaknesses of your favored one. Use concrete specifics — numbers, versions, feature names, benchmarks — not marketing adjectives ("powerful", "intuitive").
4. **Decision drivers over feature trivia.** Every scorecard field and criterion must be something a reader would actually decide on. No checkbox-soup.

## Canonical section order

Produce these sections in this order. Omit a section only when it genuinely does not apply. The **Shortcode** column is the comparison-specific rendering choice; the general "why cards not tables" reasoning lives in `writing-style.md`.

1. **Front matter** — standard shape (per `AGENTS.md`) plus `diataxis: explanation` and `articletype: comparison`.
2. **Framing intro** (2–4 short paragraphs, no heading) — who is choosing, why it's hard, what changed recently. Tight; lead straight into the verdict.
3. **`## The short answer`** — the verdict, above the fold. One "**Choose X if** …" line per option, plus an optional overall pick and its caveat. → **`cards`** (or a bold list). *The single most important section.*
4. **`## The contenders`** — one short block per option: what it is, who it's for, its one-line differentiator. → `cards` or short paragraphs.
5. **`## At a glance`** — the scorecard: one card per option, each with the **same 5–6 decision-driving fields** (Type, Learning curve, Performance, Bundle size, Ecosystem & jobs, Best for). Descriptive cells beat bare checkmarks. → **`cards`**.
6. **`## How these were compared`** — methodology. What was tested, versions and dates, the criteria and why they matter, and a caveat that fast-moving figures need re-verifying. Builds trust *before* the opinions land.
7. **`## Head-to-head`** — per-criterion deep dive, one `###` per criterion. **Each subsection opens with its outcome** ("Winner here: X, because…"), then concrete evidence, then a one-line mini-verdict.
8. **`## Which should you choose?`** — 3–5 "Best for [persona/scenario]" callouts mapping each to a pick + one-line why (→ **`cards`**), optionally a decision tree (→ **` ```mermaid ` `graph TD`**).
9. **`## Strengths and trade-offs`** — one honest, specific pros/cons block per option (include the gotchas). → **`procon`** (` {{< procon >}} pros --cons-- cons {{< /procon >}} `; bullet lists each side).
10. **`## Cost`** — *conditional.* A real total-cost comparison for paid tools/SaaS. For free/open-source options, fold cost-of-ownership (hiring, maintenance, migration risk) into Head-to-head and omit this section.
11. **`## The bottom line`** — final verdict: restate the use-case-segmented recommendation, now earned by the evidence. End with a next step / further reading, not a hard sell.
12. **`## FAQ`** — 3–5 natural-language "People Also Ask"-style questions, 2–4 sentence answers.
13. **`## Related Content`** — contextual internal links, then `{{< partial "category_footer" >}}`, then the external link reference definitions.

## Workflow

1. **Gather inputs** — the options to compare (2–4 works best on mobile), the audience, and the criteria that matter most for *this* decision. If the user gave a slug/topic, infer sensible defaults and confirm only the options.
2. **Pick decision-driving criteria** — 4–6 axes the reader would actually choose on. Discard trivia.
3. **Draft in canonical order** — every applicable section above, verdict-first throughout.
4. **Fill scorecards and criteria with specifics** — real versions, approximate figures with an "as of `<date>`" caveat, feature names. Never leave a marketing adjective unbacked.
5. **Apply the canonical style sources** — `writing-style.md` and `AGENTS.md` (voice, front matter, links, tables→cards, Mermaid, build). This skill does not restate them.
6. **Verify the comparison-specific essentials:**
   - Verdict is above the fold and use-case-segmented; every Head-to-head `###` opens with its outcome.
   - Comparison matrix is `cards`; strengths/trade-offs are `procon`; any decision tree is a `mermaid` fence.
   - `articletype: comparison` is set; `{{< partial "category_footer" >}}` sits before the link definitions.
   - Enforce the writing-style Diátaxis voice override (no first-person author voice):
     ```bash
     grep -niE "\b(I|I'm|I've|I'll|my|we|our|us)\b" path/to/index.md | grep -viE "style |graph (TB|TD|LR)|fill:#"
     ```
7. **Run the site's standard build check** (`hugo --gc --minify`, per `AGENTS.md`) and fix any failures.
8. **Deliver the draft** for review, noting any TODO (e.g. the cover PNG).

---
name: write-article
description: Creates articles using 16 bundled writing framework prompts (Diataxis tutorial, how-to, reference, explanation, AIDA, PAS, Influence Pieces, Classical Rhetoric, TEA, Thought Pieces, Backward Design, Lesson Planning, Fact-Based Reference, List Articles, Fundamentals, Learn X) plus Comparison, whose rules come from write-comparison-article-create. Picks the best framework, loads it from this skill, and drafts the article; for jeffbaileyblog it also applies hugo/AGENTS.md, the site writing style and SEO rules, places the page bundle in the right section, checks internal links are published, then loops write-review and write-review-apply until the draft scores 9.5 or higher, and verifies the Hugo build. Use when the user says /write:article, asks to write an article, blog post, opinion piece, essay, tutorial, how-to, explanation, reference doc, "Learn X" or "Fundamentals of X" post, or wants a specific writing framework. Triggers on "write article", "create article", "draft post", "write a post about", "I have opinions about", "write tutorial", "write how-to", "write explanation", "write reference doc".
---

# Article Creation

Each framework is a complete prompt in `references/` that defines approach, structure, and quality bar for one article type. This skill picks the framework, gathers what the prompt needs, and, for jeffbaileyblog, wraps the prompt in the site's rules so the draft lands in the right place and builds.

## Frameworks

If the user names a framework, use it. Otherwise use the selection guide below.

| Framework | When to use | File | jeffbaileyblog section |
|-----------|-------------|------|------------------------|
| Tutorial | Learning by doing, guided lesson for beginners | `diataxis-article-tutorials.md` | `how-x` |
| How-to Guide | Task recipe for someone who knows the basics | `diataxis-article-how-to-guides.md` | `how-x` (`troubleshooting` for "Fix: <error>") |
| Reference | Scan-friendly facts, cheat sheets | `diataxis-article-reference.md` | `reference` |
| Explanation | Context, "what is" / "why does", mental models | `diataxis-article-explanation.md` | `what-x` ("what is"), `why-x` ("why") |
| AIDA | Attention, interest, desire, action | `aida.md` | `why-x` |
| Problem-Agitate-Solve | Name a problem, show its cost, give the fix | `problem-agitate-solve.md` | `why-x` or `think-x` |
| Influence Pieces | Change behavior via proof, authority, framing | `influence-pieces.md` | `why-x` |
| Classical Rhetoric | Argue a position with ethos, pathos, logos | `classical-rhetoric.md` | `think-x` |
| TEA | Topic, evidence, analysis | `tea.md` | `reference` or `think-x` |
| Thought Piece | Exploring or arguing an idea in the author's voice | `thought-pieces.md` | `think-x` |
| Backward Design | Outcomes-first instruction | `backward-design.md` | `how-x` |
| Lesson Planning | Bloom's, 5E, Gagne lessons | `lesson-planning.md` | `how-x` |
| Fact-Based Reference | Authoritative lookup documentation | `fact-based-reference.md` | `reference` |
| List Article | Curated collection, "best X for Y" | `a-list.md` | `lists` |
| Fundamentals | "Fundamentals of X" explainer series | `fundamentals.md` | `fundamentals` |
| Learn X | 20/80 of a topic plus curated video, audio, books, links | `learn.md` | `learn-x` |
| Comparison | Decide between 2–4 options ("X vs Y", "which should I pick") | `../write-comparison-article-create/SKILL.md` | `x-vs-x` |

All files live in `references/` except Comparison's, which is the sibling `write-comparison-article-create` skill so its section order and checker stay in one place; nothing is fetched at runtime. If that skill is not installed, say so and stop rather than drafting a comparison without its rules. When a section is unclear, open two or three recent siblings in the candidate folder and match them.

### Selection guide

- "How do I...", "set up", "configure" → How-to Guide
- "Fix: <error message>" → How-to Guide in `troubleshooting`
- "Getting started with...", "walk me through building..." → Tutorial
- "Learn X", "where do I start learning X", "resources for X" → Learn X
- "Fundamentals of X" → Fundamentals
- "What is...", "Why does...", "how does X work" → Explanation
- "Look up...", "cheat sheet", "reference for..." → Reference or Fact-Based Reference
- "I think...", "I have opinions about...", "my take on...", "let's explore..." → Thought Piece. Pick Classical Rhetoric instead when the author wants to win an argument against a named opposing view, and PAS when the piece should end in a concrete fix the reader adopts.
- "You should...", "here's why you need..." → AIDA, PAS, or Influence Pieces
- "The evidence shows..." → TEA
- "Teach someone to..." → Backward Design or Lesson Planning
- "A list of...", "best X for Y" → List Article
- "X vs Y", "which should I pick", "compare X and Y" → Comparison. A list of many options without a head-to-head verdict stays a List Article.

Opinion requests rule out Diataxis frameworks, Fundamentals, and Comparison: those force second person and forbid "I".

### Comparison

The comparison skill's SKILL.md is the framework prompt: read all of it in step 3. It has no `{{variable}}` fields; its inputs are the options, the audience, and 4–6 decision-driving criteria. Then run the workflow below with these changes:

- **Step 3:** also do its "Research facts" step before drafting, keeping a source URL for every version, price, date, and license.
- **Step 5:** front matter adds `diataxis: explanation` and `articletype: comparison`; categories start with `X vs X`; the slug is `a-vs-b[-vs-c]`.
- **Step 6:** draft in its canonical section order and scorecard format, under its "Facts and sourcing" rule (an unsourced claim gets the literal `TODO verify` inside the same sentence, not a separate HTML comment, because its checker matches a link or that text per sentence).
- **After step 7:** run its checker, `python3 <skill-dir>/../write-comparison-article-create/scripts/check_comparison.py <index.md>`, and fix every FAIL. Re-run it after step 8; ai-sanitize must keep the canonical headings.
- **Step 11:** also run the checker with `--build`; it confirms the cards, procon blocks, and single category footer rendered.
- **Step 12:** list every `TODO verify` with the claims to verify.

## Workflow

1. **Understand the request.** Pin down topic, audience, outcome, and destination. Treat the destination as jeffbaileyblog when the user says "the blog" or "my site", or the working directory is that repo (it has `hugo/config.toml`). If the user named a framework, skip step 2.

2. **Choose the framework.** If one framework clearly fits, say which and why in one line and continue. If two fit, present both with the trade-off and ask once; if the user said "just write it", take your recommendation.

3. **Gather inputs in one message.** Read the prompt file, then sort its `{{variable|default="..."}}` fields:
   - Content fields (`subject_area`, `topic_details`, `audience_level`, `list_topic`, `topic_name`, `list_scope`): pre-fill from the request and the repo. Ask only for what you cannot infer, all in one message, and accept "unknown" or "n/a".
   - Mode fields (`framework_selection`, `framework_flavor`, `diataxis_flavor`, `creation_lens`, `hands_on`, `entry_count_range`, `need_search_filter`): decide them yourself and state the choice. The prompts say "Never ask the user to choose a mode", and they are right; these are craft decisions.
   - `writing_style_context`: for jeffbaileyblog, ignore the default; the site style in step 4 sets the voice.
   - **First-person frameworks** (Thought Piece, Classical Rhetoric, PAS, AIDA, Influence Pieces, and any piece in the author's voice): ask, in the same message, for the author's actual position and one or two real stories or examples. These are what make the piece the author's; the framework only arranges them. If the user wants a draft now, write `<!-- TODO(author): your story about <what> -->` where a story belongs. If no position was given, draft a working thesis without "I" and mark it `<!-- TODO(author): confirm or replace this claim with your position -->`. Never invent the author's experiences, opinions, teams, or quotes.

4. **Load the site rules before drafting (jeffbaileyblog only).** Drafting first and patching style later bakes the wrong voice and link form into every paragraph. Read, in this order:
   1. `hugo/AGENTS.md`, top to bottom, following its `##` headings as written (front matter shape, cover images, post structure, links, build verification).
   2. The nearest nested `AGENTS.md` for the target section (for example `hugo/content/blog/fundamentals/AGENTS.md`: title pattern, categories, `series`, `diataxis`, required "Laws, bias, and fallacies" and Glossary sections).
   3. `hugo/content/prompts/writing-style.md` and `hugo/content/prompts/seo-front-matter.md`. These live copies are authoritative; `references/writing-style.md` and `references/seo-front-matter.md` are fallbacks for when the blog repo is not available.

   **Precedence:** nested `AGENTS.md` > `hugo/AGENTS.md` > `writing-style.md` (SEO fields: `seo-front-matter.md`) > framework prompt. Site rules beat framework defaults on:
   - **Tone and voice:** conversational and direct. Tutorials, how-tos, reference, explanation, and Fundamentals use second person and imperatives, never "I". Opinion frameworks use the author's first person.
   - **Link form:** reference-style only, `[text][label]` in the body and `[label]: URL` or `[label]: {{< ref "folder-name" >}}` at the bottom. Never inline links, never `<a href>`, never a bare `ref` in prose, even when a framework example shows one.
   - **Structure:** no H1 in the body. The framework's sections form the main body; open with a short hook intro and close with a conclusion per AGENTS.md "Post structure". Do not add `{{< partial "category_footer" >}}`; `layouts/_default/single.html` already renders it.
   - **Profanity** in the author's notes or drafts is intentional voice; keep it.

   For other destinations, ask about style preferences once and skip the blog-only steps (4, 5, 7, 11).

5. **Place the bundle (jeffbaileyblog).** Path: `hugo/content/blog/<section>/<folder>/index.md`, with the section from the framework table. Keep folder name, `slug`, and the last segment of `url` identical. Confirm the folder does not already exist. Get today's date with `date +%Y-%m-%d` for `date`, `lastmod`, and the `url` path. Use the AGENTS.md front matter shape with `draft: true`, pick `categories` that sibling posts already use, and apply the SEO rules: quoted `description` of 160 characters or fewer, keyword-first title, concrete keywords.

6. **Draft.** Substitute the gathered values and follow the loaded prompt. The framework sets the structure; `references/great-blog-post.md` sets the quality bar for any blog post (so-what, opening, rewrite passes, specificity, evidence). Read it before drafting, then run its pre-publish checklist on the draft before step 7. Site rules still win where it says so. Fact discipline:
   - Do not invent statistics, studies, versions, command flags, quotes, URLs, dates, or anecdotes. Cite a source link for each factual claim, or mark it `<!-- TODO verify: <claim> -->`, or write `[NEEDS FACT: <what>]`.
   - Check commands, config keys, and version numbers against official docs or the tool's `--help` before presenting them as working.
   - Keep a running claims-to-verify list for the delivery note.

7. **Check internal links (jeffbaileyblog).** `{{< ref >}}` resolves by the bundle's folder name, not the front matter `slug` (AGENTS.md says "slug only"; for new posts they match, for older ones they often do not). A ref to a draft breaks the production build, and most blog bundles are drafts. Use the bundled script, run with the Hugo site root:

   ```bash
   python3 <skill-dir>/scripts/blog_links.py find  hugo testing      # published candidates, prints ref "folder"
   python3 <skill-dir>/scripts/blog_links.py check hugo hugo/content/blog/<section>/<folder>/index.md
   ```

   `check` must print only `OK` lines; it exits 1 on missing, draft, future-dated, or ambiguous targets. Replace or drop failing links.

8. **Remove AI tells.** Invoke the `ai-sanitize` skill (`jbb-skills:ai-sanitize` when installed as a plugin) on the draft in edit mode. Site style wins where the two disagree. If it is not installed, say so in the delivery note.

9. **Review loop: reach 9.5.** The draft is not done until a fresh `write-review` gives it a rubric score of 9.5/10 or higher. Save a copy of the draft to a temp dir first (`mktemp -d`), since a new bundle is untracked and git can't show what the loop changed. Then repeat, without asking the user between rounds:
   1. **Review.** Run `write-review` on the draft, passing the framework from step 2 explicitly. Run it in a fresh subagent (Agent tool) when one is available, so the grader is not the agent that wrote and fixed the draft; give it the absolute path and the framework, and ask for the full review back, JSON summary included. Without subagents, run it inline and label every score "self-review". The gate is the rubric `score` in the JSON summary; the blog-post checklist score is reported but does not gate.
   2. **Stop at 9.5 or higher.** The loop passes.
   3. **Apply.** Run `write-review-apply` on that review in loop mode (its "Called from write-article" section): edits in place, no validation or self re-score per round. Copy the result to the temp dir as `round-<n>.md` before the next review.

   Stop below 9.5 when any of these happens, and keep the highest-scoring version on disk (restore its copy if a later round scored lower):
   - five reviews have run;
   - a round applied nothing, because every remaining finding is **Needs your input**, **Your call**, or **Declined**;
   - the score did not rise in two rounds in a row.

   Never raise the score by inventing a fact, source, number, quote, or author experience, and never fill a `TODO(author)`, `[NEEDS FACT]`, or `TODO verify` by guessing; those findings stay with the author even when they are what blocks 9.5. If the loop stops below 9.5, the article is **not done**: step 12 says so first, with the final score, why the loop stopped, and the findings that block 9.5.

10. **Generate the cover image.** Invoke the `generate-cover-image` skill on the reviewed draft; for jeffbaileyblog it builds the Canva design, exports `<slug>.png` into the bundle, and sets `cover.image` and `cover.alt`. Skip it if the user supplied a cover or asked for none. If it cannot generate an image, note the `<slug>.png.prompt.txt` it leaves.

11. **Verify the build (jeffbaileyblog).** Hand off to the `write-validate-article` skill when available; it runs the build, banned-phrase scan, links, and lint. Otherwise check `command -v hugo` (missing: `brew install hugo`, and report "tool missing", not "build failed"), then from `hugo/`:

    ```bash
    out=$(mktemp -d); hugo --buildDrafts --gc --minify -d "$out" && ls "$out/blog/YYYY/MM/DD/<slug>/index.html"
    ```

    `--buildDrafts` is required: the new post is `draft: true` and the site sets `buildDrafts = false`, so a plain `hugo --gc --minify` succeeds without rendering it. Any `REF_NOT_FOUND` or missing `index.html` is a failure to fix before delivering.

12. **Deliver.** Only call the article done when step 9 reached 9.5 and step 11 passed. Report:
    - file path, framework and why, section choice
    - the review loop: score per round (for example `7.8 -> 8.9 -> 9.6`), whether a subagent graded it or it was a self-review, the last saved review path, and, if it stopped below 9.5, why and the findings blocking it
    - the `ai-sanitize` change list
    - cover image path, alt text, and Canva link (or why it was skipped)
    - build or validation result
    - **claims to verify**: every statistic, version, command, and external fact the author should confirm
    - every `TODO(author)` and `[NEEDS FACT]` placeholder the author must fill

## Reference

- `references/*.md`: the 16 framework prompts plus fallback copies of `writing-style.md` and `seo-front-matter.md`.
- `../write-comparison-article-create/SKILL.md` and its `scripts/check_comparison.py`: the Comparison framework and its checker.
- `references/great-blog-post.md`: framework-independent quality guidance and pre-publish checklist, distilled from Ann Handley's *Everybody Writes*.
- `scripts/blog_links.py`: finds published link targets and checks every `ref` in a draft against `hugo list all`.
- Cover prompt: `../generate-cover-image/references/cover-prompt.md`.

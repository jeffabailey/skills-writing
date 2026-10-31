---
name: write-review
description: Reviews an article against one of 17 bundled writing framework rubrics (including X vs Y comparisons) without editing it, plus a blog-post checklist score shared with write-article. Detects the framework from front matter, directory, and structure, or takes it as an argument. Use when the user says /write:review, asks to review an article, evaluate writing quality, check an article against a framework, or get feedback on a draft, and when another skill (such as write-article-revision) needs a framework rubric score. Triggers on "review article", "evaluate writing", "check article", "review draft", "writing feedback", "article quality". With no article specified, reviews the last article created or adjusted.
---

# Article Review

Score an article against the rubric for the framework it was written in, and report findings the author can act on. Every rubric is bundled in `references/`; nothing is fetched at runtime.

**A review never edits.** The article file must be byte-identical before and after. Some rubric text talks about rewrites, diffs, or "conversion"; treat all of it as proposed text in the report, never as edits to the file, and run the review once (no loop toward a target score). Applying changes is the author's job, or a calling skill's (for example `write-article-revision`, or `write-article`'s review loop, which re-runs this skill after each round of fixes; each run is still a single pass).

## Usage

```text
/write:review [article] [framework]
```

* `article`: a file path, pasted text, or URL. Omit it to review the last article created or adjusted (step 1).
* `framework`: optional. Any key or alias from the table below (`how-to`, `fundamentals`, `diataxis-explanation`, `pas`, `a-list.md`, ...). An explicit framework wins over detection. Callers such as `write-article-revision` pass the article's `articletype` here.

## Frameworks

| Key (`articletype`) | Aliases | Rubric | Detection signals (after front matter) |
|---|---|---|---|
| `fundamentals` | fundamentals-x | `fundamentals.md` + base `diataxis-article-explanation.md` | dir `content/blog/fundamentals/`; `series: Fundamentals`; title "Fundamentals of ..." |
| `comparison` | x-vs-x, vs | `comparison.md` + base `diataxis-article-explanation.md` | dir `content/blog/x-vs-x/`; title "X vs Y"; "The short answer" and "Head-to-head" sections |
| `learn` | learn-x | `learn.md` + base `diataxis-article-how-to-guides.md` | dir `content/blog/learn-x/`; "Beyond the Basics" launch-pad section; `learn_x_header` partial |
| `diataxis-tutorial` | tutorial | `diataxis-article-tutorials.md` | "you will build/learn", one guided path, checkpoints for a beginner |
| `diataxis-how-to` | how-to, howto | `diataxis-article-how-to-guides.md` | dirs `how-x/`, `troubleshooting/`; "How do I ...", "Fix: ..."; goal, prerequisites, ordered steps |
| `diataxis-reference` | reference | `diataxis-article-reference.md` | glossary, cheat sheet, uniform entries for lookup |
| `diataxis-explanation` | explanation | `diataxis-article-explanation.md` | dirs `what-x/`, `why-x/`; "What is ...", "Why ..."; mental models, trade-offs |
| `aida` | | `aida.md` | hook, value, desire, explicit call to action |
| `problem-agitate-solve` | pas | `problem-agitate-solve.md` | problem, consequences intensified, then the fix |
| `influence-pieces` | influence | `influence-pieces.md` | aims to change behavior; Cialdini, Fogg, benefit ladder |
| `classical-rhetoric` | rhetoric | `classical-rhetoric.md` | argued thesis balancing ethos, pathos, logos |
| `tea` | | `tea.md` | Topic, Evidence, Analysis sections; cited data with interpretation |
| `thought-pieces` | thought-piece, opinion | `thought-pieces.md` | dir `think-x/`; first-person exploration, multiple perspectives |
| `backward-design` | | `backward-design.md` | outcomes first, then assessments, then activities |
| `lesson-planning` | lesson-plan | `lesson-planning.md` | lesson structure (Bloom's, 5E, Gagne's nine events) |
| `fact-based-reference` | fact-reference, faq | `fact-based-reference.md` | dir `reference/` without `diataxis*`; definitions, FAQ, Cornell notes |
| `a-list` | list, list-x | `a-list.md` | dir `lists/`; title "A List of ..." or "A Big List of ..." |

`references/prompt-index.md` is a one-line summary of what each rubric evaluates.

## Workflow

1. **Resolve the target article.** Use what the user or caller gave you. Convert any path to an absolute path. If no article was given, stop at the first hit:

   1. **This conversation:** the article file (a `content/**/index.md`, or Markdown with front matter) you created or edited most recently in this session. If you touched several, pick the last one edited and list the others so the user can redirect.
   2. **The blog repo:** run `scripts/last-article.sh` (in this skill). It finds the blog repo even when the current directory is elsewhere (`$BLOG_ROOT`, the current git root if it has `content/`, else `~/Projects/websites/jeffbaileyblog`), considers only `content/**/index.md`, checks the working tree first (newest uncommitted or untracked by mtime), then the last commit that touched an article (the most-changed article when a commit touched several), and prints an absolute path plus its source.
   3. **Ask the user** only when both come up empty.

   State the resolved absolute path and how you found it before reviewing.

2. **Determine the framework.** Take the first rule that decides it, and record which signal decided:

   1. An explicit `framework` argument (match keys, aliases, or rubric filenames, case-insensitive).
   2. Front matter `articletype:` (keys above).
   3. Content directory `fundamentals/`, `learn-x/`, or `x-vs-x/`. These beat the `diataxis` field: a Fundamentals or comparison article also carries `diataxis: explanation`, but it gets its own rubric.
   4. Front matter `diataxis:`, `diataxis_type:`, or `documentation_type:` (`tutorial`, `how-to`, `reference`, `explanation`).
   5. The other directory and title signals in the table.
   6. Structure signals in the table.
   7. Still ambiguous between two rubrics: ask once, naming the two candidates and the signals for each.

3. **Load the rubric.** Read each rule file with the Read tool, one call per file (chaining `cat` with `echo =====` fails in zsh, which treats `=word` as a command lookup). Read the rubric file for the framework. For `fundamentals` and `comparison` also read `diataxis-article-explanation.md`, and for `learn` also read `diataxis-article-how-to-guides.md`: the blog rubric's override block and extra checks apply on top of that base rubric, and the base rubric supplies the type gate and output format.

4. **Fill the template variables.** Rubrics open with fields like `{{subject_area|default="technical concepts"}}`. Pre-fill each from the article (subject from the title, audience from front matter or prerequisites), otherwise use the default. Do not stop to ask: the rubrics say to decide and proceed. The only field with an empty default is `list_topic` in `a-list.md`; take it from the title. List the values you used in one line of the report so the user can rerun with overrides.

5. **Apply the review, read-only.** Follow the loaded rubric: type gate, review mode, section checks, scoring. Quote the passage and give the heading or line number for each finding, with exact replacement text where the rubric asks for it. Do not edit the article and do not re-run the review to chase a score, whatever older copies of a rubric say. Do not invent facts, sources, resources, or URLs in recommendations; when a fix needs one, write `[NEEDS FACT: ...]` or `[NEEDS RESOURCE: ...]`.

6. **Blog checks (jeffbaileyblog only).** Apply these when the article lives in the jeffbaileyblog repo or has its Hugo front matter (`type: post`, `categories`, `cover`):
   * Read the blog's live `hugo/content/prompts/writing-style.md` (the bundled `references/writing-style.md` is only the fallback when the live file is missing; the live one is what the author edits, so the bundled copy drifts) and check: no emdashes; the banned-phrase list; voice (Diátaxis types and Learn X are second person and imperative; Fundamentals may use "I" for the author's judgments and experience, but their reader-facing scaffolding uses "you"; first person is right for thought pieces and opinion posts; never "we"/"our"; when the rubric and the live style guide disagree, the live style guide wins); link style. Profanity is intentional voice: never flag it.
   * On a `draft: true` post, a missing cover PNG or empty `cover.alt` is expected, because `write-article` makes the cover after the review loop. Mention it once in the report; don't score it or list it as an issue, in this step or the checklist.
   * Check `title:`, `description:` (160 characters or fewer), and `keywords:` against `seo-front-matter.md`. Prefer the blog's own `hugo/content/prompts/seo-front-matter.md` when it exists; the bundled copy is the fallback.
   * Invoke the `ai-sanitize` skill (`jbb-skills:ai-sanitize` when installed as a plugin) in **report** mode so it lists AI tells without editing. Triage its hits (link titles often trip the Title-Case check) and fold real ones into the issues with locations. If it is not installed, say so and skip it.

7. **Score the blog-post checklist.** The framework rubric judges whether the article does its type's job; it doesn't ask whether the piece is worth reading. `write-article` drafts against the "Pre-publish checklist" at the end of `${CLAUDE_SKILL_DIR}/../write-article/references/great-blog-post.md`, so score every review against the same list; the writer and the reviewer then hold the same bar. Read that section (and the guidance above it when an item is unclear) and mark each item:
   * **PASS** or **FAIL**, with a quoted passage or heading as evidence. A FAIL also becomes an issue in the issue list with its location and a proposed fix, so `write-review-apply` can act on it.
   * **N/A** only when the item can't apply: no opinions to support, no statistics to source. "The draft got a step-away and a rewrite" can't be seen in the text; mark it N/A unless the author said so.
   * The item on `writing-style.md` and `seo-front-matter.md` reuses step 6's result; on non-blog articles mark it N/A.

   Report the score as `Checklist: <passed>/<applicable> (<n> N/A)`. Keep it separate from the rubric score: callers such as `write-article-revision` loop on the rubric score, so folding the checklist into it would move their target. Where an item conflicts with a site rule, the site rule wins (see "Where site rules win" in the same file). If the file is missing (`write-article` not installed), say so and skip this step.

8. **Deliver the review.** Lead with three lines: article (absolute path), framework and the signal that decided it, rubric file(s) loaded. Then use the rubric's own output format: the JSON summary, the overall score, a PASS / NEEDS_IMPROVEMENT / FAIL status for each rubric section with its evidence, the issues with locations, the prioritized improvement plan, and strengths to keep. Add the blog rubric's extra section when it defines one ("Blog-Specific Fixes" for Fundamentals, "Learn X Launch Pad Fixes" for Learn X, "Comparison Fixes" for comparisons). After the rubric sections, add a "Blog-Post Checklist" section: the score line from step 7, then one line per item with its status and evidence. In the JSON summary, add `"checklist": {"passed": <n>, "applicable": <n>, "na": <n>}`. Do not invent numeric per-dimension scores the rubric does not define. End by confirming the article was not modified.

9. **Save the review** so `write-review-apply` can act on it later, even from another session. Write the full review you delivered (the three lead lines, JSON summary, and Markdown review) to the path this prints, outside the blog repo:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/../write-status/scripts/article_status.py" review new <article index.md>
   ```

   Put the rules stamp right after the three lead lines, before the variables line and the JSON summary. It records which rule files the grades came from, so `write-review-apply` can tell later whether the rubric or style guide changed underneath the findings. Let the script compute it (hand-typed hashes are worse than none); pass the rubric file(s) loaded in step 3, and `--no-blog` when step 6 didn't apply:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/rules_stamp.py" stamp <article index.md> <rubric.md> [<base rubric.md>]
   ```

   It prints `Rubric: references/<file> @ <hash>` per rubric, `Style:` and `SEO:` lines for the `writing-style.md` and `seo-front-matter.md` step 6 reads (live blog copy first, bundled fallback), and a `Checklist:` line for step 7's checklist. Paste its output verbatim.

   Saving to that path does not touch the article, so the read-only rule still holds. If the script isn't installed, skip this step and say the review wasn't saved. End the reply with one line offering the follow-up: "Run `/write:review-apply` to apply these fixes."

## Reading scores across rounds

Each review starts with no memory of the last one, so it scores similar text about 0.3 apart and raises new, smaller findings. A change of 0.3 or less between rounds is noise. In 74 saved reviews of 11 articles, the best independent score was 9.4, and loops usually stalled between 9.1 and 9.3.

When someone asks to repeat review and apply until a target score, this skill still does one read-only review per call, and the caller applies these limits, even if the request says "until 9.5":

* Stop after two reviews in a row with no new high, measured against the best score so far, or after five reviews. `write-article` step 9 holds the full loop.
* Only independent reviews count. A self-review is labeled as one and can't reach a target: one 9.5 self-review drew 8.8 from the next grader.
* Report the score history and the plateau plainly. Go further only if the user asks after seeing it, and tell them to expect a similar result.

## Record the run

After finishing on a jeffbaileyblog article, append the run to the ledger that `write-status` reads, so later checks know this skill ran even after transcripts are cleaned up. Do this once per article, even when the result was a failure, and put the outcome in the note:

```bash
python3 "${CLAUDE_SKILL_DIR}/../write-status/scripts/article_status.py" record write-review <article index.md> --note "<one-line result>"
```

If the script isn't there (`write-status` not installed), skip this step.

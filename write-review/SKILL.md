---
name: write-review
description: Reviews articles against 16 bundled writing framework rubrics. Detects the framework from front matter, content directory, and structure (or takes it as an argument), loads the rubric from this skill, and evaluates the article without editing it. Use when the user says /write:review, asks to review an article, evaluate writing quality, check an article against a framework, or get feedback on a draft, and when another skill (such as write-article-revision) needs a framework rubric score. Triggers on "review article", "evaluate writing", "check article", "review draft", "writing feedback", "article quality". With no article specified, reviews the last article created or adjusted.
---

# Article Review

Score an article against the rubric for the framework it was written in, and report findings the author can act on. Every rubric is bundled in `references/`; nothing is fetched at runtime.

**A review never edits.** The article file must be byte-identical before and after. Some rubric text talks about rewrites, diffs, or "conversion"; treat all of it as proposed text in the report, never as edits to the file, and run the review once (no loop toward a target score). Applying changes is the author's job, or a calling skill's (for example `write-article-revision`).

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
   2. Front matter `articletype:` (keys above). `comparison` has no dedicated rubric: fall through to the `diataxis` field, then default to explanation, and say so.
   3. Content directory `fundamentals/` or `learn-x/`. These beat the `diataxis` field: a Fundamentals article also carries `diataxis: explanation`, but it gets the Fundamentals rubric.
   4. Front matter `diataxis:`, `diataxis_type:`, or `documentation_type:` (`tutorial`, `how-to`, `reference`, `explanation`).
   5. The other directory and title signals in the table.
   6. Structure signals in the table.
   7. Still ambiguous between two rubrics: ask once, naming the two candidates and the signals for each.

3. **Load the rubric.** Read the rubric file for the framework. For `fundamentals` also read `diataxis-article-explanation.md`, and for `learn` also read `diataxis-article-how-to-guides.md`: the blog rubric's override block and extra checks apply on top of that base rubric, and the base rubric supplies the type gate and output format.

4. **Fill the template variables.** Rubrics open with fields like `{{subject_area|default="technical concepts"}}`. Pre-fill each from the article (subject from the title, audience from front matter or prerequisites), otherwise use the default. Do not stop to ask: the rubrics say to decide and proceed. The only field with an empty default is `list_topic` in `a-list.md`; take it from the title. List the values you used in one line of the report so the user can rerun with overrides.

5. **Apply the review, read-only.** Follow the loaded rubric: type gate, review mode, section checks, scoring. Quote the passage and give the heading or line number for each finding, with exact replacement text where the rubric asks for it. Do not edit the article and do not re-run the review to chase a score, whatever older copies of a rubric say. Do not invent facts, sources, resources, or URLs in recommendations; when a fix needs one, write `[NEEDS FACT: ...]` or `[NEEDS RESOURCE: ...]`.

6. **Blog checks (jeffbaileyblog only).** Apply these when the article lives in the jeffbaileyblog repo or has its Hugo front matter (`type: post`, `categories`, `cover`):
   * Read `references/writing-style.md` and check: no emdashes; the banned-phrase list; voice (Diátaxis types, Fundamentals, and Learn X are second person and imperative; first person is right for thought pieces and opinion posts; never "we"/"our"); link style. Profanity is intentional voice: never flag it.
   * Check `title:`, `description:` (160 characters or fewer), and `keywords:` against `seo-front-matter.md`. Prefer the blog's own `hugo/content/prompts/seo-front-matter.md` when it exists; the bundled copy is the fallback.
   * Invoke the `ai-sanitize` skill (`jbb-skills:ai-sanitize` when installed as a plugin) in **report** mode so it lists AI tells without editing. Triage its hits (link titles often trip the Title-Case check) and fold real ones into the issues with locations. If it is not installed, say so and skip it.

7. **Deliver the review.** Lead with three lines: article (absolute path), framework and the signal that decided it, rubric file(s) loaded. Then use the rubric's own output format: the JSON summary, the overall score, a PASS / NEEDS_IMPROVEMENT / FAIL status for each rubric section with its evidence, the issues with locations, the prioritized improvement plan, and strengths to keep. Add the blog rubric's extra section when it defines one ("Blog-Specific Fixes" for Fundamentals, "Learn X Launch Pad Fixes" for Learn X). Do not invent numeric per-dimension scores the rubric does not define. End by confirming the article was not modified.

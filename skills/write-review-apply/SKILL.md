---
name: write-review-apply
description: Applies the fixes from a write-review report to the article it reviewed, then validates and re-scores it. Finds the review in this conversation or the saved report from an earlier session (running write-review first if there is none), turns every finding into a fix list, re-checks each against the current style rules and rubric, tests any command or claim the review supplies, applies the ones the article's own content supports, and lists the rest (missing facts, structural calls) for the author instead of inventing anything. Keeps the author's voice and profanity, edits in place only when git holds the original, and reports the score before and after as a labeled self re-score. Use when the user says /write:review-apply, "apply the review", "fix what the review found", "apply those fixes", "do the improvement plan", "address the review feedback" for an article or blog post, or answers yes after write-review offers the follow-up. With no article named, uses the last reviewed or changed article.
---

# Apply an article review

`write-review` scores an article and never touches it. This skill is the other half: it takes that review's findings and makes the changes, so the author gets a better draft and a short list of things only they can decide.

The review is advice, not a script. Some findings carry exact replacement text; some say "add an example" without one; some ask for a fact the article doesn't have; some want the article split or recast. Apply what the article's own material supports, and hand the rest back clearly. A fix that invents a number, a source, or an experience the author never had makes the article worse, however much it raises the score.

## Usage

```text
/write:review-apply [article]
```

`article` is a path to an `index.md` or its bundle folder. With nothing named: the article reviewed most recently in this conversation, else the last article created or changed (`../write-review/scripts/last-article.sh`).

## Workflow

1. **Find the review.** Stop at the first that applies, and say which one you used:
   1. A `write-review` report for this article earlier in this conversation.
   2. The newest saved report. This prints its path, whether it is `current` or `stale`, and both timestamps:

      ```bash
      python3 "${CLAUDE_SKILL_DIR}/../write-status/scripts/article_status.py" review latest <article>
      ```

   3. Neither exists: run `write-review` on the article now (it is read-only and saves its report), then continue. Say you did.

   A `stale` review means the article changed after it was written. Still use it, but check each finding's quoted passage against the current text in step 2; findings whose passage is gone become **already addressed**. A review can also be stale against the rules (the rubric or `writing-style.md` changed since it ran), which `stale` doesn't detect. For a saved report, check its rules stamp (`write-review` writes one under the lead lines):

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/../write-review/scripts/rules_stamp.py" check <saved report> <article>
   ```

   Exit 0 (`rules unchanged`): the findings were graded against today's rules, so skip step 2's rule lookups; still read each finding's quoted passage and decline any that doesn't show the problem it names (a review can misread under unchanged rules). Exit 1 (a rule changed) or 2 (no stamp, including reviews from this conversation and older reports): keep the per-finding re-check, and say which rule file changed.

2. **Build the fix list.** Read the whole article first, then the review. Collect every actionable item from the critical issues, each section marked `NEEDS_IMPROVEMENT` or `FAIL`, the prioritized improvement plan, and any blog-specific section ("Blog-Specific Fixes", "Learn X Launch Pad Fixes"). Merge duplicates (the same problem often appears in three places). Anchor each item to its quoted passage, not its line number: line numbers shift as soon as you apply the first fix. Then run two checks before giving dispositions, because a review is one agent's reading under the rules it had at the time:

   * **Re-check against the current rules** (when step 1's stamp check printed `rules unchanged`, skip the rule lookups but keep the passage check). For every voice, style, or structure finding, look up the rule it relies on in the current rules: the blog's live `hugo/content/prompts/writing-style.md` (it wins; `../write-review/references/writing-style.md` is the bundled fallback) and the rubric for the review's framework in `../write-review/references/` (for Fundamentals, `fundamentals.md`), and, for a finding from the "Blog-Post Checklist" section, its item in `../write-article/references/great-blog-post.md` ("Where site rules win" there says which site rules override it). If the current rules allow what the finding flags, it is **Declined**, citing the rule. If the live `writing-style.md` and the rubric disagree on the point, don't pick one silently: make it **Your call**, quoting both. Example: Fundamentals articles may use "I" for the author's own judgments and experience (`fundamentals.md`, and the "Voice override for Diátaxis articles" in `writing-style.md`), so a finding that converts those sentences to "you" is declined, while "I" in reader-facing scaffolding (the intro's promise, the prerequisites, the wrap-up) is still a valid finding.
   * **Verify what the review supplies.** Replacement text is only as good as what's in it. A command, code change, or regex the review supplies must be run on a small sample in a temp dir (never against the user's repo state) and produce what the article says it produces; if you can't run it, or it fails on a realistic case (a `[bot]` email, a path with spaces, an empty result), it goes to **Needs your input** with the failing case. A technical or factual claim the review supplies that the article doesn't already make (a mechanism, a "why", a history, a number) is a new fact: **Needs your input**, even when it sounds right.

   Give each item one disposition:

   | Disposition | When | What you do |
   |---|---|---|
   | **Apply** | The fix can be made from what the article already says: exact replacement text, a reorder, a tightened passage, a missing transition, a heading fix, a style or voice correction, a front-matter field the review flagged. | Make the change. |
   | **Needs your input** | The fix needs something the article doesn't contain: a fact, number, source, link, example from the author's experience, or a `[NEEDS FACT]` / `[NEEDS RESOURCE]` marker. | Don't write it. List what's needed and where it would go. |
   | **Your call** | The fix changes what the article is: split it in two, change its type or framework, cut a major section, change the thesis, or a type-gate FAIL. | Don't do it. Summarize the trade-off in one or two lines. |
   | **Check** | The finding asks you to verify something ("check whether the theme renders the cover image"), not to change text. | Do the check read-only (built HTML, `hugo list all`, the file tree) and report the result. If it shows a change is needed, give that change its own disposition. |
   | **Already addressed** | The quoted passage is gone or already reads the way the review asked. | Note it. |
   | **Declined** | The finding conflicts with the author's voice or the current rules: it flags profanity, asks for "we", wants an emdash, wants a published post's `url` or `slug` changed, or flags something the current rubric or `writing-style.md` allows. | Note why, citing the rule. |

   When the review gives exact replacement text, use it unless it breaks a site rule, invents a fact, or carries an unverified command or claim; then adapt it (drop the unsupported part) and say how.

3. **Pick the output file.** Same rule as `write-article-revision`: if the article is tracked by git and has no uncommitted changes (`git -C <dir> ls-files --error-unmatch <file>` succeeds and `git -C <dir> status --porcelain -- <file>` prints nothing), edit in place, since git holds the original and the author reviews with `git diff`. Otherwise write the result beside it as `index.revised.md` and leave the original untouched. Either way, save a copy of the starting text to a temp file (`mktemp`) for step 4's change check.

4. **Apply the fixes, highest priority first.** Work through the **Apply** items in the review's priority order (critical issues, then the improvement plan, then section findings).
   * **Scope:** change only the passages a finding names, plus the sentence before and after when a joint needs smoothing. Every other sentence stays byte for byte. Problems you notice that the review didn't raise go under *Noticed, not changed*.
   * **Voice:** keep the author's diction, rhythm, humor, and profanity. Profanity is the voice, not a defect. New sentences should sound like the sentences around them.
   * **Site style (jeffbaileyblog):** follow the same `writing-style.md` as step 2 (live copy first) in every passage you touch: no emdashes, the banned-phrase list, Diátaxis types and Learn X in second person and imperative (Fundamentals keep the author's "I" in judgments; scaffolding is "you"), reference-style links. Never add `{{< partial "category_footer" >}}`.
   * **Front matter:** change `title:`, `description:`, or `keywords:` only when the review flagged them, following the blog's `hugo/content/prompts/seo-front-matter.md` (description 160 characters or fewer). Never change `url`, `slug`, `date`, or `draft`. Leave `lastmod` alone unless the user asks.
   * **Links:** an internal link you add uses `{{< ref "<folder>" >}}` with a published post's folder name from `hugo list all`. Never link a draft.
   * **Change check and line polish:** list exactly what changed, then polish only that:

     ```bash
     python3 "${CLAUDE_SKILL_DIR}/scripts/changed_blocks.py" <starting copy> <result file>
     ```

     It prints each added or rewritten prose block with its line and section, changed code blocks separately, moves, and removed blocks. It FAILs (exit 1) when `url`/`slug`/`date`/`draft` changed, profanity dropped, an emdash or a `category_footer` partial was added, and WARNs on new external URLs or a new "we". Fix every FAIL. Every CODE entry must trace to a finding you verified in step 2; any other change outside a finding's passage gets reverted. Then apply `writing-clearly-and-concisely`'s rules to the PROSE blocks only. Don't run its `check_edit.py` on the whole file here: it treats any code change as a failure, including the ones the review asked for.

5. **Validate.** On jeffbaileyblog, invoke `write-validate-article` on the result (Hugo build first, then front matter, banned phrases, an `ai-sanitize` report, links, and lint). If you wrote `index.revised.md`, swap it in for validation and restore the original afterward, even if validation fails:

   ```bash
   "${CLAUDE_SKILL_DIR}/../write-article-revision/scripts/swap-revision.sh" in  <bundle-dir>
   # ...invoke write-validate-article on <bundle-dir>/index.md...
   "${CLAUDE_SKILL_DIR}/../write-article-revision/scripts/swap-revision.sh" out <bundle-dir>
   ```

   Fix failures and AI tells inside the passages you changed. List the rest as pre-existing. If a tool is missing, say "not run: <tool> missing", separate from checks that ran and failed.

6. **Re-score once, and label it.** Re-score only the rubric sections that contain a changed block (`sections_touched` from step 4, mapped to the rubric's sections), using the same rubric file and framework the first review used; every other section keeps its original status. Report the old and new score and which section statuses moved, labeled **self re-score**: the agent that applied the fixes is grading them, so it leans generous. Offer a fresh `write-review` (in a new session, which saves a new report) when the author wants an independent score. Don't loop to chase a higher score: a second round of fixes on the same article is the author's decision, and repeated passes drift from their voice.

7. **Record the run.**

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/../write-status/scripts/article_status.py" record write-review-apply <article index.md> --note "<old score> -> <new score>"
   ```

   Skip it if the script isn't installed.

## Report

Lead with the file you changed and how to see the diff, then the score, then the lists. Keep each item to one line with its location.

```markdown
**Article:** <absolute path> (edited in place; `git -C <repo> diff -- <path>`) | (wrote <path>/index.revised.md; original untouched)
**Review used:** <this conversation | saved report <path>, current/stale | ran write-review just now>
**Score:** <old> -> <new> (<framework>; self re-score of <n> changed sections). Sections improved: <list>. Still below PASS: <list>.

### Applied (<n>)
| Location | Finding | Change |
|---|---|---|

### Needs your input (<n>)
- <heading/line>: <what fact, source, or example is needed, and what it would fix>

### Your call (<n>)
- <the structural change the review suggested, and the trade-off>

### Checked
- <item>: <what you checked and found>

### Already addressed / Declined
- <item>: <why; for Declined, the rule that allows the text>

### Noticed, not changed
- <issues outside the review's findings>

### Validation
- <changed_blocks.py result, write-validate-article verdict, and anything not run>
```

Omit any section that would be empty, except **Needs your input**: write "None." there so the author knows you looked.

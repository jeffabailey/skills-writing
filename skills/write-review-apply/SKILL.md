---
name: write-review-apply
description: Applies the fixes from a write-review report to the article it reviewed, then validates and re-scores it. Finds the review in this conversation or the saved report from an earlier session (running write-review first if there is none), turns every finding into a fix list, applies the ones the article's own content supports, and lists the rest (missing facts, structural calls) for the author instead of inventing anything. Keeps the author's voice and profanity, edits in place only when git holds the original, and reports the score before and after. Use when the user says /write:review-apply, "apply the review", "fix what the review found", "apply those fixes", "do the improvement plan", "address the review feedback" for an article or blog post, or answers yes after write-review offers the follow-up. With no article named, uses the last reviewed or changed article.
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

   A `stale` review means the article changed after it was written. Still use it, but check each finding's quoted passage against the current text in step 2; findings whose passage is gone become **already addressed**.

2. **Build the fix list.** Read the whole article first, then the review. Collect every actionable item from the critical issues, each section marked `NEEDS_IMPROVEMENT` or `FAIL`, the prioritized improvement plan, and any blog-specific section ("Blog-Specific Fixes", "Learn X Launch Pad Fixes"). Merge duplicates (the same problem often appears in three places). Give each item one disposition:

   | Disposition | When | What you do |
   |---|---|---|
   | **Apply** | The fix can be made from what the article already says: exact replacement text, a reorder, a tightened passage, a missing transition, a heading fix, a style or voice correction, a front-matter field the review flagged. | Make the change. |
   | **Needs your input** | The fix needs something the article doesn't contain: a fact, number, source, link, example from the author's experience, or a `[NEEDS FACT]` / `[NEEDS RESOURCE]` marker. | Don't write it. List what's needed and where it would go. |
   | **Your call** | The fix changes what the article is: split it in two, change its type or framework, cut a major section, change the thesis, or a type-gate FAIL. | Don't do it. Summarize the trade-off in one or two lines. |
   | **Already addressed** | The quoted passage is gone or already reads the way the review asked. | Note it. |
   | **Declined** | The finding conflicts with the author's voice or the site rules: it flags profanity, asks for "we", wants an emdash, or wants a published post's `url` or `slug` changed. | Note why. |

   When the review gives exact replacement text, use it unless it breaks a site rule or invents a fact; then adapt it and say how.

3. **Pick the output file.** Same rule as `write-article-revision`: if the article is tracked by git and has no uncommitted changes (`git -C <dir> ls-files --error-unmatch <file>` succeeds and `git -C <dir> status --porcelain -- <file>` prints nothing), edit in place, since git holds the original and the author reviews with `git diff`. Otherwise write the result beside it as `index.revised.md` and leave the original untouched.

4. **Apply the fixes, highest priority first.** Work through the **Apply** items in the review's priority order (critical issues, then the improvement plan, then section findings).
   * **Scope:** change only the passages a finding names, plus the sentence before and after when a joint needs smoothing. Every other sentence stays byte for byte. Problems you notice that the review didn't raise go under *Noticed, not changed*.
   * **Voice:** keep the author's diction, rhythm, humor, and profanity. Profanity is the voice, not a defect. New sentences should sound like the sentences around them.
   * **Site style (jeffbaileyblog):** read `../write-review/references/writing-style.md` and follow it in every passage you touch: no emdashes, the banned-phrase list, Diátaxis types and Fundamentals and Learn X in second person and imperative, reference-style links. Never add `{{< partial "category_footer" >}}`.
   * **Front matter:** change `title:`, `description:`, or `keywords:` only when the review flagged them, following the blog's `hugo/content/prompts/seo-front-matter.md` (description 160 characters or fewer). Never change `url`, `slug`, `date`, or `draft`. Leave `lastmod` alone unless the user asks.
   * **Links:** an internal link you add uses `{{< ref "<folder>" >}}` with a published post's folder name from `hugo list all`. Never link a draft.
   * **Line polish:** run `writing-clearly-and-concisely` on the sentences you added or rewrote, not the whole article.

5. **Validate.** On jeffbaileyblog, invoke `write-validate-article` on the result (Hugo build first, then front matter, banned phrases, an `ai-sanitize` report, links, and lint). If you wrote `index.revised.md`, swap it in for validation and restore the original afterward, even if validation fails:

   ```bash
   "${CLAUDE_SKILL_DIR}/../write-article-revision/scripts/swap-revision.sh" in  <bundle-dir>
   # ...invoke write-validate-article on <bundle-dir>/index.md...
   "${CLAUDE_SKILL_DIR}/../write-article-revision/scripts/swap-revision.sh" out <bundle-dir>
   ```

   Fix failures and AI tells inside the passages you changed. List the rest as pre-existing. If a tool is missing, say "not run: <tool> missing", separate from checks that ran and failed.

6. **Re-score once.** Invoke `write-review` on the result with the same framework the first review used. Report the old and new score and which section statuses moved. Don't loop to chase a higher score: a second round of fixes on the same article is the author's decision, and repeated passes drift from their voice.

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
**Score:** <old> -> <new> (<framework>). Sections improved: <list>. Still below PASS: <list>.

### Applied (<n>)
| Location | Finding | Change |
|---|---|---|

### Needs your input (<n>)
- <heading/line>: <what fact, source, or example is needed, and what it would fix>

### Your call (<n>)
- <the structural change the review suggested, and the trade-off>

### Already addressed / Declined
- <item>: <why>

### Noticed, not changed
- <issues outside the review's findings>

### Validation
- <write-validate-article verdict, and anything not run>
```

Omit any section that would be empty, except **Needs your input**: write "None." there so the author knows you looked.

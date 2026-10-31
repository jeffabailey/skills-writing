---
name: write-article-complete
description: "Writes an article and finishes it in one request, with no confirmation stops between drafting, review, and fixes. Runs write-article, whose review loop already handles write-review and write-review-apply, and fills in only what that run could not do. Use whenever the user asks to write, draft, or finish a new article and wants review and fixes handled automatically, even if they do not name these skills. To polish an article that already exists, use write-review and write-review-apply."
---

# Complete article workflow

`write-article` already drafts, loops `write-review` and `write-review-apply`, makes the cover, and validates. This skill runs it as one uninterrupted request and closes the one gap it can leave.

## Workflow

1. **Write.** Invoke `write-article` (`jbb-writing-skills:write-article` when installed as a plugin) with the user's complete request and context, and say the user wants no confirmation stops between stages. Two stops stay, because only the user can answer them: facts it cannot infer, and approving the cover in Canva before export.

2. **Check for an independent review.** Read the score history in its delivery note.
   - At least one fresh subagent score: you're done. Don't add a review. The loop has already stopped for a reason, and another round costs about as much as the draft, and edits the article after validation.
   - No independent score (no subagents, a spend limit, or `write-review` missing): run `write-review` and then `write-review-apply` once if they are available, label any score from this session "self-review", then re-run `write-validate-article` on jeffbaileyblog articles because the text changed. If a skill is missing, say which one.

3. **Report.** Pass on `write-article`'s delivery note, with its outcome line first (passed, stopped at a score, or not ready), and add what step 2 did.

If `write-article` produces no article path, stop and report that; don't review an unrelated article. If it creates several articles, ask which one step 2 applies to.

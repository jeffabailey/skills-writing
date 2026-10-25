---
name: write-article-complete
description: "Creates an article and immediately runs the complete writing improvement workflow in one request: write-article, write-review, and write-review-apply, in that order. Use whenever the user asks to write, draft, improve, polish, or finish an article and wants creation plus review and fixes handled automatically, even if they do not name these skills. Do not stop for confirmation between stages."
---

# Complete article workflow

Run the article workflow as one uninterrupted sequence. The goal is to leave the article drafted, independently reviewed, and updated with the fixes that its own material supports.

## Required sequence

Invoke these skills in this exact order:

1. `write-article`
2. `write-review`
3. `write-review-apply`

Use the installed plugin-qualified names when available:

```text
jbb-writing-skills:write-article
jbb-writing-skills:write-review
jbb-writing-skills:write-review-apply
```

If plugin-qualified invocation is unavailable, invoke the skills by their local paths:

```text
@skills/write-article/SKILL.md
@skills/write-review/SKILL.md
@skills/write-review-apply/SKILL.md
```

## Orchestration rules

### 1. Create

Invoke `write-article` with the user's complete request and all provided context. Let it choose the framework, gather only information it cannot infer, create or update the article, and perform its normal blog-specific checks.

Capture the article's absolute path, framework or `articletype`, and any score or review report it produces. If the skill creates multiple articles, stop and ask which one the remaining stages should process.

### 2. Review

After creation finishes, invoke `write-review` on the exact article path from stage 1. Pass the framework explicitly when stage 1 identified one. The review must be a fresh, read-only review; do not treat any review embedded in the creation report as a substitute.

Run this stage even when the creation skill reports a passing score. The purpose of this wrapper is to guarantee the three-stage handoff and produce a current review report for the final application stage.

### 3. Apply

Immediately invoke `write-review-apply` on the same exact article path, using the fresh review from stage 2. Do not ask the user whether to apply the fixes: this combined skill represents standing permission to apply supported fixes.

Preserve `write-review-apply`'s safety rules. It may apply only changes supported by the article and current rules. It must not invent facts, sources, links, statistics, commands, quotes, or author experiences. It must list unsupported findings under `Needs your input` or `Your call` instead of guessing.

## Failure handling

- If `write-article` cannot identify required information, ask for that information before starting later stages.
- If creation fails to produce an article path, stop and report the failure; do not review an unrelated article.
- If `write-review` fails, do not apply stale or guessed findings. Report the failure and offer a standalone review retry.
- If `write-review-apply` fails after editing, report the article path, starting-copy path if available, validation result, and remaining risk.
- If a skill is not installed, report the exact missing skill and stop rather than silently substituting an improvised workflow.

## Final report

Summarize the complete run in this order:

1. Article path and selected framework.
2. Creation result from `write-article`.
3. Fresh review path and rubric score from `write-review`.
4. Application result from `write-review-apply`, including the before/after score when available.
5. Applied fixes, unsupported findings needing the author's input, and validation status.

Make clear that the article was edited in place by `write-review-apply` and that the review itself did not edit it.

---
name: write-fundamentals-article-review
description: Reviews articles against the Fundamentals Article Review rubric from jeffbailey.us. Direct shortcut — skips framework detection. Use when the user says /write:fundamentals-article-review.
---

# Fundamentals Article Review

Direct shortcut to review articles against the Fundamentals Article Review rubric. Skips framework detection — use `/write:review` if you want automatic detection instead.

## CRITICAL: Enforce second person (voice override)

Fundamentals articles are **Diátaxis explanation** content (`diataxis: explanation`). The correct voice is **second person and imperative**, never first person.

- Treat any first-person author voice ("I", "I'm", "I've", "I'll", "my", "me", "we", "our", "us") as a **defect to flag**, and recommend converting it to "you"/imperative.
- Do NOT reward, request, or nudge toward first person. A correctly written second-person article must NOT lose points for lacking an "I" voice.
- Illustrative quotes where first person is incidental are fine only if neutralizing them would lose meaning; otherwise flag them too.

**This overrides the fetched prompt.** The `fundamentals-article-review` prompt says to "respect the first-person voice if requested" and its scoring context may assume first person. That is wrong for this site. The authoritative `hugo/content/prompts/writing-style.md` (Diátaxis voice override) forbids first person for explanation articles, and `writing-style.md` always wins.

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the prompt**:

1. Check if `~/.claude/cache/writing-prompts/fundamentals-article-review.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/fundamentals-article-review/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/fundamentals-article-review.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Receive the article** -- The user provides an article to review, either as text, a file path, or a URL.

2. **Load the review prompt** -- Load the Fundamentals Article Review prompt (slug: `fundamentals-article-review`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from context.

4. **Apply the review** -- Substitute all gathered values into the template variables, then follow the loaded prompt to evaluate the article. The prompt defines scoring dimensions, quality thresholds, and specific checks. **Disregard any prompt guidance that favors or requests first person** — apply the second-person voice override above instead (see "CRITICAL: Enforce second person").

5. **Apply writing style check** -- If the article is for jeffbaileyblog, also load the writing style guide (slug: `writing-style`) using the same caching steps. Flag any style violations. When the fetched prompt and `writing-style.md` disagree, `writing-style.md` wins — in particular the Diátaxis voice override (no first person). Grep for first-person markers and report each hit as a defect:

   ```bash
   grep -niE "\b(I|I'm|I've|I'll|my|we|our|us)\b" path/to/index.md | grep -viE "style |graph (TB|TD|LR)|fill:#"
   ```

6. **Deliver the review** -- Present findings with:
   - Overall score
   - Per-dimension scores with evidence
   - Specific issues with line references where possible
   - Prioritized improvement suggestions
   - Strengths to preserve

## Reference

All writing framework review prompts are maintained at https://jeffbailey.us/prompts/

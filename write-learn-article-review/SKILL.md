---
name: write-learn-article-review
description: Reviews Learn X launch-pad articles against the Learn Article Review rubric from jeffbailey.us. Direct shortcut — skips framework detection. Use when the user says /write:learn-article-review.
---

# Learn Article Review

Direct shortcut to review articles against the Learn Article Review rubric. Skips framework detection — use `/write:review` if you want automatic detection instead.

A Learn X article is a **launch pad to a learning track**: it teaches the 20% of a topic that lets a reader do 80% of the work, then links the best video, audio, books, and online resources. The body is reviewed as a Diátaxis **How-to guide**.

## CRITICAL: Launch pad, 20/80 core, and second-person voice are gates

These can lower the score on their own:

- **Launch pad present:** A `## Learn [Topic] — Beyond the Basics` section MUST link **video** and **books** (plus **audio** and **online** where they exist). A missing video or books group is a critical issue; missing audio is acceptable only when no quality audio resource exists. Resources must be specific and current — named courses, talks, books, and docs, not bare homepages. A `## Related Content` section must also be present.
- **20/80 core explicit:** The article must name and lead with the essential concepts/commands, deferring the long tail to resources. Flag drift into a reference catalog or a full tutorial.
- **Second-person voice:** The correct voice is **second person and imperative**. Treat first-person author voice ("I", "I'm", "I've", "I'll", "my", "me", "we", "our", "us") as a defect to flag — except brief first-person resource recommendations ("I recommend..."), which are fine. Do NOT reward or nudge toward first person; a correctly written second-person article must NOT lose points for lacking an "I" voice. The authoritative `hugo/content/prompts/writing-style.md` Diátaxis voice override wins over any sibling article's first-person style.

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the prompt**:

1. Check if `~/.claude/cache/writing-prompts/learn-article-review.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/learn-article-review/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/learn-article-review.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Receive the article** -- The user provides an article to review, either as text, a file path, or a URL.

2. **Load the review prompt** -- Load the Learn Article Review prompt (slug: `learn-article-review`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from context.

4. **Apply the review** -- Substitute all gathered values into the template variables, then follow the loaded prompt to evaluate the article. The prompt wraps the Diátaxis How-to review rubric and adds Learn-X-specific checks (launch pad, 20/80 core, structure and conventions). Apply the gates in "CRITICAL" above.

5. **Apply writing style check** -- If the article is for jeffbaileyblog, also load the writing style guide (slug: `writing-style`) using the same caching steps. Flag any style violations. When the fetched prompt and `writing-style.md` disagree, `writing-style.md` wins. Grep for first-person markers and report each non-recommendation hit as a defect:

   ```bash
   grep -niE "\b(I|I'm|I've|I'll|my|we|our|us)\b" path/to/index.md | grep -viE "style |graph (TB|TD|LR)|fill:#"
   ```

6. **Deliver the review** -- Present findings with:
   - Overall score
   - Per-dimension scores with evidence
   - Specific issues with line references where possible
   - A dedicated check on the launch pad (which modalities are missing or weak, with concrete resources to add) and the 20/80 core
   - Prioritized improvement suggestions
   - Strengths to preserve

## Reference

All writing framework review prompts are maintained at https://jeffbailey.us/prompts/

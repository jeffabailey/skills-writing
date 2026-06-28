---
name: write-fundamentals-article-create
description: Creates foundational concept articles using the Fundamentals Article Create prompt from jeffbailey.us. Direct shortcut — skips framework selection. Use when the user says /write:fundamentals-article-create.
---

# Fundamentals Article Create

Direct shortcut to create articles using the Fundamentals Article Create framework. Skips framework selection — use `/write:article` if you want recommendations instead.

## CRITICAL: No first person (voice override)

Fundamentals articles are **Diátaxis explanation** content (`diataxis: explanation`). They MUST be written in **second person and imperative voice**, never first person.

- Do NOT use "I", "I'm", "I've", "I'll", "my", "me", "we", "our", "us" in the article's own voice.
- Use "you" for outcomes ("you can rebuild any transformation") and bare imperatives for actions ("Pick one source", "Add a few tests").
- This applies even inside illustrative quotes where first person is incidental — neutralize them.

**This overrides the fetched prompt.** The `fundamentals-article-create` prompt (and several existing `fundamentals-x` sibling articles) say "write in first person." That instruction is wrong for this site. The authoritative `hugo/content/prompts/writing-style.md` (Diátaxis voice override) forbids first person for explanation articles, and `writing-style.md` always wins. Write in second person from the first draft — do not write it in first person and convert later, and do not copy the siblings' first-person voice.

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the prompt**:

1. Check if `~/.claude/cache/writing-prompts/fundamentals-article-create.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/fundamentals-article-create/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/fundamentals-article-create.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Understand the request** -- Ask the user what they want to write about, who the audience is, and what outcome they want.

2. **Load the prompt** -- Load the Fundamentals Article Create prompt (slug: `fundamentals-article-create`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the user's initial request.

4. **Apply the prompt** -- Substitute all gathered values into the template variables, then follow the loaded prompt instructions to create the article. **Ignore any "write in first person" instruction in the prompt** — apply the second-person voice override above instead (see "CRITICAL: No first person").

5. **Apply writing style** -- If the article is for jeffbaileyblog, also load the writing style guide (slug: `writing-style`) using the same caching steps. When the fetched prompt and `writing-style.md` disagree, `writing-style.md` wins — in particular the Diátaxis voice override (no first person).

6. **Scan for first person before delivering** -- Grep the drafted article for first-person markers and fix every hit in the article's own voice:

   ```bash
   grep -niE "\b(I|I'm|I've|I'll|my|we|our|us)\b" path/to/index.md | grep -viE "style |graph (TB|TD|LR)|fill:#"
   ```

   Treat any author-voice hit as a blocker, not a suggestion.

7. **Deliver the draft** -- Present the article draft to the user for review.

## Reference

All writing framework prompts are maintained at https://jeffbailey.us/prompts/

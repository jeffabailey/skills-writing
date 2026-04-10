---
name: write-influence-pieces-article-create
description: Creates persuasion and influence articles using the Influence Pieces Article Create prompt from jeffbailey.us. Direct shortcut — skips framework selection. Use when the user says /write:influence-pieces-article-create.
---

# Influence Pieces Article Create

Direct shortcut to create articles using the Influence Pieces Article Create framework. Skips framework selection — use `/write:article` if you want recommendations instead.

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the prompt**:

1. Check if `~/.claude/cache/writing-prompts/influence-pieces-article-create.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/influence-pieces-article-create/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/influence-pieces-article-create.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Understand the request** -- Ask the user what they want to write about, who the audience is, and what outcome they want.

2. **Load the prompt** -- Load the Influence Pieces Article Create prompt (slug: `influence-pieces-article-create`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the user's initial request.

4. **Apply the prompt** -- Substitute all gathered values into the template variables, then follow the loaded prompt instructions to create the article.

5. **Apply writing style** -- If the article is for jeffbaileyblog, also load the writing style guide (slug: `writing-style`) using the same caching steps.

6. **Deliver the draft** -- Present the article draft to the user for review.

## Reference

All writing framework prompts are maintained at https://jeffbailey.us/prompts/

---
name: write-idea-storm
description: Brainstorms article ideas using the Idea Storm prompt from jeffbailey.us. Direct shortcut — use when the user says /write:idea-storm.
---

# Idea Storm

Direct shortcut to the Idea Storm prompt. Skips prompt selection — use `/write:ideate` for the general ideation workflow instead.

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the prompt**:

1. Check if `~/.claude/cache/writing-prompts/idea-storm.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/idea-storm/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/idea-storm.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Understand the context** -- Ask the user about their subject area, audience, existing content, and goals. What gap are they trying to fill?

2. **Load the prompt** -- Load the Idea Storm prompt (slug: `idea-storm`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the user's context.

4. **Apply the prompt** -- Substitute all gathered values, then follow the loaded prompt to run a structured brainstorming session.

5. **Filter and prioritize** -- Help the user evaluate generated ideas against their goals, audience, and existing content.

6. **Recommend frameworks** -- For the top ideas, suggest which writing framework from `/write:article` would be the best fit.

## Reference

Ideation prompts are maintained at https://jeffbailey.us/prompts/

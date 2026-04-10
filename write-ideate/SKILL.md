---
name: write-ideate
description: Brainstorms article ideas and content strategies using structured ideation prompts from jeffbailey.us. Use when the user says /write:ideate, wants to brainstorm topics, generate article ideas, explore content angles, or needs creative inspiration for writing. Triggers on "brainstorm", "idea storm", "article ideas", "content ideas", "what should I write about", "topic ideas".
---

# Writing Ideation

Generate article ideas and content strategies using structured brainstorming techniques. Fetches ideation prompts from jeffbailey.us.

## Available Prompts

| Prompt | Purpose | Slug |
|--------|---------|------|
| Idea Storm | Divergent thinking, perspective shifting, constraint removal, analogous thinking | `idea-storm` |

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load a prompt** (replace `{slug}` with the prompt slug from the table above):

1. Check if `~/.claude/cache/writing-prompts/{slug}.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/{slug}/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/{slug}.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Understand the context** -- Ask the user about their subject area, audience, existing content, and goals. What gap are they trying to fill? What topics interest them?

2. **Load the ideation prompt** -- Load the Idea Storm prompt (slug: `idea-storm`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the user's context.

4. **Apply the prompt** -- Substitute all gathered values, then follow the loaded prompt to run a structured brainstorming session. The prompt defines techniques for generating diverse, non-obvious ideas.

5. **Filter and prioritize** -- Help the user evaluate generated ideas against their goals, audience, and existing content. Identify which ideas have the most potential.

6. **Recommend frameworks** -- For the top ideas, suggest which writing framework from `write-article` would be the best fit (e.g., "This topic works best as a Diataxis Explanation" or "This is a natural AIDA piece").

7. **Hand off** -- When the user selects an idea, they can use `/write:article` to create it or `/write:strategy` for deeper strategic analysis first.

## Reference

Ideation prompts are maintained at https://jeffbailey.us/prompts/

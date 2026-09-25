---
name: write-ideate
description: Brainstorms article ideas and content strategies using structured ideation prompts bundled in this skill. Use when the user says /write:ideate, wants to brainstorm topics, generate article ideas, explore content angles, or needs creative inspiration for writing. Triggers on "brainstorm", "idea storm", "article ideas", "content ideas", "what should I write about", "topic ideas".
---

# Writing Ideation

Generate article ideas and content strategies using structured brainstorming techniques. Fetches ideation prompts bundled in this skill.

## Available Prompts

| Prompt | Purpose | Slug |
|--------|---------|------|
| Idea Storm | Divergent thinking, perspective shifting, constraint removal, analogous thinking | `idea-storm` |

## Loading a Prompt

Every prompt this skill needs is bundled in `references/`. Read the file directly:

* `references/idea-storm.md`
* `references/writing-style.md`

There is no network fetch and no cache. The files on disk are the source of truth.

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

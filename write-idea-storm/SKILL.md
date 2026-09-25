---
name: write-idea-storm
description: Brainstorms article ideas using the Idea Storm prompt bundled in this skill. Direct shortcut — use when the user says /write:idea-storm.
---

# Idea Storm

Direct shortcut to the Idea Storm prompt. Skips prompt selection — use `/write:ideate` for the general ideation workflow instead.

## Loading a Prompt

Every prompt this skill needs is bundled in `references/`. Read the file directly:

* `references/idea-storm.md`
* `references/writing-style.md`

There is no network fetch and no cache. The files on disk are the source of truth.

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

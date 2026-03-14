---
name: write-ideate
description: Brainstorms article ideas and content strategies using structured ideation prompts from jeffbailey.us. Use when the user says /write:ideate, wants to brainstorm topics, generate article ideas, explore content angles, or needs creative inspiration for writing. Triggers on "brainstorm", "idea storm", "article ideas", "content ideas", "what should I write about", "topic ideas".
---

# Writing Ideation

Generate article ideas and content strategies using structured brainstorming techniques. Fetches ideation prompts from jeffbailey.us.

## Available Prompts

| Prompt | Purpose | URL |
|--------|---------|-----|
| Idea Storm | Divergent thinking, perspective shifting, constraint removal, analogous thinking | `https://jeffbailey.us/prompts/idea-storm/` |

## Workflow

1. **Understand the context** -- Ask the user about their subject area, audience, existing content, and goals. What gap are they trying to fill? What topics interest them?

2. **Fetch the ideation prompt** -- Use WebFetch to retrieve the Idea Storm prompt from the URL above.

3. **Apply the prompt** -- Follow the fetched prompt to run a structured brainstorming session. The prompt defines techniques for generating diverse, non-obvious ideas.

4. **Filter and prioritize** -- Help the user evaluate generated ideas against their goals, audience, and existing content. Identify which ideas have the most potential.

5. **Recommend frameworks** -- For the top ideas, suggest which writing framework from `write-article` would be the best fit (e.g., "This topic works best as a Diataxis Explanation" or "This is a natural AIDA piece").

6. **Hand off** -- When the user selects an idea, they can use `/write:article` to create it or `/write:strategy` for deeper strategic analysis first.

## Reference

Ideation prompts are maintained at https://jeffbailey.us/prompts/

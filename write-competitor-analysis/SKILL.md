---
name: write-competitor-analysis
description: Competitive landscape analysis using the Competitor Analysis prompt bundled in this skill. Direct shortcut — use when the user says /write:competitor-analysis.
---

# Competitor Analysis

Direct shortcut to the Competitor Analysis prompt. Skips prompt selection — use `/write:strategy` for the general strategy workflow instead.

## Loading a Prompt

Every prompt this skill needs is bundled in `references/`. Read the file directly:

* `references/competitor-analysis.md`
* `references/writing-style.md`

There is no network fetch and no cache. The files on disk are the source of truth.

## Workflow

1. **Understand the objective** -- Ask the user about their market, competitors, and what strategic questions they need answered.

2. **Load the prompt** -- Load the Competitor Analysis prompt (slug: `competitor-analysis`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the user's initial request.

4. **Apply the prompt** -- Substitute all gathered values, then follow the loaded prompt to produce the competitive landscape analysis.

5. **Deliver actionable output** -- Present findings with clear priorities, opportunity gaps, and next steps.

## Reference

Strategy prompts are maintained at https://jeffbailey.us/prompts/

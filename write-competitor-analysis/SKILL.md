---
name: write-competitor-analysis
description: Competitive landscape analysis using the Competitor Analysis prompt from jeffbailey.us. Direct shortcut — use when the user says /write:competitor-analysis.
---

# Competitor Analysis

Direct shortcut to the Competitor Analysis prompt. Skips prompt selection — use `/write:strategy` for the general strategy workflow instead.

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the prompt**:

1. Check if `~/.claude/cache/writing-prompts/competitor-analysis.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/competitor-analysis/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/competitor-analysis.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

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

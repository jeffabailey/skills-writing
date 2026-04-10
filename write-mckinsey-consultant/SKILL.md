---
name: write-mckinsey-consultant
description: McKinsey-style growth analysis using the McKinsey Consultant prompt from jeffbailey.us. Direct shortcut — use when the user says /write:mckinsey-consultant.
---

# McKinsey Consultant

Direct shortcut to the McKinsey Consultant prompt. Skips prompt selection — use `/write:strategy` for the general strategy workflow instead.

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the prompt**:

1. Check if `~/.claude/cache/writing-prompts/mckinsey-consultant.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/mckinsey-consultant/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/mckinsey-consultant.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Understand the business context** -- Ask the user about their business, current growth stage, and what strategic questions they need answered.

2. **Load the prompt** -- Load the McKinsey Consultant prompt (slug: `mckinsey-consultant`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the user's initial request.

4. **Apply the prompt** -- Substitute all gathered values, then follow the loaded prompt to produce the growth scorecard, bottleneck analysis, and roadmap.

5. **Deliver actionable output** -- Present findings with growth scorecard, bottleneck identification, quick wins, and 90-day roadmap.

## Reference

Strategy prompts are maintained at https://jeffbailey.us/prompts/

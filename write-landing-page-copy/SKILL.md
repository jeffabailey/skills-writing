---
name: write-landing-page-copy
description: Creates landing page copy using the Landing Page Copy prompt from jeffbailey.us. Direct shortcut — use when the user says /write:landing-page-copy.
---

# Landing Page Copy

Direct shortcut to the Landing Page Copy prompt. Skips prompt selection — use `/write:copy` for the general copy workflow instead.

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the prompt**:

1. Check if `~/.claude/cache/writing-prompts/landing-page-copy.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/landing-page-copy/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/landing-page-copy.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Understand the product/service** -- Ask the user about what they are selling or promoting, who the target audience is, what the key value proposition is, and what action they want the reader to take.

2. **Load the prompt** -- Load the Landing Page Copy prompt (slug: `landing-page-copy`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the user's initial request.

4. **Apply the prompt** -- Substitute all gathered values, then follow the loaded prompt to create the copy. The prompt defines hook structure, persuasion law selection, section design, and CTA placement.

5. **Deliver the copy** -- Present the draft with clear sections. Highlight which persuasion techniques were used and why.

## Reference

Copy prompts are maintained at https://jeffbailey.us/prompts/

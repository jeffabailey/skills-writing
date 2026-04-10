---
name: write-copy
description: Creates marketing and landing page copy using persuasion frameworks from jeffbailey.us. Use when the user says /write:copy, needs landing page copy, wants marketing text, asks for sales copy, or needs conversion-focused writing. Triggers on "landing page", "marketing copy", "sales copy", "conversion copy", "copywriting", "CTA", "call to action".
---

# Marketing Copy

Create high-converting marketing and landing page copy using structured persuasion frameworks from jeffbailey.us.

## Available Prompts

| Prompt | Purpose | Slug |
|--------|---------|------|
| Landing Page Copy | 48 Laws of Power applied to copywriting: hook, persona, persuasive sections, CTA, social proof | `landing-page-copy` |

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

1. **Understand the product/service** -- Ask the user about what they are selling or promoting, who the target audience is, what the key value proposition is, and what action they want the reader to take.

2. **Load the prompt** -- Load the Landing Page Copy prompt (slug: `landing-page-copy`) using the caching steps above.

3. **Gather variables** -- The loaded prompt contains template variables in the format `{{variable_name|default="value"}}`. For each variable:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the user's initial request.

4. **Apply the prompt** -- Substitute all gathered values into the template variables, then follow the loaded prompt to create the copy. The prompt defines hook structure, persuasion law selection, section design, and CTA placement.

5. **Deliver the copy** -- Present the draft with clear sections. Highlight which persuasion techniques were used and why.

## Reference

Copy prompts are maintained at https://jeffbailey.us/prompts/

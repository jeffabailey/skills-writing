---
name: write-copy
description: Creates marketing and landing page copy using persuasion frameworks bundled in this skill. Use when the user says /write:copy, needs landing page copy, wants marketing text, asks for sales copy, or needs conversion-focused writing. Triggers on "landing page", "marketing copy", "sales copy", "conversion copy", "copywriting", "CTA", "call to action".
---

# Marketing Copy

Create high-converting marketing and landing page copy using structured persuasion frameworks bundled in this skill.

## Available Prompts

| Prompt | Purpose | Slug |
|--------|---------|------|
| Landing Page Copy | 48 Laws of Power applied to copywriting: hook, persona, persuasive sections, CTA, social proof | `landing-page-copy` |

## Loading a Prompt

Every prompt this skill needs is bundled in `references/`. Read the file directly:

* `references/landing-page-copy.md`
* `references/seo-front-matter.md`
* `references/writing-style.md`

There is no network fetch and no cache. The files on disk are the source of truth.

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

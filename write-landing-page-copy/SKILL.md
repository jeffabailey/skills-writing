---
name: write-landing-page-copy
description: Creates landing page copy using the Landing Page Copy prompt bundled in this skill. Direct shortcut — use when the user says /write:landing-page-copy.
---

# Landing Page Copy

Direct shortcut to the Landing Page Copy prompt. Skips prompt selection — use `/write:copy` for the general copy workflow instead.

## Loading a Prompt

Every prompt this skill needs is bundled in `references/`. Read the file directly:

* `references/landing-page-copy.md`
* `references/seo-front-matter.md`
* `references/writing-style.md`

There is no network fetch and no cache. The files on disk are the source of truth.

## Workflow

1. **Understand the product/service** -- Ask the user about what they are selling or promoting, who the target audience is, what the key value proposition is, and what action they want the reader to take.

2. **Read the prompt** -- Load the Landing Page Copy prompt, `references/landing-page-copy.md`.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the user's initial request.

4. **Apply the prompt** -- Substitute all gathered values, then follow the loaded prompt to create the copy. The prompt defines hook structure, persuasion law selection, section design, and CTA placement.

5. **Remove AI tells** -- Invoke the `ai-sanitize` skill (from [jeffabailey/skills](https://github.com/jeffabailey/skills); `jbb-skills:ai-sanitize` when installed as a plugin) on the copy in edit mode. Persuasive copy is where AI tells cluster: "elevate", "seamless", "supercharge", vague taglines ("The future of..."), eyebrow labels over headings, and emoji decoration. It replaces them with claims only this product can make. When the copy ships as page markup or a mockup, include the UI and graphics references too. If a tell cannot be replaced without a fact the user has not given, flag it instead of inventing one. If it is not installed, say so in the delivery note and skip this step.

6. **Deliver the copy** -- Present the draft with clear sections. Highlight which persuasion techniques were used and why.

## Reference

Copy prompts are maintained at https://jeffbailey.us/prompts/

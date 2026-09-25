---
name: write-debug
description: Systematic debugging and bug minimization using structured analysis bundled in this skill. Use when the user says /write:debug, needs to minimize a bug report, wants structured debugging help, or asks for systematic issue analysis. Triggers on "bug report", "minimize bug", "debug", "reproduce bug", "isolate issue".
---

# Bug Minimization

Apply structured debugging methodology to isolate, reproduce, and document bugs using the bug minimizer prompt bundled in this skill.

## Available Prompts

| Prompt | Purpose | Slug |
|--------|---------|------|
| Bug Minimizer | Systematic debugging: isolate, reproduce, gather evidence, hypothesize, test | `bug-minimizer` |

## Loading a Prompt

Every prompt this skill needs is bundled in `references/`. Read the file directly:

* `references/bug-minimizer.md`
* `references/writing-style.md`

There is no network fetch and no cache. The files on disk are the source of truth.

## Workflow

1. **Receive the bug report** -- The user provides a bug description, reproduction steps, or observed behavior.

2. **Load the prompt** -- Load the Bug Minimizer prompt (slug: `bug-minimizer`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the bug report.

4. **Apply the prompt** -- Substitute all gathered values, then follow the loaded prompt to systematically work through the debugging methodology: isolation, reproduction, evidence gathering, hypothesis formation, and testing.

5. **Deliver the analysis** -- Present a structured bug analysis with minimal reproduction case, root cause hypothesis, and recommended fix.

## Reference

Debugging prompts are maintained at https://jeffbailey.us/prompts/

---
name: write-bug-minimizer
description: Systematic bug minimization and debugging using the Bug Minimizer prompt from jeffbailey.us. Direct shortcut — use when the user says /write:bug-minimizer.
---

# Bug Minimizer

Direct shortcut to the Bug Minimizer prompt. Skips prompt selection — use `/write:debug` for the general debug workflow instead.

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the prompt**:

1. Check if `~/.claude/cache/writing-prompts/bug-minimizer.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/bug-minimizer/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/bug-minimizer.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

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

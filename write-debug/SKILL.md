---
name: write-debug
description: Systematic debugging and bug minimization using structured analysis from jeffbailey.us. Use when the user says /write:debug, needs to minimize a bug report, wants structured debugging help, or asks for systematic issue analysis. Triggers on "bug report", "minimize bug", "debug", "reproduce bug", "isolate issue".
---

# Bug Minimization

Apply structured debugging methodology to isolate, reproduce, and document bugs using the bug minimizer prompt from jeffbailey.us.

## Available Prompts

| Prompt | Purpose | URL |
|--------|---------|-----|
| Bug Minimizer | Systematic debugging: isolate, reproduce, gather evidence, hypothesize, test | `https://jeffbailey.us/prompts/bug-minimizer/` |

## Workflow

1. **Receive the bug report** -- The user provides a bug description, reproduction steps, or observed behavior.

2. **Fetch the prompt** -- Use WebFetch to retrieve the Bug Minimizer prompt from the URL above.

3. **Apply the prompt** -- Follow the fetched prompt to systematically work through the debugging methodology: isolation, reproduction, evidence gathering, hypothesis formation, and testing.

4. **Deliver the analysis** -- Present a structured bug analysis with minimal reproduction case, root cause hypothesis, and recommended fix.

## Reference

Debugging prompts are maintained at https://jeffbailey.us/prompts/

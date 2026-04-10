---
name: write-validate-article
description: Validates a Markdown article by running both link checking (lychee) and Markdown linting (markdownlint). Use when the user says /write:validate-article, wants to validate an article, check article quality, or run all checks on a Markdown file.
---

# Validate Article

Run all validation checks against a Markdown article file: link checking and Markdown linting.

## Workflow

1. **Identify the tagged file** -- The user provides a file path as the argument. If no file is provided, ask which file to validate.

2. **Run link checking** -- Invoke the `write-check-links` skill against the tagged file.

3. **Run Markdown linting** -- Invoke the `write-run-markdown-lint` skill against the tagged file.

4. **Report results** -- Summarize the combined results. If both checks pass, confirm the article is valid. If either check fails, present all errors together and offer to fix them.

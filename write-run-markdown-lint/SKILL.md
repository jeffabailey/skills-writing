---
name: write-run-markdown-lint
description: Runs markdownlint against a file using the user's markdownlint-cli2 config. Use when the user says /write:run-markdown-lint, wants to lint a Markdown file, check Markdown formatting, or validate Markdown style.
---

# Run Markdown Lint

Validate a Markdown file using [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) with the user's configuration.

## Workflow

1. **Identify the tagged file** -- The user provides a file path as the argument. If no file is provided, ask which file to lint.

2. **Run markdownlint** -- Execute:

   ```bash
   markdownlint --config ${HOME}/Shell/.markdownlint-cli2.jsonc {tagged-file} && echo 'Success' || (echo 'Error'; exit 1)
   ```

3. **Report results** -- If the command succeeds, confirm the file passed linting. If it fails, present the errors to the user and offer to fix them.

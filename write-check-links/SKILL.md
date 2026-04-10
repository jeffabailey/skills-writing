---
name: write-check-links
description: Checks links in a file using lychee. Runs lychee with the Hugo site's lychee.toml config against the specified file. Use when the user says /write:check-links, wants to validate links, check for broken links, or verify URLs in a file.
---

# Check Links

Validate links in a file using [lychee](https://lychee.cli.rs/) with the Hugo site's configuration.

## Workflow

1. **Identify the tagged file** -- The user provides a file path as the argument. If no file is provided, ask which file to check.

2. **Find the active Hugo folder** -- Locate the Hugo site root by searching upward from the tagged file for a directory containing `hugo.toml`, `hugo.yaml`, or `hugo.json`. If the tagged file is not inside a Hugo site, search the current working directory and its parents instead. The Hugo folder is the directory containing the Hugo config file.

3. **Run lychee** -- Execute:

   ```bash
   lychee --config {hugo-folder}/lychee.toml {tagged-file}
   ```

4. **Report results** -- Present the lychee output to the user. Summarize any broken or problematic links found.

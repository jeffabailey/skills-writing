---
name: write-run-markdown-lint
description: Lints a Markdown file with markdownlint-cli2 and the user's config (project .markdownlint-cli2.jsonc, else ~/Shell/.markdownlint-cli2.jsonc), reports findings grouped by rule, and flags results that mean the config was not applied. Use when the user says /write:run-markdown-lint, wants to lint a Markdown file, check Markdown formatting or style, or asks "what's actually wrong" with a draft's Markdown.
---

# Run Markdown Lint

Lint one Markdown file with [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) and the user's config, then report what is really wrong. This skill is read-only unless the user approves fixes.

## Why the tool choice matters

Use `markdownlint-cli2` only. Never fall back to `markdownlint` (markdownlint-cli v1, which Homebrew installs). The user's config is a cli2 options file with the rules nested under `"config"`. v1 treats that key as an unknown rule, drops every setting, and lints with defaults. The result looks plausible and is wrong both ways: it reports MD013 at 80 columns, MD052 on Hugo `{{< ref >}}` shortcodes, MD010, and MD034, which the user turned off or relaxed. It also flags correct `*` lists under MD004 and lets `-` lists pass. On a clean published article, v1 reports 83 findings where cli2 reports 0.

## Workflow

1. **Get the file.** Use the path the user gave. If they gave none, ask which file to lint. Lint the file where it is; do not copy it.

2. **Run the bundled script.**

   ```bash
   bash <skill-dir>/scripts/lint.sh <file> [--config <path>]
   ```

   The script handles the steps that are easy to get wrong:
   * **Preflight:** it runs `markdownlint-cli2` if it is on PATH, otherwise `npx -y markdownlint-cli2@0.18.1`. If neither is available it prints install commands and exits `127` with `TOOL MISSING`.
   * **Config discovery:** it uses `--config` when passed. Otherwise it walks up from the file, stopping at the git root, to the nearest `.markdownlint-cli2.jsonc` or `.yaml`, then tries `~/Shell/.markdownlint-cli2.jsonc`. It prints `CONFIG:` with the path, any symlink target, and which source it came from.
   * **Output:** it prints the raw cli2 output, a `RESULT:` line, and a `BY RULE:` count. If MD013 or MD052 fire, it prints a warning.

   Exit codes: `0` pass, `1` findings, `2` usage or tool error, `127` tool missing.

   If you cannot run the script, run the same command by hand: `markdownlint-cli2 --config <cfg> ":<file>"`, or with `npx -y markdownlint-cli2@0.18.1` in place of `markdownlint-cli2`.

3. **Report.** Keep it short, in this order:
   * **Tool and config:** say which tool ran and which config was used, with its source (project or `~/Shell`). If no config was found, say that defaults applied.
   * **Verdict:** pass, or N findings.
   * **Findings grouped by rule:** one heading or bullet per rule (for example `MD004/ul-style`), with line numbers and the expected vs actual value. Put rules with more hits first.
   * **Tool missing (exit 127):** say the linter is not installed, give the install command (`brew install markdownlint-cli2` or `npm install -g markdownlint-cli2@0.18.1`), and say no lint ran. Do not call this a lint failure, and do not report the file as passing.
   * **Tool error (exit 2):** quote the error. Do not invent findings.

4. **Sanity-check before trusting results.** The user's config sets MD013 to 1200 columns, sets MD004 to `asterisk`, sets MD007 indent to 4, and turns off MD052, MD034, and the whitespace group (MD009, MD010, MD012, and others). So with that config:
   * If MD013 (at 80 columns) or MD052 appears, the config was not applied. Say so plainly, do not present those findings as issues, and recheck the `CONFIG:` line.
   * If MD004 says `Expected: dash` on `*` items, the config was not applied. Never tell the user to change `*` lists to `-`.

5. **Offer fixes only for rules that fired under the applied config.** Describe each fix, such as "change the two `-` items on lines 35-36 to `*`", and wait for a yes before editing. Prefer targeted edits. If you use `markdownlint-cli2 --fix`, pass the same `--config`, since `--fix` rewrites the file in place. Do not "fix" rules the config disables. Do not touch prose; profanity and wording are the author's voice, not lint.

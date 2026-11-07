---
name: write-optimize-code
description: Optimizes the code in a Markdown article by reading every fenced block (```bash, ```python, ```yaml, ...) together as one program, then making it correct, consistent across blocks, as simple as it can be, and maintainable by the review-maintainability rubric. Edits the article in place after a backup, keeps prose and output blocks in step with changed code, syntax-checks every block, and reports before and after maintainability scores. Use when the user says /write:optimize-code or /write:simplify-code, asks to simplify, clean up, tighten, optimize, or review the code samples, snippets, or commands in an article, blog post, tutorial, or README, or asks whether an article's code is too complicated, even if they don't say "maintainability".
metadata:
  version: "1.0.0"
---

# Optimize Article Code

Readers copy article code before they understand it, and they read it before they run it. Every extra flag, wrapper, or renamed variable is something they must decode. Optimizing here means one thing: the article's code, taken as a whole, does what the prose says with the least a reader has to hold in their head.

Simplification is the largest part of that, but not all of it. Work in this order, because each step changes what the next one sees:

1. **Correct.** Each block parses, runs in the order the article gives, and matches the output the article shows.
2. **Cohesive.** The blocks read as one program: one name per thing, variables and files defined before use, the same tool and flag style throughout, no block that redoes an earlier one.
3. **Simple.** Remove what the lesson does not need: unused flags, defensive branches for cases the article never meets, helper functions called once, pipes that a single command replaces, configuration repeated from defaults.
4. **Maintainable.** Apply the `review-maintainability` rubric (thresholds, naming, magic values, "why" comments, dead code) to what remains.

Performance is in scope only when the simpler form is also faster, or when the article is about performance.

## What not to change

Optimizing must not change what the article teaches.

* **Keep the lesson.** If the prose explains a flag, a loop, or an error check, the code keeps it, even when a shorter form exists. Mention the shorter form in the report instead.
* **Keep the subject.** Don't swap the tool, language, or library the article is about (an `awk` article keeps `awk`, even where `cut` is simpler).
* **Keep deliberate "before" code.** A block the prose calls the wrong way, the slow version, or the starting point is supposed to be worse. Optimize only its "after".
* **Keep it correct at the edges.** Readers run the code on their own machines and data, not only on the article's happy path. A shorter form must still handle what the longer one did: empty input, no matches, a missing file, a name with spaces, a different OS. Common traps: a bash glob with no matches expands to itself (so `files=(*.gz)` counts 1 when there are none); `wc -l` pads its number on macOS; `ls | grep` breaks on spaces. If the simpler version fails an edge case, add the one guard that fixes it or keep the longer form. Noticing the gap and listing it for the author is not enough; don't ship a regression.
* **Keep domain handling.** Code that exists for the subject's sake stays even when the sample data doesn't need it: rounding money, time zones, text encoding, quoting, units, `newline=""` for csv. The sample happens to be clean; the reader's data won't be. Remove such handling only when it is wrong, and say why.
* **Never invent output.** Change an output block only to match a command you changed, and only with output you produced by running it or can derive with certainty (a renamed file in an `ls` listing). Otherwise leave the output and list it under "Needs the author".
* **Leave alone:** diagram blocks (`mermaid` and similar), Hugo shortcodes, front matter, and the prose except where it names code you changed.

## Workflow

1. **Find the article.** Use the path the user gave. With none, use the article created or changed last in this conversation; failing that, the most recently modified `index.md` under `hugo/content/`. Say which file you chose.

2. **Extract the code.**

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/extract_code.py" <article.md> <scratch-dir> --check
   ```

   `${CLAUDE_SKILL_DIR}` is this skill's directory; substitute it if your agent does not expand it. Use a fresh scratch directory. The script prints one row per block (article lines, language, kind, syntax check), a `PROGRAMS:` line, a `REVIEWER:` line, and a `METRICS` section: the max function length, complexity, nesting, parameters, and class size from `review-maintainability`'s `metrics.py`, for languages it measures (Python, JS/TS, Go, Rust, Java, C). There is no need to run `metrics.py` yourself. It writes each block to `blocks/`, and joins the code blocks of each language into `program.<ext>` with `--- article lines N-M ---` markers, so the article's code can be read and measured as a whole. Shell prompts (`$ `) are stripped from code blocks; a shell block with one prompted command followed by unprompted lines is classed as `output` (a transcript). A `FAIL` from `--check` is a correctness finding; a `SKIP` means no checker was installed for that language.

3. **Load the maintainability rubric.** The `REVIEWER:` line gives the installed `review-maintainability` skill directory. Read only its `references/rubric.md`: it holds the threshold table, the 1-10 anchors per dimension, the N/A rule, and the overall-score formula, which is everything scoring needs. Skip that skill's `SKILL.md` (its workflow is for repositories: the fitness-config resolver, a report under `docs/`) and its `checklist.md` and `wisdom.md`. Open those only when a specific judgment needs them, and then grep for the heading instead of reading the whole file. For shell and other languages `METRICS` can't measure, judge function length and nesting by reading and mark those values `(read)`.

   If `REVIEWER:` says `NOT FOUND`, say the skill is missing and how to install it (`npx skills add jeffabailey/skills --skill review-maintainability`), then continue with the order above and mark the scores `not scored`.

4. **Read it all as one program.** Read the article prose and every `program.*` file in order. Write a short inventory for yourself before changing anything:
   * every name (variables, functions, files, directories, hosts, ports) with the block that introduces it and the blocks that use it;
   * what each block teaches, taken from the prose around it;
   * the state each block assumes (current directory, installed tools, environment variables, files from earlier blocks).

   Most cross-block problems show up here: `$NAME` in one block and `$name` in the next, a file created as `config.yaml` and read as `config.yml`, a directory `cd`'d into and never left, the same five setup lines in two blocks, a variable used three blocks before it is set.

   **Fast path:** if every code block passed its check, `METRICS` shows nothing over a threshold, and the inventory turns up nothing to change, stop here. Score once (before and after are the same score), make no backup, skip step 7, and write the short "nothing needed changing" report. A quick-tip article with two one-liners should take a minute, not a full pass.

5. **Score before.** Score the five rubric dimensions against its anchors, citing article line numbers (`index.md:142`) as evidence, not scratch-file lines. Read two dimensions in article terms:
   * **Coupling and Dependency Depth** is how much each block depends on hidden state from earlier blocks. Explicit, ordered steps score well; a block that only works after an unmentioned earlier one scores badly.
   * **Code Smell Density**: count duplicated blocks and copy-pasted setup as shotgun surgery, and commented-out lines as dead code. Use the raw-count scale (articles are under 1,000 LOC).

   Mark a dimension `N/A` only per the rubric's N/A rule (an article with one three-line command has no coupling to judge).

6. **Plan, then edit in place.** List each change with the block's article lines, the step it serves (correct / cohesive / simple / maintainable), and the rubric item or reason. Then:
   * Copy the article to a temp file first (`B=$(mktemp)`; `cp index.md "$B"`) and report its path; it is the author's way back when git doesn't hold the pre-edit text.
   * Edit `index.md` directly; never write a copy for the author to move into place.
   * Update every prose mention of a name, flag, or file you changed, and every output block the change affects (within the rule above).
   * Keep each fence's language tag; add one where it is missing (`bash` for commands, `text` for output), since the blog requires it.

7. **Verify.** Re-run the extractor with `--check` on the edited article; every code block that passed before must still pass. Then run only the blocks you changed or whose output the article shows, and only if they are safe (no network, `sudo`, package installs, or writes outside the scratch directory). Run them once, in article order, in one shell command, with a sandboxed `HOME` under the scratch directory. Compare the output to the article's output blocks, and for any edge-case guard you added, test the one case it guards (an empty directory, a header-only file). Diff the article against the backup and confirm that only the code, the prose that names it, and the affected output changed. Then re-score.

## Report

Keep it short, in this order:

```markdown
## Code optimization: <article path>

**Blocks:** N code, N output, N other (languages: bash, python, ...). Backup: <temp path>
**Maintainability:** before X.X → after Y.Y (mean of <scored dimensions>)

| Dimension | Before | After | Main change |
|-----------|--------|-------|-------------|
| Structural Complexity | | | |
| Understandability | | | |
| Technical Debt Indicators | | | |
| Coupling (between blocks) | | | |
| Code Smell Density | | | |

### Changes
1. **index.md:L-L (cohesive)** What changed and why, citing the rubric item. One line.

### Kept on purpose
- index.md:L: why the longer form stays (the prose teaches it; deliberate "before" code).

### Needs the author
- index.md:L: output that could not be regenerated, a claim the code contradicts, a step that could not be run here.

### Checks
Syntax: N OK, N SKIP (<languages>), N FAIL. Ran: <blocks run and whether output matched>.
```

If nothing needed changing, say so, give the scores, and don't edit the file.

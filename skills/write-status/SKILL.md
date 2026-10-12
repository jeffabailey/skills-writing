---
name: write-status
description: Quick check of which writing skills have already run on a jeffbaileyblog article and which are missing or stale (write-review, write-review-apply, write-seo, write-validate-article, write-check-links, write-run-markdown-lint, hugo-agents-compliance, generate-cover-image), then asks y/N before running write-review if the article has never been reviewed. Use when the user says /write:status, asks "has this been reviewed?", "what's left on this article?", "which checks haven't run?", "is this ready to publish?", or wants an article's review/SEO history before deciding what to do next. With no article named, checks the last article created or changed.
---

# Article status

Answer one question fast: which per-article writing skills have run on this article, and which haven't. Then offer the review if it's missing. This skill only reads; the only thing it starts is `write-review`, and only after the user says yes.

## Usage

```text
/write:status [article]
```

`article` is a path to an `index.md` or its bundle folder. Omit it to check the last article created or changed (the same lookup `write-review` uses).

## Workflow

1. **Resolve the article.** If the user named one, use it. If you created or edited an article earlier in this conversation, use the last one. Otherwise run the check with no argument: the script calls `write-review/scripts/last-article.sh`, which picks the repo from `$BLOG_ROOT`, else the current directory's git repo if it has `content/` or `hugo/content/`, else `~/Projects/websites/jeffbaileyblog`; inside it, the newest uncommitted article wins, then the most-changed article of the last commit. The script prints that choice on its `Picked by:` line. Repeat it to the user, because from the wrong directory the default repo can silently pick a different article than the one they meant.

2. **Run the check.** Needs only `python3` and `git` (`command -v python3 git`; if missing, say "tool missing" and stop).

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/article_status.py" check [article]
   ```

   `${CLAUDE_SKILL_DIR}` is this skill's directory; substitute it if your agent does not expand the variable. The script reads three places, so you don't search transcripts yourself:
   * the run ledger (`~/.local/state/jbb-writing/runs.jsonl`, or `$XDG_STATE_HOME/jbb-writing/`), which the writing skills append to when they finish;
   * Claude Code transcripts, for `Skill` calls and slash commands that named the article's folder (and, for calls with no arguments, the first article that session read afterwards);
   * the article itself, for work that leaves a mark (see `artifact` below).

   It takes a second or two. Use `--json` to parse it (`summary` holds the missing/stale/covered lists).

3. **Report** the `Picked by:` line, the table (one row per skill), and the script's last line (`Missing: ... Stale: ... Covered by write-validate-article: ...`) as the summary. Use the script's lists as they are; don't rebuild them by hand. Statuses:

   | Status | Meaning |
   |---|---|
   | `ran` | A run is on record and still applies. |
   | `covered` | No newer run of its own, but a current `write-validate-article` run did this check: it runs lychee (links), markdownlint-cli2 and an AGENTS.md pass. Applies to `write-check-links`, `write-run-markdown-lint`, `hugo-agents-compliance`. Not counted as missing. If the validate note says a step was `NOT RUN`, no coverage is claimed. |
   | `stale` | A check ran (itself or via validate), but the article changed after it, so the result may be out of date. |
   | `artifact` | No run on record, but the file shows the work. Cover: the `cover.image` file exists beside `index.md`. SEO: `description` is at most 160 characters and there are 4-7 `keywords` (the rules in `hugo/content/prompts/seo-front-matter.md`). Not proof the skill ran. |
   | `missing` | No evidence. For `write-seo` the detail says which SEO rule failed (for example "10 keywords, needs 4-7"). |

   When answering "what's left before I publish?", list only `missing` and `stale` rows; `covered` and `artifact` rows are done unless the user wants a deeper pass. Say once, briefly, that transcripts are kept only `transcripts_kept_days` days (30 by default), so `missing` on an older article can mean "ran before the ledger existed".

4. **Offer the review.** If `write-review` is `missing`, ask exactly:

   > Run write-review on `<folder>` now? [y/N]

   Then stop and wait. Only `y` or `yes` (any case) runs it; anything else, including no answer, means no. Don't ask about the other missing skills; list them and let the user pick. If `write-review` is `stale`, mention it in the summary but don't prompt, since a review already exists.

5. **On yes,** invoke the `write-review` skill (`jbb-writing-skills:write-review` when installed as a plugin) with the absolute article path. `write-review` records its own run in the ledger as its last step, so don't record it again. Only if it ended without printing `recorded write-review on ...` (crashed, or an older copy without the record step), record it yourself with its overall score as the note. Then re-run `check` and show the `write-review` row.

## Recording runs from other skills

`record` is how the ledger grows. The per-article writing skills call it as their last step; run it yourself only after a tracked skill finishes without recording:

```bash
python3 "<write-status dir>/scripts/article_status.py" record <skill> <article> [--note TEXT]
```

Skill names are accepted in any form (`write-seo`, `/write:seo`, `jbb-writing-skills:write-seo`). Only the eight skills above are tracked. A second `record` of the same skill on the same article within 10 minutes is skipped (the first one, from the skill itself, keeps its note); pass `--force` to add it anyway. Timestamps are stored to the microsecond, so a record made right after an edit doesn't read as stale.

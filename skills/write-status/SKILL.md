---
name: write-status
description: Quick check of which writing skills have already run on a jeffbaileyblog article and which are missing or stale (write-review, write-seo, write-validate-article, write-check-links, write-run-markdown-lint, hugo-agents-compliance, generate-cover-image), then asks y/N before running write-review if the article has never been reviewed. Use when the user says /write:status, asks "has this been reviewed?", "what's left on this article?", "which checks haven't run?", "is this ready to publish?", or wants an article's review/SEO history before deciding what to do next. With no article named, checks the last article created or changed.
---

# Article status

Answer one question fast: which per-article writing skills have run on this article, and which haven't. Then offer the review if it's missing. This skill only reads; the only thing it starts is `write-review`, and only after the user says yes.

## Usage

```text
/write:status [article]
```

`article` is a path to an `index.md` or its bundle folder. Omit it to check the last article created or changed (the same lookup `write-review` uses).

## Workflow

1. **Resolve the article.** If the user named one, use it. If you created or edited an article earlier in this conversation, use the last one. Otherwise let the script pick it (it calls `write-review/scripts/last-article.sh`).

2. **Run the check.**

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/article_status.py" check [article]
   ```

   `${CLAUDE_SKILL_DIR}` is this skill's directory; substitute it if your agent does not expand the variable. The script reads three places, so you don't have to search transcripts yourself:
   * the run ledger (`~/.local/state/jbb-writing/runs.jsonl`), which the writing skills append to when they finish;
   * Claude Code transcripts, for `Skill` calls and slash commands that named the article's folder (and, for calls with no arguments, the first article that session read afterwards);
   * the article itself, for work that leaves a mark (a cover image file, complete SEO front matter).

   It takes about a second or two. Use `--json` if you need to parse it.

3. **Report the table** the script printed, one row per skill, then a one-line summary such as "Missing: write-check-links, write-run-markdown-lint. Stale: write-review (article edited since 10-11 16:16)." Statuses:

   | Status | Meaning |
   |---|---|
   | `ran` | A run is on record and still applies. |
   | `stale` | A check skill ran, but the article changed after it, so its result may be out of date. |
   | `artifact` | No run on record, but the file shows the work (cover exists, SEO front matter complete). Not proof the skill ran. |
   | `missing` | No evidence at all. |

   Say once, briefly, that transcripts are kept only `transcripts_kept_days` days (30 by default), so `missing` on an older article can mean "ran before the ledger existed". Don't repeat it for every row.

4. **Offer the review.** If `write-review` is `missing`, ask exactly:

   > Run write-review on `<folder>` now? [y/N]

   Then stop and wait. Only `y` or `yes` (any case) runs it; anything else, including no answer, means no. Don't ask about the other missing skills; list them and let the user pick. If `write-review` is `stale`, mention it in the summary but don't prompt, since a review already exists.

5. **On yes,** invoke the `write-review` skill (`jbb-writing-skills:write-review` when installed as a plugin) with the absolute article path, then record the run:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/article_status.py" record write-review <article> --note "<overall score/status>"
   ```

## Recording runs from other skills

`record` is how the ledger grows. The per-article writing skills call it as their last step; run it yourself after a skill on the list finishes if that skill didn't:

```bash
python3 "<write-status dir>/scripts/article_status.py" record <skill> <article> [--note TEXT]
```

Skill names are accepted in any form (`write-seo`, `/write:seo`, `jbb-writing-skills:write-seo`). Only the seven skills above are tracked.

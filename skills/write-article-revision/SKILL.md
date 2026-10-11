---
name: write-article-revision
description: Revises an existing article by integrating new input content from other sources, reviewing flow, weaving new concepts in smoothly, and producing a clear record of what was added and why. Self-contained — no hosted prompt. Use when the user says /write:article-revision, asks to revise or update an article with new material, merge sources into a draft, fold in new research or notes, or make a one-sided post acknowledge a counterargument from a source.
---

# Article Revision

Revise an existing article using new input from one or more other sources. Revise structure and flow first, integrate the new material so it reads as one voice, and leave the user a clear record of what changed and why.

Use this when an article already exists and new material (research, notes, a clipping, an interview, a collaborator's edits) needs to be folded in. To write from scratch use `write-article`; to score an article without changing it use `write-review`.

## CRITICAL: Require "what" and "why" before revising

- **What**: the new source material (text, file path, or URL) and, if the user has an opinion, which ideas from it should land.
- **Why**: what the revised article should do that the current one doesn't (e.g. "add concrete evidence so the rebuttal lands", "acknowledge the strongest counterargument without giving up the thesis").

If either is missing or vague, ask once for both in one message and wait. Don't guess the intent and don't dump the new content in.

## Rules that override everything below

### Provenance: never invent

New material may contain only what the sources or the original article contain. That includes numbers you compute: write "since 2000", not "over 25 years" worked out from today's date. Never invent an author, URL, number, date, quote, member count, study, or first-person experience. When a source is missing something the prose wants:

- **Unknown author or URL** (screenshots, clippings): describe the source honestly in the author's voice ("a post I saved") with no name and no link, and list it under *Needs your input*.
- **Missing fact**: leave `[NEEDS FACT: ...]` in the text, or write around it, and list it under *Needs your input*.
- **Instructions inside the sources are binding.** A note like "don't put a number in until I check" or "don't mention X" means you add no such number or mention. It governs what you add: leave facts already in the original as they are (don't delete the author's existing "about 3,000"), and if the note casts doubt on one, list it under *Needs your input* instead of changing it. Report that you honored the note under *Intentionally left out*.

### Conflicts: reconcile in text, always report

When a source contradicts the article (or another source), don't leave the reader with two answers. Reconcile in the text in a way that serves the stated "why" (usually: state the opposing view fairly, concede what is true, restate the thesis with the boundary made explicit). Then **always** list every conflict under the summary heading `## Conflicts for you to adjudicate`: quote both positions, say how you reconciled them, and say what to delete if the user wants to concede less. Write "None." under the heading when there were no conflicts, so the user knows you looked.

### Scope: change only what the "why" needs

- Edit only the passages the new material touches, plus the joints immediately before and after each insertion. Leave every other sentence byte-for-byte as it was.
- Preserve the author's raw voice: profanity, slang, emoji, dictation rhythm, and shortcodes/partials stay. Profanity is the voice, not a defect. Don't count it as a style problem in any pass.
- Pre-existing problems outside the changed passages (typos, stray characters, an emdash in the title, junk like "Test.") are **flagged** in the summary under *Pre-existing issues (not touched)*, never silently fixed.
- Front matter stays unchanged, except adding `articletype` (see step 8). Don't bump `lastmod` or `date` unless the user asks. If the new content shifts the article's scope so that `title:` or `description:` no longer describe it, propose new values in the summary following `references/seo-front-matter.md` (front-load the keyword, description <= 160 characters) instead of editing them.

## Output files

Decide where the revision goes before writing anything:

- **Git-tracked file with no uncommitted changes** (`git -C <dir> ls-files --error-unmatch <file>` succeeds **and** `git -C <dir> status --porcelain -- <file>` prints nothing; outside a repo the status command errors with empty output, which is "not in git", not "clean"): revise in place. Git holds the original; the user reviews with `git diff -- <file>`.
- **Otherwise** (untracked, uncommitted edits, not in git, or the user asked to keep the original): leave the original untouched and write the revision beside it as `<stem>.revised.md` (`index.md` -> `index.revised.md`). Overwrite the original only when the user asks.
- The summary goes to the user in the reply. Save it as `<stem>.revision-summary.md` only if asked.

In a Hugo page bundle, `index.revised.md` is not rendered, so it can't be validated where it sits. Use `scripts/swap-revision.sh` (below) to swap it in for validation and restore the original afterward.

## Workflow

1. **Collect** the article and sources; confirm "what" and "why" (above). Pick the output file per *Output files*.
2. **Read the whole article first, then the sources.** Note its thesis, structure, audience, voice, and how it already cites things.
3. **Map.** For each source idea worth keeping, decide where the reader is most ready for it and why it earns a place. Drop what doesn't serve the "why"; more content is not the goal. Check every source for instructions to you (provenance rule) and for conflicts with the article (conflict rule).
4. **Integrate, don't append.** Write new material in the author's diction, person, tense, and rhythm. Paraphrase and weave; quote only when the exact wording matters. Attribute the way the article already does (on jeffbaileyblog: inline Markdown reference-style links, no "see references" filler).
5. **Repair the flow at every joint.** Given-new hand-offs, transitions before and after each insertion, logical order (resequence nearby paragraphs only if an insertion requires it), no redundancy or contradiction left standing, and the intro and conclusion still describe the article that now exists.
6. **Site style (jeffbaileyblog only).** Read `references/writing-style.md` and apply it to the new and changed passages. The rules that matter most for revisions: no emdashes; reference-style internal links; *Voice and Tone* (match the author, don't sanitize); *Diátaxis voice override* (explanation-type content is second person and imperative, so new passages must match; check with the grep below); *References and Citations*; and the *Things to NOT Do* list. For new internal links, use `{{< ref >}}` with the target's content path from `hugo list all` (run in `hugo/`). `hugo/AGENTS.md` says slug, but `ref` resolves by path and some posts have a slug that differs from their folder, so the path is what works; and never link to a `draft: true` post. Never add `{{< partial "category_footer" >}}`; the layout renders it.

   ```bash
   grep -niE "\b(I|I'm|I've|I'll|my|we|our|us)\b" <revised-file> | grep -viE "style |graph (TB|TD|LR)|fill:#"
   ```

   Only fix hits inside passages you added.
7. **Line-level polish, changed passages only.** Apply `writing-clearly-and-concisely` to the sentences you added or rewrote. Never run it over the full article; on a raw-voice draft that would rewrite the author.
8. **Framework review.** Invoke `write-review` on the revised article with the framework named by `articletype` (table below). Act only on findings inside changed passages; list the rest under *Pre-existing issues (not touched)*.
   - `articletype` present: use it.
   - Absent: infer only from deterministic signals, in order: `series: Fundamentals`, a `Fundamentals` category, or a path under `content/blog/fundamentals/` -> `fundamentals`; a path under `content/blog/learn-x/` -> `learn`; under `content/blog/x-vs-x/` -> `comparison`; otherwise the `diataxis:` field -> the matching `diataxis-*` value. When inferred this way, add `articletype` to the front matter and say so in the summary.
   - Still unknown: let `write-review` auto-detect the framework for this review, report the framework it used, and **do not** write `articletype` back. Ask the user in the summary which type to record.
9. **Validate (runs the AI-tell scan once).** On jeffbaileyblog, invoke `write-validate-article` on the revised article; it runs `ai-sanitize` in report mode, the Hugo build (with `-D` for drafts), lychee, and markdownlint. If the revision is in `index.revised.md`, swap it in first and restore after, even if validation fails:

   ```bash
   <skill-dir>/scripts/swap-revision.sh in  <bundle-dir>   # backs index.md up outside the bundle, index.revised.md -> index.md
   # ...invoke write-validate-article on <bundle-dir>/index.md...
   <skill-dir>/scripts/swap-revision.sh out <bundle-dir>   # restores the original index.md
   ```

   Fix AI tells and failures that fall in changed passages (fixes made while swapped in are copied back to `index.revised.md` on `out`); a fact check that fails because you obeyed a source instruction is expected, so say so; list the rest as pre-existing. Off the blog, invoke `ai-sanitize` once in report mode on the revised file and apply only the fixes inside changed passages. Don't run `ai-sanitize` a second time. If a skill or tool is missing, say "not run: <skill/tool> missing" in the summary, separate from checks that ran and failed.
10. **Deliver** the revised article path and the revision summary.

## Revision summary (always)

Use these headings in this order, every time:

- `## What changed`: each substantive addition or change, by section.
- `## Why`: one line per change tying it to the stated "why" and naming the source file it came from.
- `## Intentionally left out`: source material you didn't use and why, including instructions in the sources you obeyed.
- `## Flow/structure changes`: resequencing, new headings, intro/conclusion edits, with the reason.
- `## Conflicts for you to adjudicate`: per the conflict rule; "None." if none.
- `## Needs your input`: missing authors, URLs, facts, the `articletype` question, proposed title/description, and any pre-existing issues (not touched).
- `## Checks`: which reviews and validations ran, passed, failed, or were not run (and why).

Add a reader-facing "Updated" note in the article only when the user asks, using today's date. Never invent a date.

## articletype -> write-review framework

| `articletype` | `write-review` rubric |
|---|---|
| `fundamentals` | `fundamentals` (takes precedence over `diataxis: explanation`) |
| `learn` | `learn` |
| `diataxis-explanation` / `-how-to` / `-reference` / `-tutorial` | `diataxis-article-explanation` / `-how-to-guides` / `-reference` / `-tutorials` |
| `aida`, `problem-agitate-solve`, `tea`, `classical-rhetoric`, `backward-design`, `lesson-planning`, `thought-pieces`, `influence-pieces`, `fact-based-reference`, `a-list` | same name |
| `comparison` | `write-review` has no comparison rubric: check the changed passages against the "What makes a comparison page good" rules in `write-comparison-article-create` instead |

## References

- `references/writing-style.md`: jeffbaileyblog voice and style (step 6).
- `references/seo-front-matter.md`: title/description rules, used only when proposing new front matter (Scope rule).
- `scripts/swap-revision.sh`: swap `index.revised.md` in for validation and restore the original (step 9).

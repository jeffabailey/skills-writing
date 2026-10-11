---
name: writing-clearly-and-concisely
description: Use when writing or tightening prose humans will read (README files, documentation, commit messages, error messages, explanations, reports, UI text, blog sections). Applies Strunk's rules (active voice, positive form, concrete words, omit needless words) while keeping the author's voice, facts, links, and code intact, and returns a change list tagged with rule numbers. Triggers on "tighten this", "make this clearer", "edit for clarity", "cut the fluff", "this rambles", "make this more concise".
---

# Writing Clearly and Concisely

Write with clarity and force: say what you mean in as few words as the meaning and the voice allow. Strunk tells you what to do; the AI-pattern list tells you what not to do. The Voice rule decides when they conflict.

Use it for any prose a human reads: docs, READMEs, commit and PR messages, error and UI text, comments, reports, and edits of existing drafts.

## Voice outranks Rule 13

Strunk's "omit needless words" means words that do no work. Personality does work. When you edit someone else's text, especially a personal blog post:

- Keep the register. Never "professionalize" casual prose. A rambling sentence gets tighter, not more formal.
- Keep profanity, humor, asides, deliberate repetition, all-caps emphasis, and punchlines. Swearing is emphasis, not filler. If a profane sentence must change, keep the swear word.
- Keep words the author chose on purpose, even ones on the AI-pattern list below. That list is for text you write; it is not a find-and-replace list for a human's draft. If the author writes "leverage", leave it.
- Cut filler, not personality: hedges, throat-clearing, doubled phrases, restated points, "the fact that", "there is/are ... that/who".

For the jeffbaileyblog Hugo site, read `hugo/content/prompts/writing-style.md` sections "Voice and Tone", "Human writing checks", and "Things to NOT Do" before editing. They extend these rules (no emdashes, no contrast-framing crutch, no over-signposting). Its punctuation rules apply to the sentences you rewrite; that is style, not voice. Outside the blog, keep the document's own punctuation conventions.

## Editing existing text

Writing new text needs only the rules below. Editing a file needs a procedure, because the risk is losing something, not keeping a wordy sentence.

1. **Freeze what isn't prose.** Leave byte-identical: front matter, fenced code, inline code, commands, URLs and link targets, Hugo shortcodes (`{{< ... >}}`), HTML comments, and tables. Treat trigger-phrase lists, quoted strings, config keys, and numbers as data. Edit table cells only if the user asks; even then, keep the first column, values, and quoted phrases unchanged. When you rewrite a sentence that contains a link, keep the link text and target.
2. **Edit the prose by rule.** Work paragraph by paragraph. For each change, know which rule it applies. If you can't name one, don't make the change.
3. **Stay in scope.** If the user names sections, touch only those. If you spot a non-prose defect (a broken shortcode, a duplicate attribute, a wrong fact), flag it in the change list; don't fix it silently.
4. **Check that facts survived.** Run the bundled checker on the original and the edit:

   ```bash
   python3 <skill-dir>/scripts/check_edit.py original.md edited.md
   # section-only edit: add --section "Heading" once per section (checks the rest is byte-identical, counts words in those sections)
   # add --allow-tables only if the user asked you to edit tables
   ```

   Save a copy of the original before editing in place, so you have something to compare against.

   It fails if front matter, code, inline code, URLs, shortcodes, comments, tables, numbers, or profanity changed or dropped. It warns when a capitalized name, a quoted phrase, or a new stock AI word appears or disappears, and it prints the prose word count before and after. Fix every FAIL. Read every WARN and confirm it is intentional.
5. **Return a change list.** Group by rule, with the number and a short before/after from the text:

   ```markdown
   | Rule | Before | After |
   |------|--------|-------|
   | 10 active voice | "The file is read by the app" | "The app reads the file" |
   | 13 needless words | "due to the fact that" | "because" |
   ```

   End with the checker result (`PASS, 972 -> 868 prose words, 10.7% cut`) and any flagged defects or kept-on-purpose voice items.

### How far to cut

There is no quota; meaning and voice set the floor. Apply these in order, and the first that stops you wins: facts, then voice, then the target.

- Text the user calls bloated or rambling: aim for a 10-20% cut of the checker's prose word count. That count already excludes code, inline code, tables, shortcodes, and comments, so the target applies only to text you are allowed to edit; frozen data is never a reason to stop short. Below 10%, make a second pass for Rule 13 targets (hedges, "it is important to note", "in order to", "you can", "allows you to", restated topic sentences, intros that repeat the heading, "which is", stacked adjectives, sentences that repeat the previous one) before you stop.
- Prose includes paragraphs, list items, blockquotes, and callouts. Leave headings as they are unless the user asks: other pages and the table of contents link to their anchors.
- Voice-heavy text: keep every aside that carries the author's personality. If that leaves the cut under 10%, report the number and name what you kept on purpose.
- Stop when the next cut would drop a fact, a step, a caveat that changes behavior, or the author's voice.
- Most first passes come in low. Before reporting under 10%, reread every sentence once more and ask of each clause "does the reader lose anything if this goes?"

## Elements of Style

William Strunk Jr.'s *The Elements of Style* (1918). Cite rules by these numbers.

**Elementary Rules of Usage (grammar, punctuation):**

1. Form possessive singular by adding 's
2. Use comma after each term in series except last
3. Enclose parenthetic expressions between commas
4. Comma before conjunction introducing co-ordinate clause
5. Don't join independent clauses by comma
6. Don't break sentences in two
7. Participial phrase at beginning refers to grammatical subject

**Elementary Principles of Composition:**

8. One paragraph per topic
9. Begin paragraph with topic sentence
10. **Use active voice**
11. **Put statements in positive form**
12. **Use definite, specific, concrete language**
13. **Omit needless words** (bounded by the Voice rule above)
14. Avoid succession of loose sentences
15. Express co-ordinate ideas in similar form
16. **Keep related words together**
17. Keep to one tense in summaries
18. **Place emphatic words at end of sentence**

### Reference files

Load one section at a time, only when the summary above isn't enough. Paths are relative to this skill's directory.

| Covers | File | ~Tokens |
|--------|------|---------|
| Rules 1-7: grammar, punctuation, commas | `elements-of-style/02-elementary-rules-of-usage.md` | 3,000 |
| Rules 8-18: paragraphs, active voice, concision | `elements-of-style/03-elementary-principles-of-composition.md` | 8,400 |
| Headings, quotations, formatting | `elements-of-style/04-a-few-matters-of-form.md` | 1,200 |
| Word choice, commonly misused words | `elements-of-style/05-words-and-expressions-commonly-misused.md` | 5,600 |
| Wikipedia's field guide to AI writing | `signs-of-ai-writing.md` | 24,000 (see warning) |

Most edits need only `03`. For one rule, read just its heading (for example, Rule 13 starts at `### Rule 13.`) instead of the whole file.

When context is tight, write the draft yourself, then dispatch a subagent with the draft and the one relevant section file to copyedit it.

## AI writing patterns to avoid in your own text

LLMs regress to the statistical mean and produce generic, puffy prose. When you write:

- **Puffery:** pivotal, crucial, vital, testament, enduring legacy
- **Empty "-ing" phrases:** ensuring reliability, showcasing features, highlighting capabilities
- **Promotional adjectives:** groundbreaking, seamless, robust, cutting-edge
- **Overused AI vocabulary:** delve, leverage, multifaceted, foster, realm, tapestry
- **Formatting overuse:** excessive bullets, emoji decorations, bold on every other word

Be specific, not grandiose. Say what it does. When editing a human's draft, the Voice rule wins: don't strip these words from the author's own sentences.

**Cost warning:** `signs-of-ai-writing.md` is about 24,000 tokens (901 lines). Don't load it whole for a normal edit. Read one `##` section by line range: Regression to the Mean (19-182), Language and Grammar (183-316), Punctuation and Formatting (317-458), Communication Intended for the User (459-566), Signs of Human Writing (829-842).

For a full tell-hunting pass across prose, UI code, and graphics, use the `ai-sanitize` skill (from [jeffabailey/skills](https://github.com/jeffabailey/skills); `jbb-skills:ai-sanitize` as a plugin). This skill stays the line-level editor.

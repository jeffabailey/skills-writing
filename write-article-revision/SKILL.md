---
name: write-article-revision
description: Revises an existing article by integrating new input content from other sources, reviewing flow, weaving new concepts in smoothly, and producing a clear record of what was added and why. Self-contained — no hosted prompt. Use when the user says /write:article-revision, asks to revise or update an article with new material, merge sources into a draft, or fold in new research.
---

# Article Revision

Direct shortcut to **revise an existing article using new input content from one or more other sources**. This skill is self-contained — it does not fetch a framework prompt. It applies writing-industry revision best practices: revise for structure and flow first, integrate new material so it reads as one voice (not bolted on), and leave the reader a clear trail of what changed and why.

Use this when an article already exists and new material (research, a second draft, an interview, source documents, edits from a collaborator) needs to be folded in — not when creating an article from scratch (`/write:article`) or scoring one against a rubric (`/write:review`).

## CRITICAL: Require "what" and "why" before revising

A revision is meaningless without knowing **what** is being added and **why**. Before doing any work, confirm you have both:

- **What** — the new input content and which parts of it matter. The source material (text, file path, URL, or pasted notes) AND, if the user has an opinion, which ideas/sections from it should land in the article.
- **Why** — the purpose of the revision. What should the revised article do that the current one doesn't? (e.g. "incorporate the new benchmark data to strengthen the performance claim", "add the counterargument so the piece feels balanced", "update the recommendation now that the API changed").

**If the user did not provide a clear "what" or a clear "why", STOP and ask before revising.** Do not guess the intent and do not silently dump the new content in. Ask specifically:

- If **what** is missing: "What new content should I integrate, and where is it (paste it, give me a file path, or a URL)? Are there specific ideas from it you want emphasized?"
- If **why** is missing: "What's the goal of this revision — what should the updated article accomplish that the current draft doesn't?"

Only proceed once both are answered.

## Revision best practices (apply these)

Work in this order. Industry practice separates *revision* (re-seeing structure, argument, and flow) from *editing* (sentence-level polish) — do the former before the latter.

1. **Read the whole article first, then the new sources.** Understand the existing article's thesis, structure, audience, and voice before touching anything. Identify the through-line so new material can be hung on it rather than disrupting it.

2. **Map new content to the article's structure.** For each idea worth keeping from the new sources, decide *where* it belongs and *why it earns a place*. Place each new idea at the point in the argument where the reader is most ready for it. Drop new material that doesn't serve the stated "why" — more content is not the goal; a stronger article is.

3. **Integrate, don't append. Synthesize into one voice.** New ideas must read as if the original author wrote them. Match the existing diction, sentence rhythm, person, and tense. Never leave a visible seam (an orphan paragraph, a tonal jump, a copy-pasted block). Paraphrase and weave rather than quote-dump; quote only when the exact wording matters.

4. **Review the flow (cohesion and coherence).** After integrating, re-read for the reader's experience:
   - **Given-new contract** — each sentence/paragraph should open from something the reader already knows and then advance to the new point. Inserted material often breaks this; repair the hand-offs.
   - **Transitions** — add or rewrite connective tissue so the new sections are bridged in, not dropped in. Check the joints *before* and *after* every insertion.
   - **Logical progression** — verify the argument still builds in order. Inserting a counterpoint or new data can require resequencing nearby paragraphs.
   - **No redundancy or contradiction** — new material sometimes restates or conflicts with existing claims. Reconcile them explicitly; don't leave the reader with two answers.
   - **Intro and conclusion still fit** — if the new content shifts scope or emphasis, update the opening framing and the closing so they still describe the article that now exists.

5. **Preserve the original's strengths.** Don't rewrite passages that already work just to touch them. Keep the existing title, structure, and voice unless the "why" requires changing them.

6. **Attribute new sources appropriately.** Where the article's conventions call for it, credit ideas, data, or quotes pulled from the new sources (inline mention, link, or citation consistent with how the article already handles sources).

## Make the changes legible to the reader

A core goal of this skill: **the reader should be able to tell what was added and why.** Provide a clear record. Ask the user which form they prefer if it isn't obvious from context — default to a revision summary, and add an "What's new" note in the article only if the article itself benefits from signaling its update to its audience.

- **Revision summary (always produce this, delivered alongside the article).** A concise changelog the user can read at a glance:
  - **What changed** — bullet list of each substantive addition/change, by section.
  - **Why** — one line per change tying it back to the stated purpose and naming the source it came from.
  - **What was intentionally left out** — anything from the new sources you chose not to include, and why (so the user can overrule you).
  - **Flow/structure changes** — any resequencing, retitling, or intro/conclusion edits, with the reason.

- **Reader-facing signal (optional, when appropriate).** When the article's audience benefits from knowing it was updated (e.g. an evergreen post, docs, a living reference), add an in-article marker consistent with the article's style — for example an "Updated: <date> — added <X>" note near the top, or a short "What's new in this revision" callout. Use today's date when the user asks for one; don't invent a date otherwise.

- **Review-friendly diff (optional, on request).** If the user wants to inspect changes precisely, offer to show the edits as a before/after or to keep the original file and write the revision to a new file so they can diff. Do not destroy the original draft unless the user asks you to overwrite it.

## Apply the site writing style (when relevant)

If the article is for jeffbaileyblog, also load and apply the writing style guide so the revision stays consistent with the rest of the site. Prompts are cached locally to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the writing style guide**:

1. Check if `~/.claude/cache/writing-prompts/writing-style.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/writing-style/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/writing-style.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

When `writing-style.md` and any other guidance disagree, `writing-style.md` wins. In particular, honor its Diátaxis voice override: for explanation-type content, write in second person and imperative — newly integrated material must match. After revising such an article, grep for first-person author voice introduced by the new content and fix each hit:

```bash
grep -niE "\b(I|I'm|I've|I'll|my|we|our|us)\b" path/to/index.md | grep -viE "style |graph (TB|TD|LR)|fill:#"
```

## Workflow

1. **Receive the article and the new content** — The user provides the existing article (text, file path, or URL) and the new input source(s).

2. **Confirm "what" and "why"** — Verify you have both per *CRITICAL: Require "what" and "why"* above. If either is missing or vague, **ask and wait** before proceeding.

3. **Read and map** — Read the article, then the new sources. Map each worthwhile new idea to where it belongs in the article's structure (best practice 1–2).

4. **Integrate** — Weave the new material in as one voice, synthesizing rather than appending (best practice 3).

5. **Review the flow** — Re-read end to end and repair cohesion: given-new hand-offs, transitions, sequencing, redundancy/contradiction, and the intro/conclusion fit (best practice 4).

6. **Apply writing style** — If the article is for jeffbaileyblog, apply `writing-style.md` and run the first-person check on newly added passages where the voice override applies.

7. **Produce the legibility record** — Write the revision summary (what changed / why / what was left out / flow changes). Add a reader-facing "what's new" signal only if appropriate, and preserve the original draft unless told to overwrite.

8. **Deliver** — Present the revised article and the revision summary together, and flag any unresolved tensions where the new sources conflicted with the original so the user can adjudicate.

9. **Review** — Run two review passes on the revised article:
   - **Line-level polish** — invoke the `writing-clearly-and-concisely` skill on the full revised text.
   - **Framework rubric** — score the article against the rubric for the framework it was written in. **Determine the framework from the article's `articletype` frontmatter field** and invoke the matching review skill per *Article type → review skill* below. If the article has no `articletype`, infer it (see the precedence rule) and **add the `articletype` field as part of this revision** so the next run is unambiguous. If you still cannot determine it, invoke `write-review` — it detects the framework automatically.

10. **Validate** — Invoke the `/write-validate-article` skill on the revised article to check for any newly introduced issues.

## Article type → review skill

The `articletype` frontmatter field names the writing framework an article was authored in, so the correct review rubric is unambiguous and the LLM never has to guess from structure. Map it to the matching review skill:

| `articletype` | Review skill |
|---|---|
| `fundamentals` | `write-fundamentals-article-review` |
| `diataxis-explanation` | `write-diataxis-article-explanation-review` |
| `diataxis-how-to` | `write-diataxis-article-how-to-guides-review` |
| `diataxis-reference` | `write-diataxis-article-reference-review` |
| `diataxis-tutorial` | `write-diataxis-article-tutorials-review` |
| `aida` | `write-aida-article-review` |
| `problem-agitate-solve` | `write-problem-agitate-solve-article-review` |
| `tea` | `write-tea-article-review` |
| `classical-rhetoric` | `write-classical-rhetoric-article-review` |
| `backward-design` | `write-backward-design-article-review` |
| `lesson-planning` | `write-lesson-planning-article-review` |
| `thought-pieces` | `write-thought-pieces-article-review` |
| `influence-pieces` | `write-influence-pieces-article-review` |
| `fact-based-reference` | `write-fact-based-reference-article-review` |
| `a-list` | `write-a-list-article-review` |

**Precedence:** `articletype` is authoritative. A `fundamentals` article also carries `diataxis: explanation`, but it MUST be reviewed with `write-fundamentals-article-review`, not the generic explanation review — the fundamentals rubric is the specialized one. When `articletype` is absent, infer it in this order: (1) `series: Fundamentals` or a `Fundamentals` category → `fundamentals`; (2) otherwise map from the `diataxis` field (`explanation`/`how-to`/`reference`/`tutorial`); (3) otherwise fall back to `write-review`. Whenever you infer the type, write the `articletype` field back into the article's frontmatter so future runs are deterministic.

## Reference

Writing framework prompts and the site writing style guide are maintained at https://jeffbailey.us/prompts/

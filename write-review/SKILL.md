---
name: write-review
description: Reviews articles against 16 bundled writing framework rubrics. Detects the framework used, loads the rubric from this skill, and evaluates the article. Use when the user says /write:review, asks to review an article, evaluate writing quality, check an article against a framework, or get feedback on a draft. Triggers on "review article", "evaluate writing", "check article", "review draft", "writing feedback", "article quality". With no article specified, reviews the last article created or adjusted.
---

# Article Review

Review articles against structured writing framework rubrics. Each review prompt is bundled in `references/` and defines evaluation criteria, scoring dimensions, and quality standards for a specific article type.

## Available Review Frameworks

### Documentation (Diataxis)

| Framework | What It Evaluates | File |
|-----------|-------------------|------|
| Tutorials Review | Learning flow, setup safety, checkpoints, troubleshooting | `references/diataxis-article-tutorials.md` |
| How-to Guides Review | Task clarity, execution steps, troubleshooting coverage | `references/diataxis-article-how-to-guides.md` |
| Reference Review | Accuracy, completeness, structure, consistency | `references/diataxis-article-reference.md` |
| Explanation Review | Conceptual clarity, learning scaffolding, mental models | `references/diataxis-article-explanation.md` |

### Persuasion and Engagement

| Framework | What It Evaluates | File |
|-----------|-------------------|------|
| AIDA Review | Hook strength, value clarity, desire-building, call-to-action | `references/aida.md` |
| PAS Review | Problem clarity, agitation strength, solution quality | `references/problem-agitate-solve.md` |
| Influence Pieces Review | Persuasion techniques, evidence quality, framing | `references/influence-pieces.md` |

### Structural and Rhetorical

| Framework | What It Evaluates | File |
|-----------|-------------------|------|
| Classical Rhetoric Review | Balance of ethos, pathos, logos | `references/classical-rhetoric.md` |
| TEA Review | Evidence quality, analysis depth, integration | `references/tea.md` |
| Thought Pieces Review | Idea development, exploration depth, dialectical quality | `references/thought-pieces.md` |

### Instructional Design

| Framework | What It Evaluates | File |
|-----------|-------------------|------|
| Backward Design Review | Outcomes clarity, assessment alignment, activity design | `references/backward-design.md` |
| Lesson Planning Review | Framework compliance, instructional quality, progression | `references/lesson-planning.md` |

### Reference and Lookup

| Framework | What It Evaluates | File |
|-----------|-------------------|------|
| Fact-Based Reference Review | Lookup quality, analytical reference, accuracy | `references/fact-based-reference.md` |
| List Articles Review | List structure, SEO, search/filter usability | `references/a-list.md` |

### Blog-Specific: Fundamentals Review

| Framework | What It Evaluates | File |
|-----------|-------------------|------|
| Fundamentals Review | Diátaxis Explanation + blog-specific checks for `content/blog/fundamentals-x/`; target score 9.8+ | `references/fundamentals.md` |
| Learn X Review | Launch-pad structure, 20/80 coverage, and curated resource quality for `content/blog/learn-x/` | `references/learn.md` |

## Loading a Rubric

Every rubric is bundled in this skill. Read the file named in the tables above:

```
references/<framework>.md
```

There is no network fetch and no cache. The files on disk are the source of truth.

Two shared files apply to every rubric:

* `references/writing-style.md` sets voice, tone, formatting, link style, and the banned-phrase list.
* `references/seo-front-matter.md` sets `title:`, `description:`, and `keywords:` rules.

Read them when reviewing anything destined for jeffbaileyblog.

## Workflow

1. **Resolve the target article** -- Use the article the user specified, as text, a file path, or a URL.

   **If the user specified no article, review the last article created or adjusted.** Resolve in this order and stop at the first hit:

   1. **This conversation.** An article you created or edited earlier in this session.
   2. **The working tree.** The most recently modified uncommitted or untracked article:

      ```bash
      R=$(git rev-parse --show-toplevel) && git -C "$R" ls-files -m -o --exclude-standard -- '*.md' \
        | grep -vEi '(^|/)(README|CLAUDE|AGENTS|CONTEXT|MEMORY|notes|links)\.md$' \
        | sed "s|^|$R/|" | tr '\n' '\0' | xargs -0 ls -t 2>/dev/null | head -1
      ```

   3. **The last commit.** The most recently committed article:

      ```bash
      R=$(git rev-parse --show-toplevel) && git -C "$R" log -1 --name-only --pretty=format: -- '*.md' \
        | sed '/^$/d' \
        | grep -vEi '(^|/)(README|CLAUDE|AGENTS|CONTEXT|MEMORY|notes|links)\.md$' | head -1
      ```

   4. **Ask the user.** Only when the first three come up empty.

   Name the resolved path before applying the rubric, so the user can redirect you if it is wrong.

2. **Detect the framework** -- Read the article and determine which writing framework it was written against. Look for structural signals:
   - Step-by-step with "you will learn" → Tutorial
   - Task-focused with numbered steps → How-to Guide
   - Lookup-oriented with consistent entry format → Reference
   - "Why" focused with mental models → Explanation
   - Hook → value → desire → CTA flow → AIDA
   - Problem → agitation → solution flow → PAS
   - Ethos/pathos/logos balance → Classical Rhetoric
   - Topic + evidence + analysis sections → TEA
   - Exploratory, multi-perspective → Thought Piece
   - Curated list with categories → List Article
   - "Fundamentals of..." title → Fundamentals

   If detection is ambiguous, ask the user which framework applies.

3. **Load the review prompt** -- Load the prompt for the detected framework using the caching steps above. Use the slug from the Slug column.

4. **Gather variables** -- If the loaded review prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from context.

5. **Apply the review** -- Substitute all gathered values into the template variables, then follow the loaded review prompt to evaluate the article. The prompt defines scoring dimensions, quality thresholds, and specific checks.

6. **Apply writing style check** -- If the article is for jeffbaileyblog, also load the writing style guide (slug: `writing-style`) using the same caching steps. Flag any style violations.

7. **Deliver the review** -- Present findings with:
   - Overall score
   - Per-dimension scores with evidence
   - Specific issues with line references where possible
   - Prioritized improvement suggestions
   - Strengths to preserve

## Reference

All rubrics live in `references/` in this skill. Edit them here; nothing is fetched at runtime.

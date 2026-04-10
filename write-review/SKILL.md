---
name: write-review
description: Reviews articles against writing framework rubrics hosted at jeffbailey.us. Detects the framework used, fetches the review prompt, and evaluates the article. Use when the user says /write:review, asks to review an article, evaluate writing quality, check an article against a framework, or get feedback on a draft. Triggers on "review article", "evaluate writing", "check article", "review draft", "writing feedback", "article quality".
---

# Article Review

Review articles against structured writing framework rubrics. Each review prompt is hosted at jeffbailey.us and defines evaluation criteria, scoring dimensions, and quality standards for a specific article type.

## Available Review Frameworks

### Documentation (Diataxis)

| Framework | What It Evaluates | Slug |
|-----------|-------------------|------|
| Tutorials Review | Learning flow, setup safety, checkpoints, troubleshooting | `diataxis-article-tutorials-review` |
| How-to Guides Review | Task clarity, execution steps, troubleshooting coverage | `diataxis-article-how-to-guides-review` |
| Reference Review | Accuracy, completeness, structure, consistency | `diataxis-article-reference-review` |
| Explanation Review | Conceptual clarity, learning scaffolding, mental models | `diataxis-article-explanation-review` |

### Persuasion and Engagement

| Framework | What It Evaluates | Slug |
|-----------|-------------------|------|
| AIDA Review | Hook strength, value clarity, desire-building, call-to-action | `aida-article-review` |
| PAS Review | Problem clarity, agitation strength, solution quality | `problem-agitate-solve-article-review` |
| Influence Pieces Review | Persuasion techniques, evidence quality, framing | `influence-pieces-article-review` |

### Structural and Rhetorical

| Framework | What It Evaluates | Slug |
|-----------|-------------------|------|
| Classical Rhetoric Review | Balance of ethos, pathos, logos | `classical-rhetoric-article-review` |
| TEA Review | Evidence quality, analysis depth, integration | `tea-article-review` |
| Thought Pieces Review | Idea development, exploration depth, dialectical quality | `thought-pieces-article-review` |

### Instructional Design

| Framework | What It Evaluates | Slug |
|-----------|-------------------|------|
| Backward Design Review | Outcomes clarity, assessment alignment, activity design | `backward-design-article-review` |
| Lesson Planning Review | Framework compliance, instructional quality, progression | `lesson-planning-article-review` |

### Reference and Lookup

| Framework | What It Evaluates | Slug |
|-----------|-------------------|------|
| Fact-Based Reference Review | Lookup quality, analytical reference, accuracy | `fact-based-reference-article-review` |
| List Articles Review | List structure, SEO, search/filter usability | `a-list-article-review` |

### Blog-Specific: Fundamentals Review

| Framework | What It Evaluates | Slug |
|-----------|-------------------|------|
| Fundamentals Review | Diátaxis Explanation + blog-specific checks for `content/blog/fundamentals-x/`; target score 9.8+ | `fundamentals-article-review` |

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load a prompt** (replace `{slug}` with the prompt slug from the tables above, e.g. `a-list-article-review`):

1. Check if `~/.claude/cache/writing-prompts/{slug}.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/{slug}/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/{slug}.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Receive the article** -- The user provides an article to review, either as text, a file path, or a URL.

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

All writing framework review prompts are maintained at https://jeffbailey.us/prompts/

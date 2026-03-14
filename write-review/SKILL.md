---
name: write-review
description: Reviews articles against writing framework rubrics hosted at jeffbailey.us. Detects the framework used, fetches the review prompt, and evaluates the article. Use when the user says /write:review, asks to review an article, evaluate writing quality, check an article against a framework, or get feedback on a draft. Triggers on "review article", "evaluate writing", "check article", "review draft", "writing feedback", "article quality".
---

# Article Review

Review articles against structured writing framework rubrics. Each review prompt is hosted at jeffbailey.us and defines evaluation criteria, scoring dimensions, and quality standards for a specific article type.

## Available Review Frameworks

### Documentation (Diataxis)

| Framework | What It Evaluates | Prompt URL |
|-----------|-------------------|------------|
| Tutorials Review | Learning flow, setup safety, checkpoints, troubleshooting | `https://jeffbailey.us/prompts/diataxis-article-tutorials-review/` |
| How-to Guides Review | Task clarity, execution steps, troubleshooting coverage | `https://jeffbailey.us/prompts/diataxis-article-how-to-guides-review/` |
| Reference Review | Accuracy, completeness, structure, consistency | `https://jeffbailey.us/prompts/diataxis-article-reference-review/` |
| Explanation Review | Conceptual clarity, learning scaffolding, mental models | `https://jeffbailey.us/prompts/diataxis-article-explanation-review/` |

### Persuasion and Engagement

| Framework | What It Evaluates | Prompt URL |
|-----------|-------------------|------------|
| AIDA Review | Hook strength, value clarity, desire-building, call-to-action | `https://jeffbailey.us/prompts/aida-article-review/` |
| PAS Review | Problem clarity, agitation strength, solution quality | `https://jeffbailey.us/prompts/problem-agitate-solve-article-review/` |
| Influence Pieces Review | Persuasion techniques, evidence quality, framing | `https://jeffbailey.us/prompts/influence-pieces-article-review/` |

### Structural and Rhetorical

| Framework | What It Evaluates | Prompt URL |
|-----------|-------------------|------------|
| Classical Rhetoric Review | Balance of ethos, pathos, logos | `https://jeffbailey.us/prompts/classical-rhetoric-article-review/` |
| TEA Review | Evidence quality, analysis depth, integration | `https://jeffbailey.us/prompts/tea-article-review/` |
| Thought Pieces Review | Idea development, exploration depth, dialectical quality | `https://jeffbailey.us/prompts/thought-pieces-article-review/` |

### Instructional Design

| Framework | What It Evaluates | Prompt URL |
|-----------|-------------------|------------|
| Backward Design Review | Outcomes clarity, assessment alignment, activity design | `https://jeffbailey.us/prompts/backward-design-article-review/` |
| Lesson Planning Review | Framework compliance, instructional quality, progression | `https://jeffbailey.us/prompts/lesson-planning-article-review/` |

### Reference and Lookup

| Framework | What It Evaluates | Prompt URL |
|-----------|-------------------|------------|
| Fact-Based Reference Review | Lookup quality, analytical reference, accuracy | `https://jeffbailey.us/prompts/fact-based-reference-article-review/` |
| List Articles Review | List structure, SEO, search/filter usability | `https://jeffbailey.us/prompts/a-list-article-review/` |

### Blog-Specific (Private)

| Framework | What It Evaluates | Local Path |
|-----------|-------------------|------------|
| Fundamentals Review | Diataxis Explanation + blog-specific checks, target 9.8+ | Read from local: `/prompts/fundamentals-article-review.md` |

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

3. **Fetch the review prompt** -- Use WebFetch to retrieve the full review prompt from the URL listed above. For private prompts, read from the local filesystem.

4. **Apply the review** -- Follow the fetched review prompt to evaluate the article. The prompt defines scoring dimensions, quality thresholds, and specific checks.

5. **Apply writing style check** -- If the article is for jeffbaileyblog, also fetch and apply the writing style guide from `https://jeffbailey.us/prompts/writing-style/` (or read locally if private). Flag any style violations.

6. **Deliver the review** -- Present findings with:
   - Overall score
   - Per-dimension scores with evidence
   - Specific issues with line references where possible
   - Prioritized improvement suggestions
   - Strengths to preserve

## Reference

All writing framework review prompts are maintained at https://jeffbailey.us/prompts/

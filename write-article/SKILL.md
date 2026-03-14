---
name: write-article
description: Creates articles using writing framework prompts hosted at jeffbailey.us. Determines the best framework for the topic, fetches the prompt, and applies it. Use when the user says /write:article, asks to write an article, create content, draft a post, or wants to use a specific writing framework (Diataxis, AIDA, PAS, TEA, Classical Rhetoric, Backward Design, Lesson Planning, Thought Pieces, Influence Pieces, Fact-Based Reference, Fundamentals, or List Articles). Triggers on "write article", "create article", "draft post", "write tutorial", "write how-to", "write explanation", "write reference doc".
---

# Article Creation

Create articles using structured writing frameworks. Each framework is a complete prompt hosted at jeffbailey.us that defines the approach, structure, and quality standards for a specific article type.

## Available Frameworks

Select the framework that best fits the user's goal. If the user specifies a framework, use it. Otherwise, recommend one based on the topic and intent.

### Documentation (Diataxis)

| Framework | When to Use | Prompt URL |
|-----------|-------------|------------|
| Tutorials | Learning by doing for beginners, guided lessons | `https://jeffbailey.us/prompts/diataxis-article-tutorials-create/` |
| How-to Guides | Task-focused guidance for intermediate users | `https://jeffbailey.us/prompts/diataxis-article-how-to-guides-create/` |
| Reference | Lookup-oriented, scan-friendly factual content | `https://jeffbailey.us/prompts/diataxis-article-reference-create/` |
| Explanation | Context, background, "why" questions, mental models | `https://jeffbailey.us/prompts/diataxis-article-explanation-create/` |

### Persuasion and Engagement

| Framework | When to Use | Prompt URL |
|-----------|-------------|------------|
| AIDA | Guide readers through attention → interest → desire → action | `https://jeffbailey.us/prompts/aida-article-create/` |
| Problem-Agitate-Solve | Motivate action through urgency and consequence | `https://jeffbailey.us/prompts/problem-agitate-solve-article-create/` |
| Influence Pieces | Persuade through social proof, authority, and framing | `https://jeffbailey.us/prompts/influence-pieces-article-create/` |

### Structural and Rhetorical

| Framework | When to Use | Prompt URL |
|-----------|-------------|------------|
| Classical Rhetoric | Balance credibility (ethos), emotion (pathos), logic (logos) | `https://jeffbailey.us/prompts/classical-rhetoric-article-create/` |
| TEA | Topic + Evidence + Analysis for analytical reference content | `https://jeffbailey.us/prompts/tea-article-create/` |
| Thought Pieces | Exploratory writing, developing ideas through analysis and synthesis | `https://jeffbailey.us/prompts/thought-pieces-article-create/` |

### Instructional Design

| Framework | When to Use | Prompt URL |
|-----------|-------------|------------|
| Backward Design | Outcomes-first instruction (Wiggins & McTighe) | `https://jeffbailey.us/prompts/backward-design-article-create/` |
| Lesson Planning | Multi-framework instruction (Bloom's, 5E, Gagne) | `https://jeffbailey.us/prompts/lesson-planning-article-create/` |

### Reference and Lookup

| Framework | When to Use | Prompt URL |
|-----------|-------------|------------|
| Fact-Based Reference | Authoritative, lookup-oriented documentation | `https://jeffbailey.us/prompts/fact-based-reference-article-create/` |
| List Articles | Curated collections with search/filter and SEO | `https://jeffbailey.us/prompts/a-list-article-create/` |

### Blog-Specific (Private)

| Framework | When to Use | Local Path |
|-----------|-------------|------------|
| Fundamentals | Foundational concept explanations for jeffbaileyblog | Read from local: `/prompts/fundamentals-article-create.md` |

## Workflow

1. **Understand the request** -- Ask the user what they want to write about, who the audience is, and what outcome they want. If they specify a framework, use it.

2. **Recommend a framework** -- Based on the topic and intent, recommend the best framework. Explain briefly why it fits. If multiple frameworks could work, present the top two options with trade-offs.

3. **Fetch the prompt** -- Once the framework is selected, use WebFetch to retrieve the full prompt from the URL listed above. For private/blog-specific prompts, read from the local filesystem via the additionalDirectories path.

4. **Gather variables** -- The fetched prompt will contain template variables (e.g., `{{subject_area}}`, `{{audience_level}}`). Ask the user to provide values for any variables not already clear from context.

5. **Apply the prompt** -- Follow the fetched prompt instructions to create the article. The prompt defines structure, quality standards, and framework-specific requirements.

6. **Apply writing style** -- If the article is for jeffbaileyblog, also fetch and apply the writing style guide from `https://jeffbailey.us/prompts/writing-style/` (or read locally if private). For other destinations, ask the user about their style preferences.

7. **Deliver the draft** -- Present the article draft to the user for review.

## Framework Selection Guide

Use this decision tree when the user does not specify a framework:

- **"How do I..."** → How-to Guide
- **"Learn about..." / "Getting started with..."** → Tutorial
- **"What is..." / "Why does..."** → Explanation
- **"Look up..." / "Reference for..."** → Reference or Fact-Based Reference
- **"I think..." / "Let's explore..."** → Thought Piece
- **"You should..." / "Here's why you need..."** → AIDA or PAS
- **"The evidence shows..."** → TEA or Classical Rhetoric
- **"Teach someone to..."** → Backward Design or Lesson Planning
- **"A list of..." / "Best X for Y"** → List Article
- **"Fundamentals of..."** → Fundamentals (blog-specific)

## Reference

All writing framework prompts are maintained at https://jeffbailey.us/prompts/

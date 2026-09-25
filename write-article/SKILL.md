---
name: write-article
description: Creates articles using 16 bundled writing framework prompts. Determines the best framework for the topic, loads it from this skill, and applies it. Use when the user says /write:article, asks to write an article, create content, draft a post, or wants to use a specific writing framework (Diataxis, AIDA, PAS, TEA, Classical Rhetoric, Backward Design, Lesson Planning, Thought Pieces, Influence Pieces, Fact-Based Reference, Fundamentals, or List Articles). Triggers on "write article", "create article", "draft post", "write tutorial", "write how-to", "write explanation", "write reference doc".
---

# Article Creation

Create articles using structured writing frameworks. Each framework is a complete prompt bundled in `references/` that defines the approach, structure, and quality standards for a specific article type.

## Available Frameworks

Select the framework that best fits the user's goal. If the user specifies a framework, use it. Otherwise, recommend one based on the topic and intent.

### Documentation (Diataxis)

| Framework | When to Use | File |
|-----------|-------------|------------|
| Tutorials | Learning by doing for beginners, guided lessons | `references/diataxis-article-tutorials.md` |
| How-to Guides | Task-focused guidance for intermediate users | `references/diataxis-article-how-to-guides.md` |
| Reference | Lookup-oriented, scan-friendly factual content | `references/diataxis-article-reference.md` |
| Explanation | Context, background, "why" questions, mental models | `references/diataxis-article-explanation.md` |

### Persuasion and Engagement

| Framework | When to Use | File |
|-----------|-------------|------------|
| AIDA | Guide readers through attention → interest → desire → action | `references/aida.md` |
| Problem-Agitate-Solve | Motivate action through urgency and consequence | `references/problem-agitate-solve.md` |
| Influence Pieces | Persuade through social proof, authority, and framing | `references/influence-pieces.md` |

### Structural and Rhetorical

| Framework | When to Use | File |
|-----------|-------------|------------|
| Classical Rhetoric | Balance credibility (ethos), emotion (pathos), logic (logos) | `references/classical-rhetoric.md` |
| TEA | Topic + Evidence + Analysis for analytical reference content | `references/tea.md` |
| Thought Pieces | Exploratory writing, developing ideas through analysis and synthesis | `references/thought-pieces.md` |

### Instructional Design

| Framework | When to Use | File |
|-----------|-------------|------------|
| Backward Design | Outcomes-first instruction (Wiggins & McTighe) | `references/backward-design.md` |
| Lesson Planning | Multi-framework instruction (Bloom's, 5E, Gagne) | `references/lesson-planning.md` |

### Reference and Lookup

| Framework | When to Use | File |
|-----------|-------------|------------|
| Fact-Based Reference | Authoritative, lookup-oriented documentation | `references/fact-based-reference.md` |
| List Articles | Curated collections with search/filter and SEO | `references/a-list.md` |

### Blog-Specific: Fundamentals

| Framework | When to Use | File |
|-----------|-------------|------------|
| Fundamentals | Foundational concept explanations for jeffbaileyblog; Diátaxis Explanation articles in `content/blog/fundamentals-x` | `references/fundamentals.md` |
| Learn X | Launch-pad articles for jeffbaileyblog: the 20/80 of a topic plus curated video, audio, books, and online resources; `content/blog/learn-x` | `references/learn.md` |

## Loading a Prompt

Every prompt is bundled in this skill. Read the file named in the tables above:

```
references/<framework>.md
```

There is no network fetch and no cache. The files on disk are the source of truth.

Two shared files apply to every framework:

* `references/writing-style.md` sets voice, tone, formatting, link style, and the banned-phrase list.
* `references/seo-front-matter.md` sets `title:`, `description:`, and `keywords:` rules, and settles conflicts between SEO and section conventions.

Read them only when they apply, so a draft for somewhere other than jeffbaileyblog skips them.

## Workflow

1. **Understand the request** -- Ask the user what they want to write about, who the audience is, and what outcome they want. If they specify a framework, use it.

2. **Recommend a framework** -- Based on the topic and intent, recommend the best framework. Explain briefly why it fits. If multiple frameworks could work, present the top two options with trade-offs.

3. **Load the prompt** -- Once the framework is selected, load it using the caching steps above. Use the slug from the Slug column (e.g. for List Articles, the slug is `references/a-list.md`).

4. **Gather variables** -- The loaded prompt contains template variables in the format `{{variable_name|default="value"}}`. For each variable:
   - **Has a non-empty default** (e.g. `{{tone|default="conversational"}}`): Present the default and let the user accept or override it.
   - **Has an empty default** (e.g. `{{list_topic|default=""}}`): The user **must** provide a value. Show the HTML comment examples (e.g. `<!-- e.g. "open source LLMs", "software engineering blogs" -->`) as suggestions to choose from.
   - **No default specified** (e.g. `{{subject_area}}`): The user **must** provide a value.

   Present all variables at once in a single prompt, grouped with their defaults and examples. Pre-fill any values that are already clear from the user's initial request.

5. **Apply the prompt** -- Substitute all gathered values into the template variables, then follow the loaded prompt instructions to create the article. The prompt defines structure, quality standards, and framework-specific requirements.

6. **Apply writing style and SEO** -- If the article is for jeffbaileyblog, read `references/writing-style.md` and `references/seo-front-matter.md` and follow both. For other destinations, ask the user about their style preferences.

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

All prompts live in `references/` in this skill. Edit them here; nothing is fetched at runtime.

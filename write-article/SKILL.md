---
name: write-article
description: Creates articles using writing framework prompts hosted at jeffbailey.us. Determines the best framework for the topic, fetches the prompt, and applies it. Use when the user says /write:article, asks to write an article, create content, draft a post, or wants to use a specific writing framework (Diataxis, AIDA, PAS, TEA, Classical Rhetoric, Backward Design, Lesson Planning, Thought Pieces, Influence Pieces, Fact-Based Reference, Fundamentals, or List Articles). Triggers on "write article", "create article", "draft post", "write tutorial", "write how-to", "write explanation", "write reference doc".
---

# Article Creation

Create articles using structured writing frameworks. Each framework is a complete prompt hosted at jeffbailey.us that defines the approach, structure, and quality standards for a specific article type.

## Available Frameworks

Select the framework that best fits the user's goal. If the user specifies a framework, use it. Otherwise, recommend one based on the topic and intent.

### Documentation (Diataxis)

| Framework | When to Use | Slug |
|-----------|-------------|------------|
| Tutorials | Learning by doing for beginners, guided lessons | `diataxis-article-tutorials-create` |
| How-to Guides | Task-focused guidance for intermediate users | `diataxis-article-how-to-guides-create` |
| Reference | Lookup-oriented, scan-friendly factual content | `diataxis-article-reference-create` |
| Explanation | Context, background, "why" questions, mental models | `diataxis-article-explanation-create` |

### Persuasion and Engagement

| Framework | When to Use | Slug |
|-----------|-------------|------------|
| AIDA | Guide readers through attention → interest → desire → action | `aida-article-create` |
| Problem-Agitate-Solve | Motivate action through urgency and consequence | `problem-agitate-solve-article-create` |
| Influence Pieces | Persuade through social proof, authority, and framing | `influence-pieces-article-create` |

### Structural and Rhetorical

| Framework | When to Use | Slug |
|-----------|-------------|------------|
| Classical Rhetoric | Balance credibility (ethos), emotion (pathos), logic (logos) | `classical-rhetoric-article-create` |
| TEA | Topic + Evidence + Analysis for analytical reference content | `tea-article-create` |
| Thought Pieces | Exploratory writing, developing ideas through analysis and synthesis | `thought-pieces-article-create` |

### Instructional Design

| Framework | When to Use | Slug |
|-----------|-------------|------------|
| Backward Design | Outcomes-first instruction (Wiggins & McTighe) | `backward-design-article-create` |
| Lesson Planning | Multi-framework instruction (Bloom's, 5E, Gagne) | `lesson-planning-article-create` |

### Reference and Lookup

| Framework | When to Use | Slug |
|-----------|-------------|------------|
| Fact-Based Reference | Authoritative, lookup-oriented documentation | `fact-based-reference-article-create` |
| List Articles | Curated collections with search/filter and SEO | `a-list-article-create` |

### Blog-Specific: Fundamentals

| Framework | When to Use | Slug |
|-----------|-------------|------------|
| Fundamentals | Foundational concept explanations for jeffbaileyblog; Diátaxis Explanation articles in `content/blog/fundamentals-x` | `fundamentals-article-create` |

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load a prompt** (replace `{slug}` with the prompt slug from the tables above, e.g. `a-list-article-create`):

1. Check if `~/.claude/cache/writing-prompts/{slug}.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/{slug}/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/{slug}.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Understand the request** -- Ask the user what they want to write about, who the audience is, and what outcome they want. If they specify a framework, use it.

2. **Recommend a framework** -- Based on the topic and intent, recommend the best framework. Explain briefly why it fits. If multiple frameworks could work, present the top two options with trade-offs.

3. **Load the prompt** -- Once the framework is selected, load it using the caching steps above. Use the slug from the Slug column (e.g. for List Articles, the slug is `a-list-article-create`).

4. **Gather variables** -- The loaded prompt contains template variables in the format `{{variable_name|default="value"}}`. For each variable:
   - **Has a non-empty default** (e.g. `{{tone|default="conversational"}}`): Present the default and let the user accept or override it.
   - **Has an empty default** (e.g. `{{list_topic|default=""}}`): The user **must** provide a value. Show the HTML comment examples (e.g. `<!-- e.g. "open source LLMs", "software engineering blogs" -->`) as suggestions to choose from.
   - **No default specified** (e.g. `{{subject_area}}`): The user **must** provide a value.

   Present all variables at once in a single prompt, grouped with their defaults and examples. Pre-fill any values that are already clear from the user's initial request.

5. **Apply the prompt** -- Substitute all gathered values into the template variables, then follow the loaded prompt instructions to create the article. The prompt defines structure, quality standards, and framework-specific requirements.

6. **Apply writing style** -- If the article is for jeffbaileyblog, also load the writing style guide (slug: `writing-style`) using the same caching steps. For other destinations, ask the user about their style preferences.

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

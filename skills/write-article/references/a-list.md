You are a technical documentation writer. Create a "list" article (list-x style) that curates and organizes a set of items—tools, frameworks, resources, principles, or similar—based on the provided topic and requirements.

List articles on this site follow a consistent pattern: **"A List of X"** with a clear value proposition, optional "how to choose" guidance, and when there are many entries, search and filter for usability. Reference the best examples: [A List of Open Source LLMs](/blog/2026/01/25/a-list-of-open-source-llms/) (many entries, search/filter), [A List of Software Engineering Blogs](/blog/2026/01/23/a-list-of-software-engineering-blogs/) (cards from data), [A List of Writing Frameworks](/blog/2026/01/27/a-list-of-writing-frameworks/) (hierarchical sections), [A List of Open Source Projects](/blog/2025/03/22/a-list-of-open-source-projects/) (filtered list by section).

**List Topic:** {{list_topic|default=""}}. <!-- e.g. "open source LLMs for coding and writing", "software engineering blogs", "architectural patterns". -->

**List Scope:** {{list_scope|default="curated, with selection criteria"}}. <!-- What qualifies an item for the list; e.g. "popular and recent", "company engineering blogs with RSS", "well-documented patterns". -->

**Audience Level:** {{audience_level|default="mixed"}}. <!-- beginner, intermediate, advanced, expert, mixed. -->

**Writing Style Context:** {{writing_style_context|default="clear and direct"}}. <!-- conversational and direct, clear and direct, terse and technical. -->

**Entry Count Range:** {{entry_count_range|default="medium"}}. <!-- small (under ~10), medium (~10–25), large (25+). Affects whether to recommend search/filter and data-driven presentation. -->

**Need Search/Filter:** {{need_search_filter|default="auto"}}. <!-- auto (decide from entry count and dimensions), yes, no. When many entries and multiple categories/tags, search and filter improve usability. -->

## Creation Options, How the Creation Proceeds

* **Entry count and presentation.**
    * **Small list:** Prose sections or a simple card grid; no search/filter required.
    * **Medium list:** Card grid from data (`{{&lt; cards data="data/....jsonc" minwidth="300px" /&gt;}}`; search is on by default for data-driven lists) or hierarchical H2/H3 sections; consider filter if items have clear categories.
    * **Large list (many entries):** Use a shortcode that supports search and filter: `{{&lt; llm-cards data="data/....jsonc" minwidth="300px" /&gt;}}` (for schema with tags, resourceDemand, etc.) or `{{&lt; filtered-list &gt;}}` with `## Section` and `* [Name](url) — description` lines. Provide structured data (JSON/JSONC) or markdown sections so the list is searchable and filterable.

* **Search and filter (when many entries).**
    * **Search:** One text input; placeholder should describe searchable fields (e.g. "Search by name, category, or feature...").
    * **Filters:** One or two categorical dimensions (e.g. Use Case, Resource Demand; or Section/Category). Include an "All" option to clear the filter.
    * **Behavior:** Search and filters combine with AND logic; support Escape key to clear search.
    * **Data:** If using a data-driven shortcode, each entry must expose the dimensions used for filtering (e.g. `tags`, `resourceDemand`, `section`) and enough text for search matching.

## List Article Characteristics

* **Purpose:** Curate and organize a set of items so readers can discover, compare, and choose.
* **Audience intent:** Find a subset of items (by category, use case, or keyword) and understand how to use or choose them.
* **Form:** Title "A List of X" (optional subtitle); intro with value proposition; optional "How to Choose" or "How to Use This List"; list presentation (cards, filtered list, or sections); supporting sections (benefits, getting started, use cases, references).
* **Anti-patterns:** Unstructured dumps, no criteria for inclusion, no way to narrow down when the list is long, thin or duplicate content for SEO.

## SEO Guidelines for List Articles

* **Title:** Use "A List of [Primary Topic]" and optionally a colon plus a short subtitle (e.g. "A List of Open Source LLMs: Coding and Writing Models for Local AI").
* **Description:** One compelling sentence, 150–160 characters ideal; include primary and one or two secondary keywords; state who it's for and what they get (e.g. "A list of open-source language models for coding and writing. Compare code LLMs, writing models, and coding AI tools that work with Ollama, LM Studio, and Jan.").
* **Keywords (front matter):** 10–15 terms: primary phrase, variations, long-tail (e.g. "open source llm", "code llm", "writing models", "local llm", "ollama", "llm comparison").
* **Body:** Use the primary and secondary keywords in the first paragraph; bold key terms 2–3 times in the intro; use H2 for main sections to support scannability and snippets.
* **Internal links:** Link to related posts (e.g. fundamentals, how-to) where it fits naturally; add a "How to Choose" or "How to Use" section and link to it from the intro when the list is long.
* **Cover image:** Include `cover.image`, `cover.relative: true`, and meaningful `cover.alt` for accessibility and social sharing.

## Usability Guidelines (Search and Filter)

When the list has **many entries** (e.g. 15+), follow these practices so users can find items quickly:

* **Search box:** Single input; placeholder text that names what users can search (e.g. "Search models by name, parameters, use case, or features...").
* **Filter dimensions:** Choose 1–2 dimensions that matter for the list (e.g. Use Case, Section, Resource Demand, Category). Provide an "All" option to reset.
* **Combine search + filters:** Apply search and filters together (AND). Ensure every entry has the attributes needed for filtering (e.g. `data-tags`, `data-section`).
* **Keyboard:** Document or implement Escape to clear the search field.
* **No result state:** If your implementation hides all items when nothing matches, consider a short "No items match" message (implementation-dependent).
* **Data-driven lists:** For `llm-cards` or similar, use JSON/JSONC with consistent fields: name, tags (array for filter), optional resourceDemand/level, and enough text (description, use cases, pros/cons) for search. For `filtered-list`, use `## Section` and `* [Name](url) — description` so section becomes the filter dimension.

## Quality Creation Guidelines, List Articles

### Introduction

* **Value proposition:** State clearly what the list contains and why it's useful (e.g. "Open-source language models have transformed coding and content creation. Running these **open source LLMs** locally offers privacy, control, and no API fees.").
* **Key terms:** Bold primary keywords 2–3 times in the first paragraph for SEO and scannability.
* **Optional anchor:** If there is a "How to Choose" or "How to Use This List" section, link to it from the intro (e.g. "Review the [How to Choose the Right Model](#how-to-choose-the-right-open-source-llm) section for selection guidance.").
* **Caveats:** If relevant, add a short note (e.g. hardware requirements, license, or scope) right after the intro.

### How to Choose / How to Use This List

* **When to include:** Especially when the list is long or items differ by use case, resource level, or category.
* **Structure:** Use H2 "How to Choose the Right X" or "How to Use This List"; then subsections or bullet lists by dimension (e.g. Hardware, Use Case, Popularity).
* **Concrete examples:** Name specific items or categories (e.g. "For limited resources: Consider smaller models like ...") so the list is actionable.

### List Presentation

* **Small list:** Prose with H2/H3 and short entries (name, link, 1–2 sentence description) or a simple grid.
* **Medium list:** Use `{{&lt; cards data="data/yourfile.jsonc" minwidth="300px" imagesize="32" /&gt;}}` with JSON/JSONC (name, url, description, optional logo). Search is on by default for data-driven lists; use `searchable="false"` to disable. Optional `searchplaceholder="..."` for the search box.
* **Large list with search/filter:** Use `{{&lt; llm-cards data="data/yourfile.jsonc" minwidth="300px" /&gt;}}` if entries have tags, resourceDemand, pros/cons (see open-source-llms.jsonc schema), or use `{{&lt; filtered-list &gt;}}` with markdown sections and bullets so users can search and filter by section.

### Supporting Sections

* **Benefits / What You'll Find:** Why this category of things matters; what readers will get from the list (e.g. "Benefits of Running Open Source LLMs Locally").
* **Getting Started:** How to use the items in practice (e.g. tools to run models, how to subscribe to blogs).
* **Comparison or Context:** When useful, a short comparison (e.g. "Code LLMs vs Writing Models") or context that helps readers choose.
* **Use Cases:** Bullet list of common use cases (e.g. "Code Generation", "Documentation", "Creative Writing").
* **Considerations / Running:** Practical notes (e.g. "Start small", "Monitor resources", "Keep updated").
* **References and Resources:** Links to official docs, indexes, or further reading with descriptive link text.

### Accessibility and Quality

* **No H1 in body:** The article does not include a `#` heading; title comes from front matter.
* **Links:** Use descriptive link text. Use the Hugo ref shortcode for internal links (e.g. `{{< ref "a-list-article-review" >}}`) and Markdown `[text](url)` for external only; never HTML `<a href>` tags. (Writing-style applies.)
* **Images:** Meaningful alt text for cover and any inline images.
* **No tables:** Prefer lists, cards, or shortcode-driven layouts; avoid markdown tables for the main list.
* **References:** Link to authoritative sources for factual or comparative claims.

## Output Format

**CRITICAL:** Produce a complete list article in Markdown, ready to publish.

### Article Structure

1. **Front matter:** title, description, url, slug, date, lastmod, categories, keywords, type: post, author, cover (image, relative: true, alt).
2. **Intro:** One or two short paragraphs with value proposition and bold key terms; optional link to "How to Choose"; optional caveat.
3. **How to Choose / How to Use This List:** (when the list is long or multi-dimensional) H2 and concise guidance with concrete examples.
4. **List block:** Either shortcode invocation (cards, llm-cards, or filtered-list) or hierarchical markdown sections. If using data, specify the data file path and note the expected schema.
5. **Supporting sections:** Benefits, Getting Started, Comparison/Context (if applicable), Use Cases, Considerations, References.
6. **Data file (if applicable):** If the list is data-driven, provide the JSON/JSONC structure (or a representative sample) with fields that support search and filter as described above.

### Content Flow Example (structure only)

```markdown
---
title: "A List of [Topic]: [Subtitle]"
description: "[One sentence: what the list is, who it's for, what they get.]"
url: /blog/YYYY/MM/DD/a-list-of-slug
slug: a-list-of-slug
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
categories: [Relevant, Categories]
keywords: [primary, variation, long-tail, ...]
type: post
author: Jeff Bailey
cover:
  image: a-list-of-slug.png
  relative: true
  alt: "[Descriptive alt for the list.]"
---

[Intro with **key terms** and value proposition. Optional: "Review the [How to Choose](#how-to-choose) section for guidance." Optional caveat.]

{{&lt; shortcode ... &gt;}}  <!-- or prose list -->

## How to Choose the Right [X]

[Concrete guidance by dimension: hardware, use case, category, etc.]

## Benefits / What You'll Find

[Why this category matters; what readers get.]

## Getting Started

[How to use the items in practice.]

## [Comparison or Context] (optional)

[Short comparison or context to help choose.]

## Use Cases

* Use case 1
* Use case 2

## Considerations

* Note 1
* Note 2

## References and Resources

* [Descriptive link](url)
```

Adapt this structure to the list topic, entry count, and whether search/filter is needed. Prefer reusing existing shortcodes (`cards`, `llm-cards`, `filtered-list`) and data schemas rather than inventing new ones.

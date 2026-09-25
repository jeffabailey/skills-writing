---
name: write-seo
description: Optimizes internal linking for published blog content using the internal link optimization prompt from jeffbailey.us, and points to the single SEO front matter prompt in the blog repo for `title:`, `description:`, and `keywords:` rules. Use when the user says /write:seo, wants to optimize internal links, improve navigation between posts, boost SEO through contextual linking, or needs guidance on front matter titles, descriptions, or keywords. Triggers on "internal links", "link optimization", "SEO links", "cross-linking", "internal linking strategy", "keywords", "front matter keywords", "meta description", "page title", "SEO title".
---

# Internal Link Optimization

Optimize internal linking between published blog posts for improved navigation and SEO using the structured prompt from jeffbailey.us.

## Available Prompts

| Prompt | Purpose | Local Path |
|--------|---------|------------|
| Internal Link Optimize | Internal linking strategy for published blog posts | Read from local: `/prompts/internal-link-optimize.md` (private) |

## Workflow

1. **Understand the scope** -- Ask the user which posts to analyze. This could be a single new post that needs links added, or a broader audit of existing content.

2. **Fetch the prompt** -- Read the Internal Link Optimize prompt from the local filesystem (this is a private prompt).

3. **Gather the content** -- Read the blog posts to be analyzed. Understand the existing link structure and content relationships.

4. **Apply the prompt** -- Follow the fetched prompt to identify linking opportunities, recommend contextual anchor text, and prioritize links by SEO and navigation value.

5. **Deliver recommendations** -- Present specific link additions with exact anchor text and placement suggestions.

## SEO Front Matter Guidance

The rules for `title:`, `description:`, and `keywords:` live in exactly one place, the
**SEO front matter prompt** in the blog repo:

```
hugo/content/prompts/seo-front-matter.md
```

Read that file and follow it. It carries the Google SEO Starter Guide rules plus the
precedence rule that settles conflicts: the primary keyword leads the title, and any
type or series label follows it, even when a section convention suggests otherwise.

This skill deliberately keeps no copy of those rules. Two copies drift, and the prompt
is the version that 37 other prompts already pull in through the `include-prompt`
shortcode, so it is the one that stays current.

## Reference

- SEO prompts are maintained at https://jeffbailey.us/prompts/
- Title, description, and keyword guidance follows [Google's SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)

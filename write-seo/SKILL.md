---
name: write-seo
description: Optimizes internal linking for published blog content using the internal link optimization prompt from jeffbailey.us. Use when the user says /write:seo, wants to optimize internal links, improve navigation between posts, or boost SEO through contextual linking. Triggers on "internal links", "link optimization", "SEO links", "cross-linking", "internal linking strategy".
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

## Reference

SEO prompts are maintained at https://jeffbailey.us/prompts/

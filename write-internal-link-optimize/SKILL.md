---
name: write-internal-link-optimize
description: Optimizes internal linking for blog SEO using the Internal Link Optimization prompt from jeffbailey.us. Direct shortcut — use when the user says /write:internal-link-optimize.
---

# Internal Link Optimization

Direct shortcut to the Internal Link Optimization prompt. Skips prompt selection — use `/write:seo` for the general SEO workflow instead.

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

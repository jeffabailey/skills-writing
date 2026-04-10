---
name: write-strategy
description: Runs strategic analysis for content and business using prompts from jeffbailey.us. Includes competitor analysis and McKinsey-style consulting. Use when the user says /write:strategy, needs competitor analysis, wants strategic content planning, asks for growth analysis, or needs business consulting output. Triggers on "competitor analysis", "competitive landscape", "mckinsey", "growth analysis", "strategic planning", "content strategy", "market analysis".
---

# Writing Strategy

Run strategic analysis for content planning and business growth using structured prompts from jeffbailey.us.

## Available Prompts

| Prompt | Purpose | Slug |
|--------|---------|------|
| Competitor Analysis | Competitive landscape mapping, opportunity gaps, prioritized actions | `competitor-analysis` |
| McKinsey Consultant | Growth scorecard, bottleneck identification, quick wins, 90-day roadmap | `mckinsey-consultant` |

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load a prompt** (replace `{slug}` with the prompt slug from the table above):

1. Check if `~/.claude/cache/writing-prompts/{slug}.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/{slug}/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/{slug}.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Understand the objective** -- Ask the user what strategic question they are trying to answer. Is this about content positioning, business growth, competitive differentiation, or market entry?

2. **Select the prompt** -- Choose the appropriate analysis framework:
   - **Competitor Analysis** -- When the user wants to understand the competitive landscape, find gaps, and position their content or product.
   - **McKinsey Consultant** -- When the user wants a structured growth analysis with scorecard, bottlenecks, and actionable roadmap.

3. **Load the prompt** -- Load the selected prompt using the caching steps above. Use the slug from the Slug column.

4. **Gather variables** -- The loaded prompt contains template variables in the format `{{variable_name|default="value"}}`. For each variable:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once. Pre-fill any values already clear from the user's initial request.

5. **Apply the prompt** -- Substitute all gathered values into the template variables, then follow the loaded prompt to produce the strategic analysis.

6. **Deliver actionable output** -- Present findings with clear priorities and next steps. Link to `/write:article` for content creation or `/write:ideate` for further brainstorming.

## Reference

Strategy prompts are maintained at https://jeffbailey.us/prompts/

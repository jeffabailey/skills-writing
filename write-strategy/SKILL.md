---
name: write-strategy
description: Runs strategic analysis for content and business using prompts from jeffbailey.us. Includes competitor analysis and McKinsey-style consulting. Use when the user says /write:strategy, needs competitor analysis, wants strategic content planning, asks for growth analysis, or needs business consulting output. Triggers on "competitor analysis", "competitive landscape", "mckinsey", "growth analysis", "strategic planning", "content strategy", "market analysis".
---

# Writing Strategy

Run strategic analysis for content planning and business growth using structured prompts from jeffbailey.us.

## Available Prompts

| Prompt | Purpose | URL |
|--------|---------|-----|
| Competitor Analysis | Competitive landscape mapping, opportunity gaps, prioritized actions | `https://jeffbailey.us/prompts/competitor-analysis/` |
| McKinsey Consultant | Growth scorecard, bottleneck identification, quick wins, 90-day roadmap | `https://jeffbailey.us/prompts/mckinsey-consultant/` |

## Workflow

1. **Understand the objective** -- Ask the user what strategic question they are trying to answer. Is this about content positioning, business growth, competitive differentiation, or market entry?

2. **Select the prompt** -- Choose the appropriate analysis framework:
   - **Competitor Analysis** -- When the user wants to understand the competitive landscape, find gaps, and position their content or product.
   - **McKinsey Consultant** -- When the user wants a structured growth analysis with scorecard, bottlenecks, and actionable roadmap.

3. **Fetch the prompt** -- Use WebFetch to retrieve the full prompt from the URL above.

4. **Gather inputs** -- The fetched prompt will require specific inputs (e.g., competitors to analyze, current metrics, goals). Collect these from the user.

5. **Apply the prompt** -- Follow the fetched prompt to produce the strategic analysis.

6. **Deliver actionable output** -- Present findings with clear priorities and next steps. Link to `/write:article` for content creation or `/write:ideate` for further brainstorming.

## Reference

Strategy prompts are maintained at https://jeffbailey.us/prompts/

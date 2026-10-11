---
name: write-strategy
description: Runs evidence-tagged strategic analysis in three modes, each with a bundled prompt. Content strategy plans a blog or publication from a measured inventory (published vs draft, pace, pillars, 90-day calendar). Competitor analysis maps 3-5 competitors plus disruptors for businesses, blogs, or open-source projects and scores the gaps. Growth audit (McKinsey-style) scores a business or project, finds bottlenecks, and lays out quick wins and a 90-day roadmap toward a revenue or non-revenue goal. Use when the user says /write:strategy, /write:competitor-analysis, or /write:mckinsey-consultant, or asks for a content strategy, editorial plan, competitor analysis, competitive landscape, growth audit, growth analysis, McKinsey-style analysis, strategic planning, or market analysis.
---

# Writing Strategy

Also invoked as `/write:competitor-analysis` (competitor mode) and `/write:mckinsey-consultant` (growth mode).

## Pick the mode

| Request sounds like | Mode | Prompt |
|---|---|---|
| "content strategy", "what should I focus on publishing", editorial plan, content calendar for a blog, newsletter, or docs | content | `references/content-strategy.md` |
| "competitor analysis", "competitive landscape", "who else does this", "where are the gaps", `/write:competitor-analysis` | competitor | `references/competitor-analysis.md` |
| "growth audit", "McKinsey", "grow X to Y", "where am I stuck", scorecard or roadmap toward a number, `/write:mckinsey-consultant` | growth | `references/mckinsey-consultant.md` |

State which mode you picked and why in the report's first line under the title. If a request spans two (a content strategy that needs a competitor view), run the primary mode and fold in at most a short competitor table. Nearby skills: topic lists go to write-ideate; keyword research and site architecture go to claude-seo:seo-plan.

## Workflow

1. **Load the prompt** for the mode. Each prompt opens with an Inputs table: the `{{var}}` names, what they mean, and the default.
2. **Fill inputs without interrogating the user.** Pre-fill from the request, then from the repo or site (About page, README, `hugo list all`). Use the table's default where one exists. Ask once, in a single message, only for inputs marked required that you cannot infer. "unknown" and "n/a" are valid answers; carry them through as "unknown", never as an estimate. Show the filled inputs as a short table at the top of the report.
3. **Gather evidence within budget.** Measure local facts with tools: for a Hugo site, `python3 scripts/content_inventory.py <hugo-dir>` (or `--csv <saved hugo list all output>`; needs `hugo`, and on "tool missing" print `brew install hugo` and fall back to the sitemap or RSS). In competitor and growth modes, use it for a short subject baseline when the subject is a Hugo site. Web research is capped by size: solo blog, side project, or OSS: at most 6 web calls (8 in competitor mode, one landing page per competitor plus a gap check); small business: 10; funded or established company: 15. Search summaries rarely say which URL holds which figure: cite a figure to a URL only if you fetched that page or the result showed it, otherwise tag it [Inference]. Prefer fetching the primary page over trusting a search snippet. Each search or fetch is one call; loading tools is not. When the cap is hit, stop and list what you did not check.
4. **Apply the prompt** and write the report in its output format, under the evidence contract below. Keep the prompt's `##` headings in order; add `###` subsections or an Inputs table freely.
5. **Self-check**: `python3 scripts/check_strategy.py <report.md> --mode content|competitor|growth`. Fix every FAIL. Review each WARN line and tag or reword it.
6. **Deliver**: save to the path the user named; otherwise `strategy/<YYYY-MM-DD>-<mode>-<subject-slug>.md` under the current directory, and never under a Hugo `content/` folder (Hugo would publish it). Tell the user the path; do not commit it. In chat, give the top three actions and the "Data the user should supply" list. Offer write-article for drafting or write-ideate for topics.

## Evidence contract

Strategy built on invented numbers is worse than none. Every report follows these rules:

- **Tag claims inline**, with these exact openings (a note after a colon is fine, e.g. `[Assumption: 2% churn]`). `[Evidence: <url, file, command, or "user input">]` for sourced or measured facts, `[Inference]` for reasoning from evidence, `[Assumption]` for a value you chose so a calculation can proceed. Arithmetic keeps its inputs' tag; if any input is an assumption, the result is [Assumption]. Numbers in a table can share one tag line under the table.
- **"unknown", not estimates.** Missing facts about the present (traffic, revenue, churn, prices, dates) stay "unknown". Projections may still run on a stated [Assumption] range, listed under Assumptions, so the plan is sized. Never invent revenue, users, installs, testimonials, URLs, or dates.
- **Conflicting figures become ranges**, citing both sources.
- **Cite only what you saw.** A source is a page you fetched, a search result you read, a file, or a command you ran.
- **Close with "Sources and Assumptions"**: numbered sources, the assumptions list, and "Data the user should supply" (what would most change the conclusions).

## Impact and Feasibility rubric (all modes)

| Score | Impact on the goal metric | Feasibility for this team and budget |
|---|---|---|
| 5 | Changes the trajectory of the goal metric | Doable this week with current skills and tools, no spend |
| 4 | Clear, measurable movement on the goal metric | Within a month, small spend or one new tool |
| 3 | Noticeable on a secondary metric or one segment | One to three months, or needs a new skill |
| 2 | Small or local effect | More than three months, or meaningful spend or help |
| 1 | Negligible or unmeasurable | Needs resources the user does not have |

Priority Score = Impact x Feasibility. Sort descending; break ties by Feasibility. A data-gathering action (connect analytics, measure churn) scores Impact by the decisions it unlocks. When the goal metric is unmeasured, scores are judgment: say so once above the table. Growth mode's "ease" is this Feasibility scale; its 0-10 Scorecard is separate.

## Output style

Plain Markdown, short direct sentences, no emdashes, no hype. These reports are working documents, not blog posts, so the blog's writing-style guide does not apply.

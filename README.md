# Writing Skills

Claude Code skills for structured article creation, review, ideation, and strategy. Each skill bundles the writing framework prompts it needs (originally published at [jeffbailey.us/prompts](https://jeffbailey.us/prompts/)).

## Install

This repo is an agent-plugin marketplace. In Claude Code:

```bash
claude plugin marketplace add ~/Projects/skills-writing
claude plugin install jbb-writing-skills@jbb-writing
```

See [SETUP.md](SETUP.md) for Cursor and other tools, and for releasing changes.

## Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| [write-article](skills/write-article/SKILL.md) | `/write:article` | Create articles with 16 bundled writing frameworks plus Comparison (via write-comparison-article-create); for jeffbaileyblog, places the bundle, checks links are published, loops write-review and write-review-apply until the draft scores 9.5+, and verifies the draft build |
| [write-review](skills/write-review/SKILL.md) | `/write:review [article] [framework]` | Review articles against framework rubrics, including comparison pages (read-only) |
| [write-review-apply](skills/write-review-apply/SKILL.md) | `/write:review-apply [article]` | Apply a write-review report: makes the fixes the article supports, lists facts and structural calls for you, validates, and re-scores |
| [write-status](skills/write-status/SKILL.md) | `/write:status [article]` | Which writing skills have run on an article and which are missing or stale; offers write-review (y/N) when it never ran |
| [write-ideate](skills/write-ideate/SKILL.md) | `/write:ideate`, `/write:idea-storm` | Brainstorm article ideas, deduped against existing posts and draft stubs |
| [write-strategy](skills/write-strategy/SKILL.md) | `/write:strategy` (also `/write:competitor-analysis`, `/write:mckinsey-consultant`) | Content strategy, competitor analysis, and growth audits with evidence-tagged claims |
| [write-copy](skills/write-copy/SKILL.md) | `/write:copy`, `/write:landing-page-copy` | Landing pages, CTAs, short emails, ads, and taglines, written only from the product's own facts |
| [write-hook](skills/write-hook/SKILL.md) | `/write:hook [source]` | 50 social media hooks in five tone groups, each with a one-line reader action, plus 12-20 paste-ready hashtags |
| [write-debug](skills/write-debug/SKILL.md) | `/write:debug` (alias `/write:bug-minimizer`) | Bug triage, minimal verified repro, root cause, fix |
| [write-seo](skills/write-seo/SKILL.md) | `/write:seo`, `/write:internal-link-optimize` | Internal links and SEO front matter (title, description, keywords) |
| [generate-cover-image](skills/generate-cover-image/SKILL.md) | `/write:cover` | 1200x630 article cover image from the article's meaning, titled through a Canva brand template for jeffbaileyblog (called by write-article) |
| [hugo-agents-compliance](skills/hugo-agents-compliance/SKILL.md) | `/hugo:agents` | Apply Hugo `AGENTS.md` as written for blog Markdown, then verify with a live ban scan, front-matter check, and a drafts-aware build |
| [create-practice-playground](skills/create-practice-playground/SKILL.md) | `/write:playground` | Build an in-browser practice playground (real program on wasm or v86) for jeffbaileyblog through the nWave waves, plus an optional Learn X article (calls write-article) |
| [write-article-revision](skills/write-article-revision/SKILL.md) | `/write:article-revision` | Fold new source material into an existing article, with conflicts and provenance listed for you |
| [write-comparison-article-create](skills/write-comparison-article-create/SKILL.md) | `/write:comparison-article-create` | Decision-first X vs Y comparison pages with sourced claims and a render check |
| [write-validate-article](skills/write-validate-article/SKILL.md) | `/write:validate-article` | Read-only pre-publish gate: Hugo build first, front matter, live banned-phrase scan, ai-sanitize, lychee, markdownlint-cli2; blocking / warning / noise verdict |
| [write-check-links](skills/write-check-links/SKILL.md) | `/write:check-links` | lychee with the site config, plus ref and /blog/ link checks, triaged broken / false positive / unverified |
| [write-run-markdown-lint](skills/write-run-markdown-lint/SKILL.md) | `/write:run-markdown-lint` | markdownlint-cli2 with your config, findings grouped by rule |
| [writing-clearly-and-concisely](skills/writing-clearly-and-concisely/SKILL.md) | (auto) | Tighten prose by Strunk's rules while keeping voice, facts, links, and code; returns a rule-tagged change list |

The create, revise, copy, review, and validate skills also call [`ai-sanitize`](https://github.com/jeffabailey/skills/tree/main/skills/ai-sanitize) from the [jeffabailey/skills](https://github.com/jeffabailey/skills) collection to remove AI tells from prose, UI copy, and graphics. Creating and revising skills run it in edit mode; review and validate run it in report mode. Install that collection too, or those steps are skipped with a note.

**Cursor:** After `~/Shell/config/configure_mcp.sh distribute`, slash commands match the files in [`.cursor/commands/`](.cursor/commands/) (for example `/write-article`, `/hugo-agents`). Claude Code may use the ` /write:…` style shown above; the workflows are the same.

## Writing Frameworks

### Article Creation (17 frameworks)

**Documentation (Diataxis):** Tutorials, How-to Guides, Reference, Explanation

**Persuasion:** AIDA, Problem-Agitate-Solve, Influence Pieces

**Rhetorical:** Classical Rhetoric, TEA, Thought Pieces

**Instructional:** Backward Design, Lesson Planning

**Reference:** Fact-Based Reference, List Articles, Fundamentals

**Learning:** Learn X (launch pad — teaches the 20% that does 80%, then links curated video/audio/books/online resources)

**Decision:** Comparison (X vs Y; structure and checker from write-comparison-article-create)

### Article Review

Each creation framework has a corresponding review rubric with scoring dimensions, quality thresholds, and specific evaluation criteria.

### Utilities

Idea Storm, Competitor Analysis, McKinsey Consultant, Content Strategy, Landing Page Copy, Short Copy, Bug Minimizer, Internal Link Optimization, Writing Style Guide

## How It Works

Each skill bundles its prompts in its own `references/` folder and reads them from disk; nothing is fetched at runtime. For jeffbaileyblog, skills read the live site rules (hugo/AGENTS.md, content/prompts/writing-style.md, content/prompts/seo-front-matter.md) from the blog repo so they stay current.

This means:
- Prompts are always up to date with the published versions
- No duplication between the blog and these skills
- Private prompts stay private (local filesystem only)

## Setup

See [SETUP.md](SETUP.md) for installation instructions.

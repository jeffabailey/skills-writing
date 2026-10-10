# Writing Skills

Claude Code skills for structured article creation, review, ideation, and strategy. Each skill bundles the writing framework prompts it needs (originally published at [jeffbailey.us/prompts](https://jeffbailey.us/prompts/)).

## Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| [write-article](write-article/SKILL.md) | `/write:article` | Create articles with 16 bundled writing frameworks; for jeffbaileyblog, places the bundle, checks links are published, and verifies the draft build |
| [write-review](write-review/SKILL.md) | `/write:review [article] [framework]` | Review articles against framework rubrics (read-only) |
| [write-ideate](write-ideate/SKILL.md) | `/write:ideate`, `/write:idea-storm` | Brainstorm article ideas, deduped against existing posts and draft stubs |
| [write-strategy](write-strategy/SKILL.md) | `/write:strategy` (also `/write:competitor-analysis`, `/write:mckinsey-consultant`) | Content strategy, competitor analysis, and growth audits with evidence-tagged claims |
| [write-copy](write-copy/SKILL.md) | `/write:copy`, `/write:landing-page-copy` | Landing pages, CTAs, short emails, ads, and taglines, written only from the product's own facts |
| [write-debug](write-debug/SKILL.md) | `/write:debug` (alias `/write:bug-minimizer`) | Bug triage, minimal verified repro, root cause, fix |
| [write-seo](write-seo/SKILL.md) | `/write:seo`, `/write:internal-link-optimize` | Internal links and SEO front matter (title, description, keywords) |
| [generate-cover-image](generate-cover-image/SKILL.md) | `/write:cover` | 1200x630 article cover image from the article's meaning, titled through a Canva brand template for jeffbaileyblog (called by write-article) |
| [hugo-agents-compliance](hugo-agents-compliance/SKILL.md) | `/hugo:agents` | Apply Hugo `AGENTS.md` as written for blog Markdown, then verify with a live ban scan, front-matter check, and a drafts-aware build |
| [write-article-revision](write-article-revision/SKILL.md) | `/write:article-revision` | Fold new source material into an existing article, with conflicts and provenance listed for you |
| [write-comparison-article-create](write-comparison-article-create/SKILL.md) | `/write:comparison-article-create` | Decision-first X vs Y comparison pages with sourced claims and a render check |
| [write-validate-article](write-validate-article/SKILL.md) | `/write:validate-article` | Read-only pre-publish gate: Hugo build first, front matter, live banned-phrase scan, ai-sanitize, lychee, markdownlint-cli2; blocking / warning / noise verdict |
| [write-check-links](write-check-links/SKILL.md) | `/write:check-links` | lychee with the site config, plus ref and /blog/ link checks, triaged broken / false positive / unverified |
| [write-run-markdown-lint](write-run-markdown-lint/SKILL.md) | `/write:run-markdown-lint` | markdownlint-cli2 with your config, findings grouped by rule |
| [writing-clearly-and-concisely](writing-clearly-and-concisely/SKILL.md) | (auto) | Tighten prose by Strunk's rules while keeping voice, facts, links, and code; returns a rule-tagged change list |

The create, revise, copy, review, and validate skills also call [`ai-sanitize`](https://github.com/jeffabailey/skills/tree/main/skills/ai-sanitize) from the [jeffabailey/skills](https://github.com/jeffabailey/skills) collection to remove AI tells from prose, UI copy, and graphics. Creating and revising skills run it in edit mode; review and validate run it in report mode. Install that collection too, or those steps are skipped with a note.

**Cursor:** After `~/Shell/config/configure_mcp.sh distribute`, slash commands match the files in [`.cursor/commands/`](.cursor/commands/) (for example `/write-article`, `/hugo-agents`). Claude Code may use the ` /write:…` style shown above; the workflows are the same.

## Writing Frameworks

### Article Creation (16 frameworks)

**Documentation (Diataxis):** Tutorials, How-to Guides, Reference, Explanation

**Persuasion:** AIDA, Problem-Agitate-Solve, Influence Pieces

**Rhetorical:** Classical Rhetoric, TEA, Thought Pieces

**Instructional:** Backward Design, Lesson Planning

**Reference:** Fact-Based Reference, List Articles, Fundamentals

**Learning:** Learn X (launch pad — teaches the 20% that does 80%, then links curated video/audio/books/online resources)

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

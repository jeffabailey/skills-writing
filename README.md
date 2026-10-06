# Writing Skills

Claude Code skills for structured article creation, review, ideation, and strategy. Each skill references writing framework prompts hosted at [jeffbailey.us/prompts](https://jeffbailey.us/prompts/) rather than embedding them, so the prompts stay in sync with the canonical source.

## Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| [write-article](write-article/SKILL.md) | `/write:article` | Create articles using 15+ writing frameworks |
| [write-review](write-review/SKILL.md) | `/write:review` | Review articles against framework rubrics |
| [write-ideate](write-ideate/SKILL.md) | `/write:ideate` | Brainstorm article ideas and content angles |
| [write-strategy](write-strategy/SKILL.md) | `/write:strategy` | Competitor analysis and growth planning |
| [write-copy](write-copy/SKILL.md) | `/write:copy` | Landing page and marketing copy |
| [write-debug](write-debug/SKILL.md) | `/write:debug` | Structured bug minimization |
| [write-seo](write-seo/SKILL.md) | `/write:seo` | Internal link optimization |
| [generate-cover-image](generate-cover-image/SKILL.md) | `/write:cover` | 1200x630 article cover image from the article's meaning, titled through a Canva brand template for jeffbaileyblog (called by write-article) |
| [hugo-agents-compliance](hugo-agents-compliance/SKILL.md) | `/hugo:agents` | Apply Hugo `AGENTS.md` top-to-bottom for blog Markdown |

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

Idea Storm, Competitor Analysis, McKinsey Consultant, Landing Page Copy, Bug Minimizer, Internal Link Optimization, Writing Style Guide

## How It Works

Skills fetch prompts from `https://jeffbailey.us/prompts/{slug}/` at runtime via WebFetch. Private prompts (Fundamentals, Learn X, Writing Style, Internal Link Optimize) are read from the local filesystem via `additionalDirectories`.

This means:
- Prompts are always up to date with the published versions
- No duplication between the blog and these skills
- Private prompts stay private (local filesystem only)

## Setup

See [SETUP.md](SETUP.md) for installation instructions.

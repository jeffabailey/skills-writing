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

## Writing Frameworks

### Article Creation (15 frameworks)

**Documentation (Diataxis):** Tutorials, How-to Guides, Reference, Explanation

**Persuasion:** AIDA, Problem-Agitate-Solve, Influence Pieces

**Rhetorical:** Classical Rhetoric, TEA, Thought Pieces

**Instructional:** Backward Design, Lesson Planning

**Reference:** Fact-Based Reference, List Articles, Fundamentals

### Article Review

Each creation framework has a corresponding review rubric with scoring dimensions, quality thresholds, and specific evaluation criteria.

### Utilities

Idea Storm, Competitor Analysis, McKinsey Consultant, Landing Page Copy, Bug Minimizer, Internal Link Optimization, Writing Style Guide

## How It Works

Skills fetch prompts from `https://jeffbailey.us/prompts/{slug}/` at runtime via WebFetch. Private prompts (Fundamentals, Writing Style, Internal Link Optimize) are read from the local filesystem via `additionalDirectories`.

This means:
- Prompts are always up to date with the published versions
- No duplication between the blog and these skills
- Private prompts stay private (local filesystem only)

## Setup

See [SETUP.md](SETUP.md) for installation instructions.

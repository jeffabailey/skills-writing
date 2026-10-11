# Setup

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed

Each skill bundles its prompts in its own `references/` directory, so the skills need no network access to load them.

## Installation

This repository is an agent-plugin marketplace (`jbb-writing`) with one plugin, `jbb-writing-skills`. The skills live under `skills/`.

### Claude Code

```bash
claude plugin marketplace add ~/Projects/skills-writing
claude plugin install jbb-writing-skills@jbb-writing
```

Claude Code picks up edits only when `version` goes up in **both** `plugin.json` and `.claude-plugin/plugin.json`. After a bump:

```bash
claude plugin marketplace update jbb-writing && claude plugin update jbb-writing-skills@jbb-writing
```

Then restart Claude Code.

### Cursor, Codex, OpenCode, Kilo and Zed

From your Shell dotfiles repo, run MCP distribution. It symlinks each folder under `skills/` into those tools' skill directories, and the slash commands into `~/.cursor/commands`:

```bash
~/Shell/config/configure_mcp.sh distribute
```

It leaves `~/.claude/skills` alone for plugin repositories, because Claude Code gets the skills from the plugin. Run it again after adding or renaming a skill.

- **Skills** come from `skills/<name>/` (for example `skills/write-article/`).
- **Slash commands** come from `.cursor/commands/*.md` in this repo (for example `/write-article`, `/hugo-agents`).

Override install locations with `SKILLS_REPO_PATH` and `SKILLS_WRITING_REPO_PATH` if your clones live elsewhere.

## Usage

```
/write:article    # Create an article (recommends a framework)
/write:review     # Review an article against its framework
/write:ideate     # Brainstorm article ideas (alias: /write:idea-storm), deduped against the blog
/write:strategy   # Content strategy, competitor analysis, or growth audit
/write:copy       # Landing page, CTA, email, ad, or tagline copy (also /write:landing-page-copy)
/write:debug      # Structured bug analysis
/write:seo        # Internal links + SEO front matter (alias: /write:internal-link-optimize)
/hugo:agents      # Hugo blog AGENTS.md compliance (read site AGENTS.md in order)
```

## Customization

### Using your own prompts

Replace the prompt files in a skill's `references/` directory with your own. Keep the file names, or update the links to them in that skill's `SKILL.md`.

### Adding frameworks

To add a new writing framework:

1. Write the create and review prompts, and save them as `skills/write-article/references/<framework>.md` and `skills/write-review/references/<framework>.md`
2. Add the framework to the tables in `skills/write-article/SKILL.md` and `skills/write-review/SKILL.md`
3. Update `references/prompt-index.md` in both skills
4. Add framework detection signals to `skills/write-review/SKILL.md` workflow step 2

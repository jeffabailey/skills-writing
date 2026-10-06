# Setup

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed

Each skill bundles its prompts in its own `references/` directory, so the skills need no network access to load them.

## Installation

### Claude Code and Cursor (skills + slash commands)

From your Shell dotfiles repo, run MCP distribution. It symlinks each skill folder into `~/.claude/skills` and `~/.cursor/skills`, and the slash commands into `~/.cursor/commands`:

```bash
~/Shell/config/configure_mcp.sh distribute
```

Because the installs are symlinks, edits to a skill take effect without reinstalling. Run it again after adding or renaming a skill.

- **Skills** come from this repository’s skill folders (for example `write-article/`).
- **Slash commands** come from `.cursor/commands/*.md` in this repo (for example `/write-article`, `/hugo-agents`).

Override install locations with `SKILLS_REPO_PATH` and `SKILLS_WRITING_REPO_PATH` if your clones live elsewhere.

### As a skill directory

Add this repository as a skill source in your Claude Code project:

```bash
# Clone the repository
git clone <repo-url> ~/Projects/writing-skills

# In your project's .claude/settings.local.json, add the skills path
```

Or add the individual skill directories you want to your project's `.claude/skills/` directory.

## Usage

```
/write:article    # Create an article (recommends a framework)
/write:review     # Review an article against its framework
/write:ideate     # Brainstorm article ideas
/write:strategy   # Competitor analysis or growth planning
/write:copy       # Landing page / marketing copy
/write:debug      # Structured bug analysis
/write:seo        # Internal link optimization
/hugo:agents      # Hugo blog AGENTS.md compliance (read site AGENTS.md in order)
```

## Customization

### Using your own prompts

Replace the prompt files in a skill's `references/` directory with your own. Keep the file names, or update the links to them in that skill's `SKILL.md`.

### Adding frameworks

To add a new writing framework:

1. Write the create and review prompts, and save them as `write-article/references/<framework>.md` and `write-review/references/<framework>.md`
2. Add the framework to the tables in `write-article/SKILL.md` and `write-review/SKILL.md`
3. Update `references/prompt-index.md` in both skills
4. Add framework detection signals to `write-review/SKILL.md` workflow step 2

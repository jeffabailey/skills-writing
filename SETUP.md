# Setup

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Access to `jeffbailey.us` for fetching prompts

## Installation

### Cursor (skills + slash commands)

From your Shell dotfiles repo, run MCP distribution (installs symlinks into `~/.cursor/skills` and `~/.cursor/commands`):

```bash
~/Shell/configure_mcp.sh distribute
```

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

### Permissions

The included `.claude/settings.local.json` grants:

- **WebFetch** to `jeffbailey.us` for fetching prompts at runtime
- **additionalDirectories** to the local blog prompts directory for private prompts

If you are not Jeff Bailey, update `additionalDirectories` to point to your local copy of the prompts, or remove it if you only use public prompts.

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

Replace the URLs in each `SKILL.md` with your own prompt hosting location. The skills expect to fetch markdown content from the configured URLs.

### Adding frameworks

To add a new writing framework:

1. Create and publish the prompt (create + review variants)
2. Add the framework to the tables in `write-article/SKILL.md` and `write-review/SKILL.md`
3. Update the corresponding `references/prompt-index.md`
4. Add framework detection signals to `write-review/SKILL.md` workflow step 2

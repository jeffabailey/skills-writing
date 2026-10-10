---
name: hugo-agents-compliance
description: Enforces jeffbaileyblog Hugo Markdown rules by reading and applying hugo/AGENTS.md section by section as written, plus any nested AGENTS.md and content/prompts/writing-style.md, then proving it with a live ban-list scan, a front-matter check, and a build that actually renders the page (drafts included). Use when editing or creating content under the Hugo site (hugo/content/), drafting blog posts, fixing Hugo build errors such as REF_NOT_FOUND, or the user says /hugo:agents, "apply AGENTS.md", "Hugo blog rules", or "compliance with hugo AGENTS".
---

# Hugo site: AGENTS.md compliance

For Markdown in the **jeffbaileyblog** Hugo site (`<repo>/hugo/`), the rules in `AGENTS.md` are mandatory. Read the files every session; they change, and a remembered summary goes stale. This skill adds the mechanics AGENTS.md leaves implicit and three scripts so the checks are one command each.

Scripts (paths relative to this skill): `scripts/banscan.py`, `scripts/fmcheck.py`, `scripts/verify-build.sh`. Preflight: `command -v hugo python3`. If one is missing, print the install command (`brew install hugo` / `brew install python`) and report "tool missing", not "check failed".

## 1. Scope the task first

Decide which mode you are in, because it controls how much you touch:

- **New post:** apply every rule below, including SEO wording from `seo-front-matter.md`.
- **Existing post** (a build fix, a link fix, or "make it compliant"): compliance means the *mechanical* rules. Fix what was asked; quote or unquote fields as required (keep the wording); add required fields that are missing (`lastmod` = today, `keywords`, `cover.alt`, a category); and fix banscan BLOCK hits (emdash, banned phrase, inline link, bare ref) with the smallest rewrite of that sentence. Never change `date:`. Do **not** reword an existing title, description, category choice, or untouched prose. That is an editorial or SEO decision the user did not ask for, and many legacy posts predate the current rules. Put those ideas under "suggested, not applied" in your report so the user can opt in.

Profanity is the author's voice in either mode. A compliance pass never removes or softens it.

## 2. Read the rules in their real order

1. Read `hugo/AGENTS.md` top to bottom. Walk its `##` headings **as they appear in the file** and, for each one, write a one-line note: applied / not relevant to this task (and why). Do not substitute a remembered list of sections; if a heading this skill mentions is gone, or a new one appeared, the file wins.
2. Find nested rules: every `AGENTS.md` on the path from `content/` down to the bundle (`find content -name AGENTS.md`). Read each top to bottom. Nearer files add to or override the global file. AGENTS.md text may call a folder by an old name (for example `fundamentals-x`); match on the directory that actually holds the file.
3. Read `content/prompts/writing-style.md` (AGENTS.md's `## Writing style` delegates to it; it wins on conflicts) and, when you set `title`/`description`/`keywords`, `content/prompts/seo-front-matter.md`.

**Do not explore sibling posts or grep `content/` by default.** The front-matter shape is in AGENTS.md, and categories come from `./scripts/generate-site-metadata.py` (prints `categories` and `category_counts`; fall back to `data/site-metadata.json`). **Exception:** when a nested AGENTS.md tells you to match comparable posts (for example the Fundamentals rules for `series:` and `diataxis:`), read the front matter of one or two of the closest siblings in that directory, only the front matter, and say which posts you matched. For "which posts cover X", use the search index AGENTS.md describes (`scripts/site-search` from the repo root) before any grep.

## 3. Apply, then verify with the scripts

Front-matter mechanics that runs keep getting wrong (AGENTS.md has the full shape):

- `url`, `slug`, `cover.image` bare (no quotes); `description` quoted (an unquoted colon breaks YAML), ≤160 chars per `seo-front-matter.md`.
- `slug`, bundle folder, and `url` tail match on new posts. `cover.image: <slug>.png`, `relative: true`, and an `alt` that says what the image shows. Open the PNG before you write `alt`. If the image does not exist yet, write `alt` from the article's subject and flag it for review once the cover is made.
- `categories:` has at least one entry on every content file, posts and pages alike, picked from existing categories (prefer higher counts). Never restate the site's context: use **Software**, not "Software Development"; **Tools**, not "Development Tools". Invent a new category only when nothing fits, and say so.
- New posts: `draft: true`, `date` = `lastmod` = today, `YYYY-MM-DD` only.
- Never add `{{< partial "category_footer" >}}` to a body; `layouts/_default/single.html` already renders it.

Run all three checks after **every** editing pass, including passes by ai-sanitize, other prose tools, or the user. Rewriters reintroduce banned phrases, and you cannot see your own.

1. **Ban scan:** `python3 scripts/banscan.py <index.md>`. It extracts the ban list fresh from the live `writing-style.md` (Skip bullets, the "Things to NOT Do" section, "Using these words") and checks markup: emdash, `<a href>`, inline `[text](url)`, bare `{{< ref >}}`, fences without a language, Markdown tables, body H1, category_footer. BLOCK lines must be fixed; REVIEW lines (contrast framing, "quietly", arrow diagrams) need a judgment call. Add `--list` to see the extracted bans.
2. **AI tells:** after the scan is clean, run the `ai-sanitize` skill (`jbb-skills:ai-sanitize`) in edit mode on what you wrote or changed, then re-run banscan. If it is not installed, say so and continue. Its survival check flags inline links converted to reference-style as LOST; that is expected, since writing-style.md requires reference-style.
3. **Front matter:** `python3 scripts/fmcheck.py <index.md>`. FAIL must be fixed. WARN is fine on legacy posts in targeted-fix mode (slug ≠ folder, no keywords). A WARN for a missing cover file means the post needs `generate-cover-image` (step 4).
4. **Build:** `scripts/verify-build.sh <index.md>`. It runs `hugo --gc --minify` into a temp dir and, when the file is `draft: true`, a second `--buildDrafts` build, because the production build skips drafts and passes even when the draft is broken. It then confirms `<url>/index.html` exists. Any `ERROR` line, including `REF_NOT_FOUND`, is a failure; fix and re-run until `BUILD OK`.

## 4. Fixing REF_NOT_FOUND

`{{< ref "x" >}}` resolves by content path or **bundle folder name**, not by front-matter `slug` (several published posts have slug ≠ folder). To find the right target:

```bash
cd hugo && hugo list all | awk -F, 'NR==1 || /blame/'   # columns: path,slug,title,date,...,draft,permalink
```

Use the folder name from the `path` column (for example `death-by-1000-cuts-3-the-blame-game` from `content/blog/death-by-1000-cuts/death-by-1000-cuts-3-the-blame-game/index.md`). If you only know the topic, query `scripts/site-search "<words>"` from the repo root and read `content_path`. Repoint the ref; do not delete the link. If the target has `draft` = `true`, a published post cannot link to it: the production build will fail. Drop the link or wait until the target is published, and tell the user.

## 5. Cover image handoff

`cover.image` names `<slug>.png` beside `index.md`. If fmcheck reports the file missing, the page's og:image points at nothing. Do not invent an image: tell the user, and offer the `generate-cover-image` skill (it builds the Canva cover and writes the PNG) as the next step.

## 6. Report

End with: mode (new / compliance pass / targeted fix); the AGENTS.md headings walked with applied/not-relevant notes; nested AGENTS.md files applied and any siblings matched; banscan, fmcheck, and verify-build results (exit codes, page path); "suggested, not applied" items for legacy posts; cover handoff if needed. Do not commit or push unless asked (AGENTS.md's `## Git` section says how when the user does ask).

## When this skill does not apply

Non-Hugo repos, non-Markdown assets, or tasks the user limits to unrelated files.

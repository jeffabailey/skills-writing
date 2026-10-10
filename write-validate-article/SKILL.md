---
name: write-validate-article
description: Validates one Markdown article for the jeffbaileyblog Hugo site before it ships and returns a three-level verdict (blocking / warning / noise). Runs the Hugo build first as the gate (drafts included, into a temp dir), then a front-matter check, a banned-phrase scan read live from writing-style.md, an AGENTS.md compliance pass, one ai-sanitize report, link checking (lychee), and Markdown linting (markdownlint-cli2). Report-only unless the user asks for fixes. Use when the user says /write:validate-article, wants to validate an article, check an article before publishing, "run all the checks" on a Markdown file, or asks whether a post is ready to publish.
---

# Validate Article

Run every check on one article for the **jeffbaileyblog** Hugo site and say, without noise, whether it can ship. The output is a report with a verdict; this skill does not edit unless the user asks (see "Fixing").

To *write or repair* a post to the AGENTS.md rules, use `hugo-agents-compliance`. This skill is the read-only gate.

Scripts (relative to this skill): `scripts/hugo_build.sh`, `scripts/check_front_matter.py`, `scripts/banned_scan.py`.

## Severity: three levels

Every finding goes in exactly one bucket. A report that lists noise as errors teaches the user to ignore it, so triage is part of the job.

* **BLOCKING:** the article must not ship. Hugo build errors (including `REF_NOT_FOUND`) or the page not rendering; front-matter BLOCKING lines; any banned-phrase hit; a `{{< ref >}}` to a post that is `draft: true` while this one is not; an external link confirmed dead (404/410, DNS failure) after a second look; markdownlint MD040 (writing-style requires a fence language).
* **WARNING:** worth fixing, does not stop publishing. Front-matter WARNING lines (description over 160 chars, slug/dir/url mismatch, missing cover file); ai-sanitize findings not already caught by the scan; AGENTS.md judgment items (voice, structure, cards vs tables); other markdownlint findings under the applied config; external links that timed out (unverified).
* **NOISE:** shown in one line, never counted. MD013 or MD052 firing (proof the lint config was not applied, not an article problem); lychee 404 on the cover image when the file exists beside `index.md` (lychee resolves bundle images against the site root); 403/429/999 that `lychee.toml` already accepts.

Verdict: **FAIL** if anything is blocking; **PASS WITH WARNINGS**; or **PASS**. If a tool was missing, the stage reads `NOT RUN (tool missing)` and the verdict carries `(incomplete: <stage>)`. A missing tool is never "check failed" and never "passed".

## Workflow

### 0. Preflight and paths

* Target: the path the user gave. If none, ask. Validate the file in place.
* Site root: the nearest parent holding `config.toml` and `content/` (this site uses `hugo/config.toml`, not `hugo.toml`). Repo root: `git rev-parse --show-toplevel`.
* Tools: `command -v hugo python3 lychee markdownlint-cli2 npx`. Missing installs: `brew install hugo lychee python`, `npm i -g markdownlint-cli2@0.18.1` (or use `npx -y markdownlint-cli2@0.18.1`). Do not substitute `markdownlint` (cli v1): it ignores the user's cli2 config.
* Read the front matter now. `draft: true` decides the build flags in step 1.

### 1. Hugo build (the gate, runs first)

```bash
bash scripts/hugo_build.sh <index.md>
```

It builds the whole site with `hugo --gc --minify` into `mktemp -d` (never the repo's `public/`), adds `--buildDrafts` when the target is a draft (new posts are `draft: true` and the config does not build drafts, so a plain build "passes" without rendering the page), greps the log for `ERROR`/`REF_NOT_FOUND`, and confirms `<url>/index.html` exists. Results: `BUILD OK` (exit 0); `BUILD FAILED` (exit 1: an error names this file, or its page did not render) is BLOCKING; `SITE BUILD BROKEN by other files` (exit 3: no error names this file) is a WARNING for this article, but say plainly that the site cannot deploy until those files are fixed, and name them. The full build takes 10-60 seconds.

It runs first because it is the only check that resolves internal links and the one that decides pass/fail. Keep going after a failure: the other checks are independent, and the user wants every problem in one report.

When `REF_NOT_FOUND` fires, name the fix: `ref` resolves by content path or bundle folder name, not front-matter `slug`. Find the real target with `cd hugo && hugo list all` (the `path` column; filter `draft` = `false` for published posts) and give the corrected ref.

Draft links: a draft built with `--buildDrafts` resolves refs to other drafts, so the build cannot catch them. For each `{{< ref "x" >}}` in the file, check the target's `draft` column in `hugo list all`; a link from a post that will publish to a draft is BLOCKING.

### 2. Front matter

```bash
python3 scripts/check_front_matter.py <index.md>
```

Checks what the build lets through: bare `url`/`slug`/`cover.image`; `date`/`lastmod` as `YYYY-MM-DD` (no ISO timestamps); `description` present, quoted, ≤160 chars; `slug` = bundle dir = `url` tail; `cover.image` = `<slug>.png` and the file exists beside `index.md`; `cover.alt`; `type: post`, `author: Jeff Bailey`; 4-7 keywords. Its BLOCKING/WARNING/INFO labels map straight onto the severity buckets. Many legacy posts have no `slug:`; the script falls back to the url tail, then the bundle dir.

### 3. AGENTS.md compliance pass (read the live rules)

Read the files every run; they change.

1. `hugo/AGENTS.md` top to bottom. Walk its `##` headings **as they appear in the file**, writing one line per heading: checked / not relevant (why). Do not use a remembered list of sections; if a heading is new or gone, the file wins. (There is no "SEO checklist" or "Publishing checklist" section; do not look for one.)
2. Every `AGENTS.md` on the path from `content/` to the bundle (`find hugo/content -name AGENTS.md`). Nearer files add to or override the global one.
3. `content/prompts/writing-style.md`. It wins over AGENTS.md on conflicts. It pulls in `content/prompts/seo-front-matter.md` through an `include-prompt` shortcode; read that too, since it holds the `title`/`description`/`keywords` rules.

Scripts cover the mechanical rules. Spend this pass on the ones that need judgment: voice (Diátaxis how-to/tutorial/reference/explanation use "you", never "I"); post structure (intro, main, conclusion); cards shortcode instead of comparison tables; Mermaid (prefer `graph TB`) instead of ```` ```text ```` diagrams; heading hierarchy with no H1 in the body; alt text on every image; no `{{< partial "category_footer" >}}` in the body (`layouts/_default/single.html` already renders it). Report these as WARNING unless a rule is stated as NEVER/must, then BLOCKING.

### 4. Banned-phrase scan

```bash
python3 scripts/banned_scan.py <index.md>      # --list prints the extracted bans
```

It reads the ban list from the live `writing-style.md` every run: inline `Skip "..."` bullets (the phrase, not the suggested replacement), quoted bullets under `## Writing Style: Things to NOT Do`, `Using these words:`, and contrast-framing templates (`it's not X, it's Y`, `This isn't A. It's B.`, `Not X. Y.`). It also flags emdashes, `<a href>`, inline `[text](url)`, and bare `{{< ref >}}` in body text. It skips code fences and front matter other than `title`/`description`. Every hit is BLOCKING; quote the line and give the rewrite.

Do not skip it because the prose "looks fine". Author-blindness is why it exists.

### 5. AI-tell scan (once)

Invoke the `ai-sanitize` skill (`jbb-skills:ai-sanitize`) once, in **report** mode, on the target. Do not also run its Detect greps by hand: that is the same check twice. Merge its findings with the scan: anything banned_scan already reported stays under step 4; the rest (triads, signposting, decorative formatting) are WARNING. Its survival check flags inline links converted to reference-style as LOST; writing-style requires reference-style, so that is noise. If ai-sanitize is not installed, mark the stage NOT RUN.

### 6. Links (external only)

Invoke the `write-check-links` skill on the target. If you run lychee yourself, run it **from the repo root** so the repo-root `.lycheeignore` applies (lychee reads it only from the cwd):

```bash
cd "$(git rev-parse --show-toplevel)" && lychee --config hugo/lychee.toml hugo/content/.../index.md
```

lychee checks only external `http(s)` URLs. It cannot resolve `{{< ref >}}` links; write-check-links adds a ref table checked against `hugo/content`, but step 1 is the authority, so count a broken ref once, under the build. Triage per the severity list: a cover-image 404 is noise once you confirm the PNG sits beside `index.md`; re-check a 404 in a second request before calling it BLOCKING.

### 7. Markdown lint

Invoke the `write-run-markdown-lint` skill on the target (it runs `markdownlint-cli2` with the project or `~/Shell` `.markdownlint-cli2.jsonc`, falling back to `npx -y markdownlint-cli2@0.18.1`). Use its result as-is. If MD013 or MD052 fire, the config was not applied: report that as NOISE plus a one-line note, and do not count those findings.

### 8. Report

Keep it scannable:

```
VERDICT: FAIL | PASS WITH WARNINGS | PASS  [(incomplete: <stage>)]
Target: <path>  draft: <true/false>  page: <rendered path or "not rendered">

| Stage | Result | Blocking | Warning | Noise |
| Hugo build | BUILD OK / FAILED / NOT RUN | n | n | n |
| Front matter | ... |
| AGENTS.md pass | ... |
| Banned phrases | ... |
| ai-sanitize | ... |
| Links (lychee, external only) | ... |
| Markdown lint (cli2) | ... |

BLOCKING
- <stage> <file>:<line> <what> -> <exact fix>
WARNING
- ...
NOISE (not counted): <one line each>
AGENTS.md headings walked: <heading: checked / n/a (why)>
```

Every BLOCKING item names the line and the concrete fix (the rewritten sentence, the bare value, the corrected ref).

## Fixing

Validation is report-only. After the report, offer to fix the BLOCKING items (and warnings the user picks). Edit only after the user says yes, or when the original request already asked to fix ("validate and fix", "make it pass"). After any edit, re-run steps 1, 2, and 4 on the changed file; rewriting reintroduces banned phrases.

When fixing, change only what the finding names. Profanity is the author's voice, not a defect: never remove or soften it. Do not rewrite a published post's title, description, or keywords unless asked; list those as suggestions.

## Outside jeffbaileyblog

For Markdown outside this Hugo site, skip steps 1-5 and run only links (step 6) and lint (step 7), and say which checks did not apply.

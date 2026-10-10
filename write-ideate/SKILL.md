---
name: write-ideate
description: Brainstorms article ideas for a blog, checks each idea against what is already written (published posts and draft stubs), and hands back ready-to-write ideas with slug, section, categories, closest existing post, and the write-article framework to use. Use when the user says /write:ideate or /write:idea-storm, wants to brainstorm topics, generate article ideas, find gaps in what they have written, explore content angles, or asks "what should I write about". Triggers on "brainstorm", "idea storm", "article ideas", "content ideas", "post ideas", "topic ideas", "what should I write about", "what haven't I written about".
---

# Writing Ideation

Also invoked as `/write:idea-storm` (the old shortcut; same workflow).

Generate article ideas that are specific, not already on the blog, and ready to hand to `/write:article`. The hard part of ideation on a blog with 1,200+ posts is not generating ideas, it is not proposing posts that already exist. A raw brainstorm duplicated live posts and draft stubs in every baseline run, so the dedupe step is not optional.

## Bundled files

* `references/idea-storm.md`: the brainstorming prompt. Variables are bare `{{name}}`; defaults are below.
* `scripts/blog_index.py`: read-only index of jeffbaileyblog posts and categories (stdlib Python; uses PyYAML if present). Run `python3 scripts/blog_index.py --help`.

## Workflow

### 1. Fill the variables from the request

Pre-fill everything the request already says. Use these defaults for the rest, show the filled values in one line, and continue. Ask (once, all missing fields in one message) only when the **topic** is missing; "unknown" or "you pick" is a valid answer.

| Variable | Default |
|---|---|
| `topic` | required; from the request |
| `perspective` | working software engineers and engineering leads |
| `quantity` | 10 |
| `constraints` | not already on the blog; specific titles; writable without invented facts |
| `coverage` | filled by step 2 |

### 2. Coverage pass (what already exists)

For jeffbaileyblog (`~/Projects/websites/jeffbaileyblog/hugo`, or any Hugo site with `content/blog`), run from the Hugo dir:

```bash
python3 <skill>/scripts/blog_index.py --hugo coverage "kw1, kw2, kw3"   # 5-10 topic keywords and synonyms
python3 <skill>/scripts/blog_index.py categories                        # valid category slugs and titles
```

`--hugo` takes draft flags from `hugo list all` (the source of truth); without hugo it falls back to front matter and says so. Every post is labeled `published`, `DRAFT`, or `FINISH-INSTEAD (draft stub)` (draft with under 200 body words).

Summarize the result in two or three lines and pass it in as `{{coverage}}`: how many published posts, drafts, and stubs touch the topic, and whether the area is **saturated**, **partly covered**, or a **gap**. Most of the blog is draft (about 1,000 of 1,280 bundles), so a topic "already written" is often a 5-line stub. Say so; it changes the advice.

For other sites, ask where existing content lives or take a list from the user. If there is no existing content, say "no existing content checked".

### 3. Brainstorm

Read `references/idea-storm.md`, substitute the variables, and generate about 1.5x `quantity` raw ideas so the dedupe step has room to drop some.

### 4. Dedupe every idea

For each raw idea:

```bash
python3 <skill>/scripts/blog_index.py --hugo match "<idea title plus 2-3 core terms>" -n 5
```

* Score 0.6+ against a published post: drop it, or reframe it with a different reader, format, or angle and name the post it differs from.
* Score 0.6+ against a draft or stub on the same subject: do not propose a new post. Put it under "Finish this instead" with its path. Stubs are often one link and a title, so open it (`head -20 <path>`) to see what it was meant to be; if the subject differs (a "Do We Need Pull Requests?" stub vs an idea about reviewing agent-written PRs), keep the idea and name the stub as closest.
* Title scores miss semantic duplicates (a "What Is Observability" idea scores 0.5 against "Fundamentals of Monitoring and Observability"). For the top match of every surviving idea, read the description, and read the body when the score is above 0.3, before deciding it is new. Also match on the idea's core concept, not only its headline words (a "who owns the bus factor" idea must be checked against "bus factor").
* Big published posts cover many sub-topics as sections that no title score finds (Fundamentals of Monitoring and Observability has sections on RED/USE, structured logging, sampling, profiles, and alerting). List the `##`/`###` headings of the 2-3 largest published posts from the coverage pass (`grep -n '^#' <path>`) and treat a matching heading as existing coverage: drop the idea or make it a deeper, narrower post that names that post.
* Every surviving idea records its closest existing post (path, status) or "none (best match below 0.3)". Make sure the proposed slug is not already in the `posts` output.

### 5. Shape each surviving idea

Use the output format in `references/idea-storm.md`. Fields that need checking:

* **Section**: an existing folder under `content/blog/`: how-x, learn-x, what-x, why-x, think-x, fundamentals, x-vs-x, lists, reference, death-by-1000-cuts, troubleshooting, developer-tools, career-development, book-reviews, 1000-life-giving-potions.
* **Categories**: the category **titles** from the `categories` output (front matter uses titles such as `Observability`; folder names are slugs). Never invent a category; if none fits, say "none fits: consider adding <name>".
* **Framework**: one of the 16 write-article frameworks: Tutorials, How-to Guides, Reference, Explanation (the four Diataxis types), AIDA, Problem-Agitate-Solve, Influence Pieces, Classical Rhetoric, TEA, Thought Pieces, Backward Design, Lesson Planning, Fact-Based Reference, List Articles, Fundamentals, Learn X. Section usually decides it: fundamentals -> Fundamentals, learn-x -> Learn X, how-x and troubleshooting -> How-to Guides, what-x -> Explanation, why-x and think-x -> Thought Pieces or Classical Rhetoric, lists -> List Articles, reference -> Reference or Fact-Based Reference, death-by-1000-cuts -> Problem-Agitate-Solve. x-vs-x goes to `/write:comparison-article-create` instead of write-article.
* **Facts needed**: ideas never carry invented numbers, quotes, search volumes, or personal anecdotes. Anything the author must supply or verify is a `[NEEDS FACT: ...]` item.

### 6. Report

Return in chat (no files unless asked):

1. One line of filled variables and the coverage verdict.
2. The ideas, best first, in the prompt's format.
3. **Finish this instead**: draft stubs that match the topic, with paths.
4. **Dropped as duplicates**: each raw idea removed and the post it duplicated (keeps the dedupe honest and visible).
5. **Gaps that remain**: sub-areas neither the blog nor these ideas cover.
6. Next step: `/write:article <idea>` (or `/write:comparison-article-create` for x-vs-x, `/write:strategy` for competitive research first).

Plain prose: no emdashes, no marketing filler. This is a planning list for the author, so the blog's full writing-style rules do not apply here; write-article applies them when the post is drafted.

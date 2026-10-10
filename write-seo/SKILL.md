---
name: write-seo
description: On-page SEO for the jeffbaileyblog Hugo site in two modes. Links mode adds contextual reference-style internal links from a post to other published posts (verified against `hugo list all` and a Hugo build). Front-matter mode rewrites or checks `title:`, `description:`, and `keywords:` against the blog's seo-front-matter prompt. Use when the user says /write:seo or /write:internal-link-optimize, wants to optimize or add internal links, cross-link posts, improve navigation between posts, boost SEO through contextual linking, or fix a weak page title, meta description, SEO title, or front matter keywords. Triggers on "internal links", "link optimization", "SEO links", "cross-linking", "internal linking strategy", "keywords", "front matter keywords", "meta description", "page title", "SEO title".
---

# Write SEO: internal links and front matter

Also invoked as `/write:internal-link-optimize` (that skill was merged into this one).

Two modes. Pick from the request; if it names both, run links first, then front matter.

| Mode | Job | Rules |
|------|-----|-------|
| Links | Add internal links from one post (or a few) to published posts | `references/internal-link-optimize.md` |
| Front matter | Write or check `title:`, `description:`, `keywords:` | blog `hugo/content/prompts/seo-front-matter.md` (authoritative); `references/seo-front-matter.md` is an offline fallback |

Both modes **edit the file in place** and then report. Only give recommendations without editing when the user asks for a review or a dry run.

`scripts/seo_posts.py` (stdlib Python) does the mechanical checks so you don't rebuild them each run. `--hugo-dir` defaults to `~/Projects/websites/jeffbaileyblog/hugo`; pass `--csv FILE` to reuse a saved `hugo list all` output.

## Preflight

Run `command -v hugo python3`. If one is missing, report "tool missing" with the install command (`brew install hugo`, `brew install python`) and stop; that is different from a check that ran and failed.

## Facts this skill depends on (verified on the blog)

* `hugo list all`, run inside `hugo/`, is the only source of truth for what is published. Use rows with `draft=false` under `content/blog/`, skipping `_index.md`. A post missing from the list, or marked as a draft, gets no link, however good a match it is. A ref to a draft breaks the normal build.
* **`ref` resolves by content path / bundle folder name, not by the front-matter `slug`.** About a dozen published posts have a slug that differs from their folder. For example, `ref "how-do-i-use-github-private-mirrors"` (the slug) fails with REF_NOT_FOUND, while `ref "how-do-i-use-private-mirrors"` (the folder) works. Take the value from the `ref` column of `seo_posts.py list`, which is the folder name from the `path` column. The blog's AGENTS.md phrase "slug only" means "no `/blog/...` prefix"; when slug and folder differ, use the folder.
* Hugo config is `hugo/config.toml`. Drafts are not rendered by a plain build.
* Never add `{{< partial "category_footer" >}}`; the layout renders it.
* Profanity in the user's posts is intentional; never touch it.

## Links mode

1. **Scope.** Use the post the user named. If none was named, use the most recently changed `index.md` under `content/blog/` (`git -C <blog> status` / `git log -1 --name-only`) and say which one you chose. Don't stop to ask.
2. **List published posts.** Run `python3 scripts/seo_posts.py list`. It runs `hugo list all` and keeps published blog posts, with columns `ref` (the folder name), title, and path.
3. **Read the target** post. Note its word count, its existing internal refs (so you don't link the same target twice), and its key concepts.
4. **Find candidates by topic, across all dates.** There is no recency window: older cornerstone posts are often the best targets. Use `seo_posts.py list --match term1 term2 ...` on titles and paths. If the blog's search index exists, `scripts/site-search "term"` (run from the repo root, per AGENTS.md "Searching existing posts") finds posts that discuss the topic in their body. Keep only candidates that appear in the published list, and skim each candidate's headings before you link to it.
5. **Apply `references/internal-link-optimize.md`**: reference-style links, existing phrases as anchors, the link budget below, and front matter left alone.
6. **Edit in place.** Put each label definition `[label]: {{< ref "<folder>" >}}` with the post's other internal definitions, kept separate from the external ones.
7. **Verify.**
   * `python3 scripts/seo_posts.py refs <file>` must print no `FAIL` (it catches drafts and slug-instead-of-folder).
   * Build from `hugo/` into a temp dir so `public/` stays untouched: `OUT=$(mktemp -d); hugo --gc --minify -d "$OUT"`. If the edited post is itself a draft, add `--buildDrafts`. Confirm the page exists with `find "$OUT" -path "*<folder>/index.html"`. Any `REF_NOT_FOUND` is a failure: fix it, then rebuild.
8. **Report** in the prompt's output format: each link (context, target, anchor, definition), total added (0 is a valid answer), the word count and the budget you applied, and any slug/url mismatches or front-matter problems you noticed but didn't fix.

### Link budget and new sentences

* Anchor on a phrase that is already in the prose. **Don't write new sentences in body prose** just to hold a link. If a strong target has no natural anchor, add one bullet to an existing "Related", "Further reading", or "Next steps" list, or name it in the report as a suggestion. Never create that section in a short post.
* Short posts (under about 1,500 words) get at most 1 new link per ~400 words, and total internal links stay at or below 1 per 200 words. Long Learn X, reference, or hub posts have no fixed cap, but every link must be one a reader would actually follow.
* Link each target once. Don't link inside code blocks, headings, front matter, or command tables.

## Front-matter mode

1. **Load the rules.** Read `<blog>/hugo/content/prompts/seo-front-matter.md`; it is authoritative. Run `python3 scripts/seo_posts.py drift`. If it reports **DRIFT**, follow the blog file and tell the user the bundled copy is stale (`drift --update` refreshes it). If it reports offline, use `references/seo-front-matter.md`.
2. **Read the article body**, not just the front matter. Keywords must name things the body actually covers, and the description must be accurate.
3. **Draft** the title, description, and keywords following the rules: primary keyword first, labels after it. A "What Is X?" title already leads with the search phrase, so keep it. The description is 1-2 sentences, at most 160 characters, and leads with the keyword. Use 4-7 long-tail keywords, lowercase except proper nouns (`Python`, `AWS Lambda`), with the primary keyword first and none repeating a `categories:` value.
4. **Edit in place.** Double-quote the `description`, leave `url` and `slug` bare and unchanged, and don't touch other fields. Changing the title doesn't change the slug or url; report a slug-alignment issue instead of changing it.
5. **Check.** `python3 scripts/seo_posts.py fm <file>` must print `PASS`. It checks title uniqueness against `hugo list all`, quoting, the 160-character limit, the keyword count, and keywords that repeat categories. Then run the same temp-dir Hugo build as in links mode (with `--buildDrafts` for a draft).
6. **Report** old and new values side by side, with the character counts and a one-line reason for each change.

## Reference

* Prompts are published at https://jeffbailey.us/prompts/. The blog source is `hugo/content/prompts/`.
* Title, description, and keyword rules follow [Google's SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide).

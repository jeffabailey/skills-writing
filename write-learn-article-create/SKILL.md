---
name: write-learn-article-create
description: Creates Learn X launch-pad articles using the Learn Article Create prompt from jeffbailey.us. Direct shortcut — skips framework selection. Use when the user says /write:learn-article-create.
---

# Learn Article Create

Direct shortcut to create articles using the Learn Article Create framework. Skips framework selection — use `/write:article` if you want recommendations instead.

A Learn X article is a **launch pad to a learning track**: it teaches the 20% of a topic that lets a reader do 80% of the work, then links the best video, audio, books, and online resources so they can go deeper. Articles live in `content/blog/learn-x/learn-[topic-slug]/index.md`.

## CRITICAL: Second-person voice + the launch pad are non-negotiable

Learn X articles are written as **Diátaxis How-to guides**. Write in **second person and imperative voice**.

- Use "you" for outcomes ("you'll have a working analyzer") and bare imperatives for actions ("Run this", "Create the file").
- Avoid first person in the article's own voice. A brief first-person aside is acceptable **only** when personally recommending a resource ("I recommend...").
- Do NOT copy the first-person voice some existing `learn-x` siblings use (e.g. `learn-python` says "I'll explain"). The authoritative `hugo/content/prompts/writing-style.md` Diátaxis voice override wins.

Every Learn X article MUST end with a **"Beyond the Basics" launch pad** (📹 video, 🔊 audio, 📚 books, 🌐 online) plus a **Related Content** section, and MUST lead with an explicit **20/80 core**. Never ship without these.

## Prompt Caching

All prompts are cached locally as markdown to avoid repeated network fetches.

**Cache directory**: `~/.claude/cache/writing-prompts/`

**To load the prompt**:

1. Check if `~/.claude/cache/writing-prompts/learn-article-create.md` exists
2. If it exists, read and use it
3. If it does not exist, fetch and cache it:
   ```bash
   mkdir -p ~/.claude/cache/writing-prompts && curl -s "https://jeffbailey.us/prompts/learn-article-create/raw.html" | pandoc -f html -t markdown --wrap=none -o ~/.claude/cache/writing-prompts/learn-article-create.md
   ```
4. Read the newly cached file and use it

**To refresh a cached prompt**: delete the cached file and re-fetch using step 3.

## Workflow

1. **Understand the request** -- Ask the user what topic they want to learn/teach (the tool, platform, protocol, language, or concept), who the audience is, and whether the article should include a hands-on build.

2. **Load the prompt** -- Load the Learn Article Create prompt (slug: `learn-article-create`) using the caching steps above.

3. **Gather variables** -- If the loaded prompt contains template variables in the format `{{variable_name|default="value"}}`:
   - **Has a non-empty default**: Present the default and let the user accept or override it.
   - **Has an empty default** or **no default**: The user **must** provide a value. Show the HTML comment examples as suggestions to choose from.

   Present all variables at once (`topic_name`, `audience_level`, `hands_on`). Pre-fill any values already clear from the user's initial request.

4. **Apply the prompt** -- Substitute all gathered values into the template variables, then follow the loaded prompt instructions to create the article. Decide `hands_on` yourself when set to "auto" — do not ask again.

5. **Apply writing style** -- If the article is for jeffbaileyblog, also load the writing style guide (slug: `writing-style`) using the same caching steps. When the fetched prompt and `writing-style.md` disagree, `writing-style.md` wins — in particular the Diátaxis voice override (no first person in the article's own voice).

6. **Verify the launch pad and core before delivering** -- Confirm the draft has:
   - An explicit 20/80 core section (the essential concepts/commands), not a reference dump.
   - A "Beyond the Basics" section with video and books (plus audio/online where they exist), using specific, current resources — not bare homepages.
   - A Related Content section.
   - `{{< partial "learn_x_header" >}}` after front matter and `{{< partial "category_footer" >}}` before the link definitions.
   - Unquoted `url`/`slug`, a bare `cover.image` with `relative: true`, `type: post`, `author: Jeff Bailey`, and `YYYY-MM-DD` dates matching the `url`.

   Then grep for stray first-person author voice and fix every hit (resource recommendations excepted):

   ```bash
   grep -niE "\b(I|I'm|I've|I'll|my|we|our|us)\b" path/to/index.md | grep -viE "style |graph (TB|TD|LR)|fill:#"
   ```

7. **Deliver the draft** -- Present the article draft to the user for review.

## Reference

All writing framework prompts are maintained at https://jeffbailey.us/prompts/

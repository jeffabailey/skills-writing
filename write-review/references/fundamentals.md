<!-- Site override. Preserved from the standalone write-fundamentals-article-review skill during consolidation.
     This block outranks the prompt that follows it. -->

## Voice for Fundamentals (site rule)

Fundamentals articles are **Diátaxis explanation** content (`diataxis: explanation`), but the site's `writing-style.md` exempts them from the Diátaxis no-first-person override:

- First person ("I") in the author's judgments and experience is **allowed**; do not flag it or recommend converting it.
- Reader-facing scaffolding must be second person (checked below). Flag "I" there.
- Flag "we", "our", and "us" anywhere.
- Do not reward or penalize an article for having or lacking an "I" voice.

The live rule is in the blog's `hugo/content/prompts/writing-style.md` (Voice override for Diátaxis articles); it wins if this file disagrees. This overrides the base rubric's voice guidance.

---

You are a fundamentals article quality reviewer for this Hugo blog.

This prompt is for reviewing articles in `content/blog/fundamentals/`. These articles are Diátaxis Explanation articles, they exist to help readers understand concepts and answer why questions. Reference: [Diátaxis](https://diataxis.fr/).

**Review only.** Do not edit the article, and do not loop toward a target score. Report findings with exact replacement text; the author, or a calling skill such as `write-article-revision`, decides what to apply.

## Required Base Rubric

**CRITICAL:** Read `diataxis-article-explanation.md` (beside this file in `references/`) and apply it in full as the base rubric, including its type gate, review options, and output format. Fundamentals articles are Diátaxis Explanation articles.

After you complete that review, apply the extra blog-specific checks below. They can lower the score on their own.

## Extra Blog-Specific Checks, Fundamentals-x

* **Voice, reader-facing scaffolding:** Reader-facing scaffolding is second person (see the rule at the top); the author's own judgments may use "I". These sections are where a misplaced "I" does harm. Flag as a FAIL any of these written with "I", because they make the author the subject of the reader's experience:

  * Learning Outcomes: must read "By the end of this article, you will be able to", never "I will be able to".
  * TL;DR: "If you only remember one workflow", never "If I only remember one workflow".
  * Prerequisites: "What you should know", never "I should know".
  * Escape routes: "If you need X, read Section Y", never "If I need".
  * Quick Check: "test your understanding", never "I should test my understanding".
  * Self-Assessment: "see if you can explain these concepts in your own words", never "I can explain".
  * Getting Started: "If you're new to [topic]", never "If I'm new to".

  Give exact replacement text for each violation.

* **No "we"/"our":** Flag any first-person plural as a violation.
* **No H1 in body:** The article should not include a `#` heading.
* **No body category footer:** `layouts/_default/single.html` already renders the category footer. Flag any `{{</* partial "category_footer" */>}}` in the body as a duplicate to remove.
* Look in the fundamentals directory for other articles and use them as structural examples, not as voice examples; the override above sets the voice.

## Output Format

Use the JSON plus Markdown output format defined in `diataxis-article-explanation.md`.

In your markdown review, add a final section:

### Blog-Specific Fixes

List the exact edits required for the extra checks above, with exact replacement text where possible.

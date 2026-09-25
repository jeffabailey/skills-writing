This is the one place SEO rules live on this site. Every other prompt, skill, and
guide points here instead of restating them, so there is exactly one copy to keep
current.


These rules follow Google's SEO Starter Guide. Hugo renders front matter `title:` as both the `<title>` element and the on-page H1, and `description:` as the meta description, so those two fields are what Google uses to build the search snippet. Treat them as part of the writing task, not as metadata to fill in afterward.

## Precedence: the keyword comes first, the label comes second

**Front-load the primary keyword, and place any type, series, or category label after it.** A leading prefix such as `Reference:`, `Guide:`, `Deep Dive:`, or `Part 3:` pushes the phrase people actually search away from the start of the title, where both Google and a scanning reader weigh it most.

* Write `jq Cheat Sheet: Filters, Operators, and Output Formats`, and skip `Reference: jq Cheat Sheet`.
* Write `Digital Fat, Deadly Cut 12`, which already leads with the topic and keeps the series label behind it.
* Apply the same order to the slug. `jq-cheat-sheet` earns the phrase; `reference-jq-cheat-sheet` spends the first two syllables on a label nobody searches.

When a section convention and this rule disagree, **this rule wins**, and the article type still gets recorded in `diataxis_type:` or `articletype:` and in `categories:`, where it belongs. Do not raise the conflict as a question; front-load and move on.

## `title:`

* **Unique to the page.** Before settling on one, confirm no sibling post uses it or a near-identical variant.
* **Clear, concise, and accurate.** A reader seeing only the title in search results should know what they get by clicking.
* **Front-loaded.** The subject opens the title, per the precedence rule above.
* **No keyword stuffing.** Repeating a phrase violates Google's spam policies and reads as tiring. The primary keyword appears once, naturally.
* **No forced length.** Google sets no minimum or maximum, but search results truncate long titles, so keep the essential meaning inside the first ~60 characters.

## `description:`

* **One or two complete sentences**, written as prose rather than a keyword list.
* **Unique to the page.** Never copy a description between posts or leave a section default in place.
* **Leads with the primary keyword phrase**, then states concretely what the article covers. Specifics beat vague promises: "how bronze, silver, and gold layers turn raw data into trusted tables" beats "everything you need to know".
* **Accurate, never clickbait.** A mismatch sends readers straight back to the results page, which costs more than any wording gains.
* **≤160 characters.** Snippets truncate around there, so put the essential message in the first sentence.

## `keywords:`

* **Four to seven entries.** Fewer wastes the field; more dilutes relevance and reads as stuffing.
* **Primary keyword first**, matching the title's intent and appearing naturally in the description and opening paragraphs.
* **Long-tail over generic.** Prefer `terraform state locking` over `cloud`. Single generic words almost never rank.
* **Match the content, not the aspiration.** Every keyword names something the article substantively covers.
* **Lowercase by default**, keeping proper nouns capitalized (`AWS Lambda`).
* **No duplication.** Skip the post's `categories:` values, and pick the strongest form of each phrase once rather than listing near-identical variants.
* **Refresh on update.** When a post is substantively revised, re-check the list against the new content.

## Cross-field consistency

`title:`, `description:`, and the first `keywords:` entry must agree on topic and intent, with no drift between them. The description extends the title with scope or payoff rather than restating it.

## The rest

* Use relevant keywords naturally in the body.
* Use proper heading hierarchy (##, ###).
* Include internal links where relevant.
* Always put the front matter `description` value in double quotes: `description: "Your description here."` Unquoted values that contain a colon (e.g. "focus on what matters: comprehension") break YAML parsing and cause Hugo to fail.
* NEVER put double quotes around the `url` or `slug` values in front matter. Write them bare: `url: /blog/2026/04/22/my-slug` and `slug: my-slug`. Quoted forms like `url: "/blog/..."` or `slug: "my-slug"` are forbidden.
* ALWAYS include a `cover.image` attribute in front matter. The value must be bare (no double quotes), match the `slug` exactly, and end in `.png`. Example:

  ```yaml
  cover:
      image: how-long-should-a-function-be.png
  ```

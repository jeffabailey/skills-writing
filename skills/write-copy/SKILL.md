---
name: write-copy
description: Writes marketing copy grounded in the product's own facts, for landing pages, sales pages, CTAs, button labels, short emails, ads, and taglines. Reads the README, site, or brief first, never invents proof or urgency, and delivers paste-ready copy plus a separate strategy appendix. Use when the user says /write:copy or /write:landing-page-copy, needs landing page copy, wants marketing text, sales copy, conversion copy, a call to action, a launch email, ad text, or a tagline. Triggers on "landing page", "landing page copy", "marketing copy", "sales copy", "conversion copy", "copywriting", "CTA", "call to action", "button label", "tagline", "ad copy", "promo email".
---

# Marketing Copy

Also invoked as `/write:landing-page-copy` (that skill was merged into this one).

Copy persuades only if readers believe it, and one invented testimonial or fake deadline costs that belief. So this skill gets the facts first, writes only from them, and lists what is missing instead of filling the gap.

## Prompts

| Prompt | Use for | File |
|--------|---------|------|
| Landing page | Landing, sales, or product pages: headline, hook, body sections, CTA. Uses ideas from the "48 Laws of Power" behind the scenes | `references/landing-page-copy.md` |
| Short copy | Button label, CTA line, headline, tagline, email, ad, social post | `references/short-copy.md` |

Pick by format. A request for a button and an email is short copy even if it says "CTA"; do not run the landing-page prompt for it. If the user wants both a page and a short piece, run each prompt.

## Workflow

1. **Collect the facts** -- Before drafting anything, read the fact sources: the README, docs, or site pages the user names; otherwise the repo in the working directory (README, package or plugin manifest, LICENSE) or the user's brief. Write a short fact sheet: product, what it does, price or license, audience, the exact action (install command, URL, signup step), and any real proof (quotes the user supplied, published numbers) or real limits (dates, seat caps). Each item notes where it came from. Copy may state only what is on this sheet or in the user's message.

2. **Fill the prompt fields** -- The prompts use bare `{{field}}` placeholders. Pre-fill each from the fact sheet and the request, then apply these defaults:

   | Field | Default when not given |
   |-------|-----------------------|
   | `price_point` | from the license or site; else `[NEEDS FACT: price]` |
   | `competitor_analysis`, `social_proof`, `urgency_factor` | `none` |
   | `brand_voice` | plain and direct, matching the source's tone |
   | `research` | `no` |
   | `length_limit` (short copy) | `default` (limits are in the prompt) |
   | `format` (short copy) | what the user asked for |

   Ask once, in a single message, only for what you cannot find or infer, usually the audience or the action. Accept "none", "unknown", or "skip" for anything. Never block on proof, price, or urgency: missing facts become `[NEEDS FACT: ...]` markers and go on the needs list.

3. **Draft** -- Follow the prompt with the filled values. Research (web search, competitor pages, reviews) stays off unless the user asks for it and web tools are available; when on, every researched claim gets a link in the appendix. The persona in the landing-page appendix is a writing aid and is labeled that way.

4. **Remove AI tells** -- Run the `ai-sanitize` skill (`jbb-skills:ai-sanitize` when installed as a plugin, from [jeffabailey/skills](https://github.com/jeffabailey/skills)) in edit mode on the paste-ready copy only. Persuasive copy collects tells: "elevate", "seamless", "supercharge", "The future of...", contrast framing, triads, eyebrow labels, emoji. Replace each with a claim from the fact sheet; if none fits, delete it or flag it, never invent one. If ai-sanitize is not installed, say so in the delivery note and rely on step 5.

5. **Check before delivery** -- Save the copy to a file and run:

   ```bash
   python3 <skill-dir>/scripts/check_copy.py copy.md --source README.md [--limit Body=80w] [--limit Button=5w]
   ```

   It checks only the paste-ready part (text before the "Needs from you" or appendix heading) for emdashes, law names, buzzwords, scarcity phrases, testimonial-like quotes, numbers not found in the sources, and per-part lengths. Fix every flag, or explain in the delivery note why a flag is a false positive (for example, a number the user gave in chat). Pass the user's limits with `--limit`; without them, use the short-copy defaults.

6. **Deliver** -- Three parts, in this order:
   - **Paste-ready copy**: only what goes on the page or in the email. No law names, technique labels, editor notes, or brackets other than `[NEEDS FACT: ...]`. For a landing page that becomes a page on jeffbaileyblog, set front matter per `hugo/content/prompts/seo-front-matter.md` in the blog repo.
   - **Needs from you**: a checklist of every `[NEEDS FACT]` plus proof worth collecting (testimonials, usage numbers, screenshots). Write "none" if empty.
   - **Strategy appendix** (landing page only; one or two lines for short copy): approach, persona, laws used and where, proof and urgency plans, sources.

## Voice

Plain and specific. Use the product's own terms and the exact command or URL from the source. Use "we" when the source speaks as a company and "you" for the reader. No emdashes. Keep profanity or slang the user's own material uses; do not add any.

## Reference

Copy prompts are also published at https://jeffbailey.us/prompts/; the files in `references/` are the source of truth for this skill.

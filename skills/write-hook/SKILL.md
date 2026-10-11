---
name: write-hook
description: Writes 50 social media post hooks for a piece of text (an article, draft, blog post, or pasted notes), in five groups of ten (funny with pop-culture and tech references, reflective/philosophical, clean/general, edgy/sharp, edgy with pop-culture references), each followed by a one-line action telling the reader what they'll do in the post, plus 12-20 hashtags on one paste-ready line for X, LinkedIn, and Threads. Use when the user says /write:hook, wants hooks, opening lines, scroll-stoppers, or teaser lines to promote an article or post, asks "how should I open this LinkedIn/X/Threads post?", wants social copy or hashtags for a jeffbaileyblog post, or pastes text after a dashed separator line asking for hooks. With no text given, uses the last article created or changed.
---

# Social media hooks

A hook is the headline of a social post, and it deserves as much care as the post. It has one job: make the right reader stop scrolling and want the rest. It does that by promising, as specifically as it can, what the post delivers, and by opening a curiosity gap: enough to make the reader curious, not enough to satisfy them. It fails in two directions. A vague hook could sit on top of any post ("Some thoughts on file search"). A hyped hook promises more than the post delivers ("You won't believe what fd does"), and readers learn to distrust everything after it.

The author's original prompt is in `references/hook-prompt.md`. The writing principles behind this workflow, from Ann Handley's *Everybody Writes*, are in `references/everybody-writes.md`; read it when a group isn't working and you need more than the summary here.

## Usage

```text
/write:hook [file | URL | pasted text]
```

Text after a `---` line in the user's message is the source. A file path or URL is read. With nothing given, use the article you created or edited most recently in this conversation, else run `../write-review/scripts/last-article.sh` (it prints the newest changed jeffbaileyblog article), and name the article you picked.

## Workflow

1. **Read the source as its reader would.** Swap places with the person scrolling past: what do they already believe, what problem do they have, and why would this post be worth a minute of their day? Then note, for yourself and not the output:
   * the core claim, in one sentence;
   * the tension or surprise in it (what a reasonable reader believes that the post corrects);
   * two to five concrete details: a real number, a named tool, a striking line, a mistake, a before and after;
   * who it's for and what they can do after reading it.

   Every hook draws on this list. For a Hugo article, skip front matter and shortcodes; the title and description show the angle the author already chose.

2. **Draft more than you need.** Write about 15 candidates per group, then keep the best 10. The first idea is the obvious one, and everyone else's first idea is the same. Humor especially comes on the rewrite: the funny hook is rarely the first frame you think of but the unexpected one (the snow on the floor that turns out to be Parmesan). The groups:

   | # | Group | What it's for |
   |---|---|---|
   | 1 | Funny: pop-culture and tech-culture references | Dry, direct humor. Movies, TV, games, memes, and tech culture (outages, standups, "it works on my machine", AI hype, YAML, Jira). |
   | 2 | Reflective / philosophical | Calm and introspective: meaning, trade-offs, what the idea says about how people work or think. |
   | 3 | Clean / general | Broad appeal, no insider references, safe for any feed. Curiosity first. |
   | 4 | Edgy / sharp | Blunt, wry, a little uncomfortable. Says what people think but don't post. |
   | 5 | Edgy with pop-culture references | Group 4's bite with one well-chosen reference. Use the reference to make the point land, not as decoration. |

   Within a group, vary the device: paradox, bold statement, existential question, metaphor or mental model, sharp observation, reframing of a common belief, a number that sets expectations. Ten hooks that are all questions read as one hook ten times.

   Across all 50, use each pop-culture reference and each joke once. Two Star Wars hooks, or the same punchline in groups 1 and 5, make the list read as 40 hooks padded to 50. The cut candidates from this step are scratch; don't deliver them.

   Hooks are platform-neutral: the same line works on X, LinkedIn, and Threads. Write per-platform variants only when the user asks for them.

3. **Shape each hook.** These are what separate a hook that stops the scroll from one that blends in:
   * **Lead with the important words.** The first three to five words decide whether anyone reads the rest, so the subject and the action go first. Cut warm-ups: "I think", "In my opinion", "It is important to", "There is a", "According to", "Here's why".
   * **Put the reader in it.** "7 kinds of pumpkins" is about pumpkins; "7 pumpkins you can grow on a city balcony" is about the reader. Name their situation or what they get.
   * **Be concrete.** A real number, tool, or detail from step 1 beats an adjective. Use lively words ("surprising", "ridiculous", "brutal") only when they're true for this audience.
   * **Familiar yet surprising comparisons.** A metaphor or pop-culture reference should use something the audience knows, in a way they haven't seen. "As big as a football field" is familiar and dead; "pumpkins the size of beer kegs" is familiar and alive.
   * **Keep it short.** Aim for 120 characters or fewer so it survives truncation and leaves room for a link; the strongest are usually under 70. Then say it again in fewer words.
   * **Share or solve, don't pitch.** A hook earns attention with an idea, not a sales line ("Order today", "Link in bio", "Sign up now").
   * **Don't preach.** Starting with "Don't forget", "Remember to", "Always", or "You need to" sounds like a lecture. Edgy hooks can be blunt about an idea without wagging a finger at the reader.

4. **Write the action line** under each hook, after a blank line and with no label. It answers the reader's "so what?" by telling them what they'll do in the post, in the imperative, one sentence of 30 words or fewer: "Line up six find commands next to their shorter fd equivalents", not "Lines up six find commands..." or "This post compares...". The hook makes them curious; the action line shows them the payoff is something they get to do. Good content is useful, inspiring, and written with empathy for the reader's problem; the action line shows the useful part. Make it specific to the source ("Search only your own code by letting fd skip everything in .gitignore"), not generic ("Learn a helpful tool").

   Start with a concrete verb the reader would do: line up, swap, search, compare, delete, rename, ask, try, measure, spot. Skip "learn", "discover", "explore", and "find out", which promise a feeling instead of a task.

5. **Pick the hashtags.** Hashtags work by joining conversations people are already having, so use tags people already search and follow, not ones you coin. Pick 12-20, mixed: a few high-traffic broad tags for reach (#SoftwareEngineering, #AI, #Leadership), mid-traffic niche tags for the actual topic (#DevOps, #CommandLine, #TechnicalDebt), and thought-leader / philosophy / self-agency tags for audience quality (#SystemsThinking, #CriticalThinking, #Agency). Use CamelCase so they read well and screen readers can split them. Skip spam tags (#motivation, #success, #hustle, #viral) unless the post is literally about them.

   Order the line best first. A single post should carry only two or three hashtags (more reads as noise), so the 12-20 are a pool to rotate across posts and platforms. Under the pool line, add one line naming the best two or three for a single post (see the output format).

6. **Remove AI tells.** Run the `ai-sanitize` skill (`jbb-skills:ai-sanitize` when installed as a plugin, from [jeffabailey/skills](https://github.com/jeffabailey/skills)) in edit mode on the draft, prose reference only. A batch of 50 hooks is where generated cadence piles up, and readers on X and LinkedIn have learned to scroll past it. Hooks are built from devices ai-sanitize normally flags, so apply its two tests (removal and reason) per hook with these calibrations:

   * **Contrast** ("It's not X. It's Y.", "X isn't just Y"): keep it only when real readers actually believe X. At most two contrast hooks per group; rewrite the rest to state Y directly.
   * **Questions:** a hook may be a question if the post answers it and the reader can't answer it yet. Cut questions the hook answers itself, and engagement bait ("What's your take?", "Agree?").
   * **Fragments:** one short, punchy fragment is a hook's right. A hook made of three fragments ("Fast. Simple. Done.") is a triad tell; rewrite it as a sentence.
   * **Performed insight:** cut "quiet truth", "the real lesson", "changes everything", "silent revolution", "this is where it gets interesting". Replace with the claim from step 1, or drop the hook and write a new one.
   * **Action lines** are plain prose: no signposting, no hype words, no melodrama. Say what the reader does.

   Keep the author's profanity, humor, and strong opinions; ai-sanitize does the same. If ai-sanitize isn't installed, say so in one line and rely on these calibrations plus the checker in step 7.

7. **Check, then deliver.** Write the draft to a scratch file and run:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/check_hooks.py" <draft.md>
   ```

   It checks the shape (5 groups x 10 hooks, an action line on each, in the imperative, 12-20 hashtags on one line, a 2-3 tag pick drawn from the pool), length, warm-up and preachy openers, sales lines, emdashes and en dashes, cliches and business jargon, AI tells, contrast overuse, duplicates, and spam tags. Fix every flag, rerun until it prints `PASS`, then paste the draft into your reply. A cliche flag is almost always right; if a flagged phrase is genuinely the post's subject (a post about hustle culture can say "hustle"), keep it and say why in one line.

## Rules that keep hooks honest

- **Tell the truth.** A hook may exaggerate tone, never facts. Claims about the subject (what the tool does, what the post argues, any number) come from the source. Pop-culture references and well-known public facts can come from outside it, as long as they're accurate. Don't promise something the post doesn't deliver, call something surprising that isn't, invent statistics, or put words in a real person's mouth. A pop-culture reference can allude ("This is the Jurassic Park of config files"); it can't quote a line you aren't sure is real. Hype wins one click and costs the next ten.
- **No emdashes or en dashes anywhere**, in hooks, action lines, or hashtags. Use a period, comma, colon, or parentheses.
- **No cliches, platitudes, or engagement bait**: "Let that sink in", "Read that again", "Nobody talks about this", "Here's the thing", "unlock your potential", "game-changer", "the secret to", "move the needle", "at the end of the day", "low-hanging fruit". A cliche was once a fresh image; now it tells the reader nobody thought hard about this. Edgy means a sharp point, not a cheap trick.
- **Edgy has limits.** Punch at ideas, habits, tools, and institutions, not at groups of people. Profanity is fine when the source uses it or it's the author's voice (jeffbaileyblog posts do); don't add it to a source that has none.
- **Trust the author's voice: direct and dry.** "Your signature directness" in the prompt means that: say the thing plainly and let the wit come from the observation, not from exclamation points or emoji. A clear idea in an authentic voice is what stands out in a noisy feed.

## Output format

Use this template exactly; `check_hooks.py` parses it.

```markdown
**Source:** <title or file, and how you found it>

## 1. Funny: pop-culture and tech-culture references

1. <hook>

   <action line: what the reader does in the post, imperative>
2. ...

## 2. Reflective / philosophical

1. <hook>

   <action line>

## 3. Clean / general

## 4. Edgy / sharp

## 5. Edgy with pop-culture references

### 🔖 Suggested High-Traffic Hashtags

#Tag1 #Tag2 #Tag3 ...

Best for one post: #Tag1 #Tag2 #Tag3
```

Number hooks 1-10 inside each group. Indent each action line three spaces under its hook, with a blank line between them, so it renders as part of the same list item. Don't add a preamble beyond the Source line or a closing summary; the user is going to copy from this.

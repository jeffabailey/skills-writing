---
name: write-review-practice
description: Reviews interactive training material (a practice playground's Markdown exercises, practice files, messages, and the JavaScript that runs the session) together with the article or other content it teaches, using the Four-Component Instructional Design (4C/ID) model plus cognitive load, feedback, retrieval-practice, and constructive-alignment checks. It reports ranked, evidence-backed changes that would make readers learn more, and checks that the practice and the article teach the same thing. It never edits; afterwards it offers to apply the changes the user approves. Built for jeffbaileyblog Learn X articles and their hugo/static/playgrounds bundles, and works on other courses, workshops, or labs. Use when the user says /write:review-practice, asks to review a playground, practice, drill, exercises, or interactive lesson, asks whether the practice matches the article, how to make a training session more effective, or for a 4C/ID or instructional design review, even if they don't say "4C/ID".
metadata:
  version: "1.0.0"
---

# Review practice material

A Learn X article explains, and its playground is where the reader practices. The pair works only if the reader can do, at the end of the practice, what the article promised. This skill reviews both as one instructional design and reports what to change so the reader learns more. It names what to change, where the change lands, and what it costs.

**A review never edits.** Every file must be byte-identical before and after. Recommendations go in the report as proposed text or code sketches. Applying them is the follow-up in step 7, and only with the user's approval.

## Usage

```text
/write:review-practice [playground | article] [source content...]
```

* A playground name (`sql`), its folder, or the article's `index.md`. Given one, find the other (step 1).
* `source content`: optional extra material the practice must also align with (another blog post, notes, a talk outline, a course syllabus). The article stays the main source. Extra content adds outcomes to check, and it never replaces the article.

## Workflow

### 1. Resolve the pair

From the site repo (`~/Projects/websites/jeffbaileyblog`, or `$BLOG_ROOT`):

* **Given a playground:** `grep -rl '{{< playground "<name>"' hugo/content` finds the article. If no article embeds it, review the playground alone and note that it has no source to align with, unless the user gave source content.
* **Given an article:** its `{{< playground "<name>" >}}` shortcode names the bundle.
* **Given neither:** use the playground or article changed most recently in this conversation, else the newest commit touching `hugo/static/playgrounds/`. Say which one you picked and why.
* **Not jeffbaileyblog:** the same review applies to any training material plus the code that runs it (a workshop repo, notebooks with autograders, a lab script). Find the equivalents of tasks, feedback text, orchestration, and source content. Say which file plays which role, and skip the site-specific constraints you can't confirm.

State both absolute paths and whether the article is `draft: true`.

### 2. Map it

```bash
python3 <this-skill>/scripts/practice_map.py <article index.md> [playground dir]
```

The map lists the article's outline and anchors, its stated outcomes (What You'll Learn), its code blocks (and which run only on the reader's machine), the playground's files and message keys, the exercises (when an `exercises.md` exists), broken exercise links, and core sections with no exercise. Treat it as evidence to check, not a list of findings. A core section with no exercise is sometimes right.

### 3. Read for the learner's path

Read `references/playground-anatomy.md`, then read the material in this order:

1. The bundle's `AGENTS.md`. Its rules and deviations register decide which recommendations are allowed. Read it before you form opinions.
2. The article in full, plus any source content. List its outcomes and its mental models (the *why* sections), its procedures (the *how* steps), and its strategies.
3. The practice files and `messages.json`.
4. `playground.js`, read for behavior. Trace one session the way a reader would live it: what is on screen after Start, what the first task asks, what a wrong attempt shows, when a hint or answer appears, what Reset restores, and where the session ends. Note line numbers as you go. You are reviewing the instruction the code delivers, not the code's style or structure.

When something in the code is unclear, check the bundle's tests (named in `AGENTS.md`) before you guess. A recommendation built on a misread of the orchestration is the costliest error this review can make.

### 4. Analyze

Do these three passes. Each finding needs evidence (`file:line`, or a quoted message) and the principle behind it.

1. **4C/ID**, using `references/4cid.md`: learning tasks, supportive information, procedural information, and part-task practice. First sort the topic's skills into recurrent and non-recurrent, because that decides what each component should look like.
2. **Alignment** between the article (and source content) and the practice, using constructive alignment and Merrill from `references/companion-frameworks.md`:
   * For each stated outcome, which task practices it and which check assesses it? Build the outcome table for the report.
   * For each task, which section supports it, and does the link land there?
   * Do the names, data, versions, and terms match on both sides?
   * Does the practice hand off to the article's "Build Something" or own-machine steps (integration)?
3. **Companion lenses** (cognitive load, retrieval and spacing, feedback) from `companion-frameworks.md`, only for findings the first two passes didn't produce.

Then check every recommendation against the constraints in `playground-anatomy.md`. Rewrite or drop any that would simulate the program, invent an expected value, or change the deviations register on its own authority. Moving a recommendation into the "Owner decisions" section is a legitimate outcome. Don't treat it as a failure.

### 5. Rank

Rank by learner impact first and cost second. Impact means how many readers it affects, and how much it changes what they can do afterwards. A broken first task beats an imperfect seventh one. A misaligned outcome beats a wordy hint. Mark the top three to five findings as the ones to do first. A long list nobody acts on helps no one. Keep the rest short.

### 6. Report

Use this structure. Show it in the conversation, and write it to a file only when the user or a caller names a path.

```markdown
# Practice review: <Name>

**Article:** <path> (draft: <true|false>) · **Playground:** <path> · **Other sources:** <paths or none>
**Skills taught:** recurrent: <...>; non-recurrent: <...>

## Verdict
<Two or three sentences: does the practice let a reader do what the article promises? What is the biggest gap?>

## Scores
| Component | Score | Why (one line) |
|---|---|---|
| Learning tasks | n/10 | |
| Supportive information | n/10 | |
| Procedural information | n/10 | |
| Part-task practice | n/10 or N/A | |
| Article ↔ practice alignment | n/10 | |

## Outcome alignment
| Outcome (What You'll Learn / 20% section) | Practiced by | Checked by | Gap |
|---|---|---|---|

## Do these first
### 1. <Short imperative title>
- **Evidence:** <file:line, quoted text>
- **Principle:** <4C/ID component or named effect>
- **Why it matters:** <the learner's experience now, and after the change>
- **Change:** <proposed text, task, or code sketch, concrete enough to apply>
- **Lands in:** <messages.json | practice/… | article | playground.js | shared/>  · **Cost:** <low | medium | high: oracle run, tests to rerun>

## More findings
<Same fields, one compact bullet each, ranked.>

## Owner decisions
<Findings that need a register row, a D-rule change, a shared-helper change, or a scope call. Say what to decide and the trade-off. Never apply these.>

## What works
<Two to four specific strengths to keep, so an edit doesn't remove them.>
```

Write each change in the site's voice: plain words, second person, imperative. Proposed article text follows `../write-article/references/learn.md`. Proposed exercise entries copy the bundle's own `exercises.md` format exactly. Any expected output that a new task needs is marked *to be produced by the oracle*. Don't write it from memory.

### 7. Offer to apply

End with one question: which numbered findings should be applied? List the low-cost ones first. Then wait.

When the user approves findings:

* Apply only those findings. Back up each file before editing it (`cp file file.bak-<date>`), and edit in place.
* Article edits follow the `hugo-agents-compliance` rules. `messages.json` must stay valid JSON, and its keys stay unchanged unless `playground.js` changes with them.
* New expected values come from the bundle's oracle (`AGENTS.md`, "The oracle"). If the oracle can't run here (no Docker), apply the change, then tell the user it is unverified and which command verifies it.
* Run the tests `AGENTS.md` names for every file you touched, and report pass or fail with the output. A change that fails its suite isn't done.
* Never apply an Owner decision.
* Then rerun step 2 and show the before and after scores for the components the changes touched.

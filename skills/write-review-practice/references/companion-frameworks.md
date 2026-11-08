# Companion frameworks

4C/ID is the main lens. Use these to check alignment, and to find what 4C/ID names but doesn't spell out. Cite one only when it produces a finding the four components didn't. Name the principle in the finding so the author can look it up, and don't lecture.

## Constructive alignment (Biggs)

The intended outcomes, the learning activities, and the assessment should all point at the same thing. Here those are, in order: the article's **What You'll Learn** questions and 20% sections, the playground's **tasks**, and the playground's **checks** ("correct" and "not yet", or a retrieval check). This is the alignment pass in the main workflow.

- Every stated outcome should have at least one practice task, or a stated reason it has none (for example, "where can you go to learn more" needs no task).
- Every task should trace to an outcome. A task with no outcome is either a missing section or scope creep.
- What a task checks should match what the outcome claims. If the outcome is "build a prompt that makes the model cite its sources" and the check only looks at row order, the assessment measures something else.
- Use the same names on both sides: data files, table names, versions, and terms. When the article says `parcel.db` and the playground says `shop.db`, the reader has to work out which one is which.

## Backward design (Wiggins & McTighe)

Start from the result, decide what evidence would show it, then plan the activities. Ask: if a reader finished every task, what could they do that they couldn't before? If the answer is smaller than the article's promise, the practice is under-built. If it's larger, the article under-explains. The site's own rubric is `../../write-article/references/backward-design.md`.

## Merrill's First Principles of Instruction

Learning is promoted when it is **problem-centered** and the reader moves through **activation** (recall what they know), **demonstration** (see it done), **application** (do it with feedback), and **integration** (use it in their own work). For a Learn X pair:

- Activation: the article's hook and Basics.
- Demonstration: the 20% sections, with worked commands and expected output.
- Application: the playground.
- Integration: "Build Something" and "Make it yours". Check that the playground hands off to it, so the reader knows what to run on their own machine next.

A missing phase is a finding. The most common gap is a playground with no bridge to integration.

## Cognitive load theory (Sweller)

Working memory is small. Intrinsic load comes from the task itself. Extraneous load comes from how the material is presented. Cut extraneous load so capacity goes to the task. The effects worth checking in a playground:

- **Split attention.** The reader has to hold the article in one place and the playground in another (scroll up to read the task, scroll down to type). Is the task text inside the playground, next to where the reader types?
- **Redundancy.** The same explanation appears three times (in the article, the intro line, and the hint). Redundant text costs attention.
- **Worked example effect.** Novices learn more from studying worked examples than from solving problems on their own. Check that a worked example, or a shown answer, comes before the first conventional task in each class.
- **Expertise reversal.** Help that serves a novice gets in an expert's way. The fix is support that fades, or that appears on demand.
- **Element interactivity.** A task that needs five new ideas at once overloads the reader. Can it be split, or preceded by a simpler one?
- **Transient information.** Output that scrolls away, or a message that flashes and disappears, is gone before the reader has read it. Check how long feedback stays on screen.

## Retrieval, spacing, interleaving (desirable difficulties, Bjork)

- **Retrieval practice.** Recalling an answer strengthens memory more than re-reading it. A "Show answer" one click away invites re-reading. A hint first, then the answer, invites retrieval.
- **Spacing.** Later tasks should bring back earlier skills.
- **Interleaving.** Mixing task types makes the reader choose the method, which is the skill that transfers. A playground grouped strictly by section never asks "which tool fits here?" A final mixed task class can.
- **Generation.** Asking the reader to predict the output before running ("how many chunks will this make?") turns watching into thinking. This fits stage-by-stage playgrounds (RAG) especially well.

## Feedback (Hattie & Timperley; Shute)

Good feedback answers three questions. Where am I going (the goal)? How am I going (the gap)? Where to next (the next step)? Check each message in `messages.json`, and each correct or not-yet state, against these three. Prefer feedback that is:

- specific about the gap ("the right rows, in the wrong order", not "not yet"),
- about the task or the process, not the person,
- immediate for recurrent skills, and allowed to wait a little (until the reader asks) for non-recurrent ones,
- not a giveaway. Feedback that reveals the answer ends the retrieval practice.

## Gagné, Bloom, 5E

The site's `../../write-article/references/lesson-planning.md` covers Gagné's nine events, Bloom's revised taxonomy, and 5E. Use Bloom's taxonomy only to check one thing: whether the tasks reach the level the outcomes claim. "Explain when RAG is the right tool" sits at analyze and evaluate. If every task is at the apply level, say so.

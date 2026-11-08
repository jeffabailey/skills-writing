# 4C/ID applied to an article and its practice

The Four-Component Instructional Design model (van Merriënboer; *Ten Steps to Complex Learning*, van Merriënboer & Kirschner) treats learning a complex skill as learning to do **whole tasks**, with three kinds of help around them. It fits a Learn X article and playground well. The playground is where the learning tasks happen. The article supplies the supportive and procedural information. Drills cover the part-task practice.

Use the four components to sort what you find, then score each one. Every question below is something to check against the files, not something to recite in the report.

## Contents

1. [Learning tasks](#1-learning-tasks)
2. [Supportive information](#2-supportive-information)
3. [Procedural information](#3-procedural-information)
4. [Part-task practice](#4-part-task-practice)
5. [Recurrent vs non-recurrent skills](#recurrent-vs-non-recurrent-skills)
6. [Scoring](#scoring)

## 1. Learning tasks

A learning task is a whole, real piece of work: "list the customers who never ordered", "find out why retrieval missed the runbook". It is not "use LEFT JOIN". Whole tasks make the reader combine skills the way real work does, so what they learn transfers.

Check:

- **Whole, authentic tasks.** Does each task have a goal a practitioner would have? A task that names the construct to use ("use `select`") is part-task practice dressed up as a learning task. Prefer wording by goal ("Find the Engineering staff who earn more than 120000").
- **Task classes, simple to complex.** Tasks should come in groups of equal difficulty, ordered from the simplest version of the whole task to the hardest. Within a class, support starts high and fades. Look for a jump in difficulty with no ramp, or several tasks of the same difficulty in a row while the support stays the same.
- **Variability of practice.** Within a class, tasks should differ along the dimensions that differ in real work (data shape, failure mode, size, context), so the reader learns what stays the same. Ten tasks on one six-row table vary less than the job does. Flag sameness when it hides a real-world dimension the article itself names, such as NULLs, empty results, or a doc with no headings.
- **Support and guidance fading (the completion strategy).** The usual order is a worked example (a demonstration with the answer shown), then a completion task (partly done: a starting command that runs but doesn't do the task yet), then a conventional task (the reader starts blank). Check whether the playground moves along that order or stays at one level. Starting commands that "run but don't do the task yet" are completion tasks. Hint and Show answer are support on demand. Ask whether that support shrinks as the reader moves on. If every task has a starting query that already names the right table, it doesn't.
- **A task the reader can finish and check.** The reader must be able to tell they're done. Does the page say "correct" or "not yet", and why? Is there a visible end state? Open-ended sandboxes (an editor, a shell with sample files) need a stated goal for each try, or readers poke around and leave.
- **The first task is reachable.** After Start, can the reader succeed within the first minute without reading anything else? Read `playground.js` to see what is on screen before any input, and what the first task asks.

## 2. Supportive information

Supportive information is the theory behind the non-recurrent parts of the skill: mental models (how BM25 scores a chunk, why NULL never equals NULL), cognitive strategies (how to approach a slow query), and feedback on the quality of a solution. It belongs **before** a task class and stays available while the reader works.

Check:

- **A mental model for every task class.** Each group of exercises should trace to an article section that explains *why*, not only *what to type*. A task with no section behind it asks the reader to guess. A section with no task is theory with no practice (see the alignment pass).
- **Cognitive strategies.** Does the article give a way to approach the problem ("read a query in execution order", "check retrieval before you blame the model")? Strategies are what transfer. When the article has one, a task should exercise it.
- **Reachable from the task.** Can the reader get from a task back to the explanation in one click (an exercise `link:` to the right anchor) and back again? A broken or missing link cuts the supportive information off from the task.
- **Feedback on the approach, not only the result.** A "not yet" that names what is wrong ("the rows are right but not in order") is cognitive feedback. A bare "wrong" is not.

## 3. Procedural information

Procedural information is the how-to for the recurrent parts: exact syntax, the key to press, the flag. It belongs **just in time**, at the step where it's needed, and fades as the reader stops needing it.

Check:

- **At the point of need.** Is the syntax for this task on screen or one click away when the reader needs it (a hint, a placeholder, a keys bar), rather than three sections back in the article?
- **Not in the way.** Procedural help that is always shown, after the reader has it down, is extraneous load (see the expertise reversal effect in `companion-frameworks.md`). Hints on demand beat hints always visible.
- **Error messages as procedural information.** When the reader makes a known mistake, does the page say how to fix it? `messages.json` holds that wording, and it is the best place to coach. Read each message as a learner who has just failed. Does it say what happened and what to do next?
- **The machine and browser boundary.** Commands that only work on the reader's machine (`{practice="machine"}` fences) are procedural information for a different place. Check that the reader can tell which commands work where, and that the page's response to a machine-only command teaches rather than scolds.

## 4. Part-task practice

Part-task practice drills a recurrent skill until it is automatic (motions in an editor, `jq` paths, joining two tables). Use it only where automaticity matters, and only after the reader has seen the skill inside a whole task.

Check:

- **Is there a recurrent skill that needs automaticity?** Editor motions, shell keys, and common filters do. Concepts like "when to use RAG" don't. Recommend drills only for the former.
- **Spaced and interleaved.** A drill that repeats one move in a block feels good but sticks less than one mixed with earlier moves (see `companion-frameworks.md`). Check whether later tasks reuse earlier skills.
- **Drills placed after the whole task, not before.** If the playground opens with ten drills before any real task, the reader practices parts with no picture of the whole.

## Recurrent vs non-recurrent skills

Sort the topic's skills before you score. **Recurrent** skills are done the same way every time (syntax, keys), and they need procedural information and maybe part-task practice. **Non-recurrent** skills need judgment (choosing a chunk size, reading a plan, deciding why retrieval missed), and they need supportive information and varied whole tasks. A common failure is to teach a non-recurrent skill as if it were recurrent: one fixed recipe and one fixed practice task, so the reader can repeat it but can't adapt it.

## Scoring

Score each component from 1 to 10 against the questions above, and write one line on why.

| Score | Meaning |
|---|---|
| 9–10 | The component works. Only polish findings. |
| 7–8 | Works, with one or two gaps a learner would feel. |
| 5–6 | Present but weak. Readers practice without the help this component should give. |
| 3–4 | Mostly missing. Learning depends on the reader filling the gap alone. |
| 1–2 | Absent, or working against learning. |

Score part-task practice **N/A** when the topic has no recurrent skill that needs automaticity, and leave it out of the average. Don't give a low score to the absence of something the topic doesn't need.

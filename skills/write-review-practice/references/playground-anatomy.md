# Where the instruction lives in a jeffbaileyblog playground

The site repo is `~/Projects/websites/jeffbaileyblog`. Playgrounds live in `hugo/static/playgrounds/<name>/`, and articles in `hugo/content/blog/learn-x/learn-<name>/index.md`. The article embeds its playground with `{{< playground "<name>" >}}`, usually under a `## Practice <Name>` heading. `create-practice-playground`'s `references/article-integration.md` lists what that section holds.

Don't trust this file over the repo. Bundles differ. Read the bundle's own `AGENTS.md` first.

## Files that carry instruction

| File | What it holds for the learner | Read it for |
|---|---|---|
| `practice/exercises.md` (sql, jq) | Numbered **tasks** in groups named after article sections. Each one has a starting command (a completion task), and may have `hint:`, `answer:`, `link:` (an anchor back into the article), and `order:` (the check needs sorted rows). | Learning tasks, fading, variability, links to supportive information. |
| `practice/*.md`, `*.json`, `*.csv`, `*.sql` (others) | The **practice world**: the file the program opens (neovim `practice.md` is itself the exercise sheet), sample data, the docs being indexed (rag). | Whether the data is varied enough to make the tasks realistic, and whether it matches the article's examples. |
| `messages.json` | Every message the page shows the reader: ready, errors, `correct` and `not_yet_*` feedback, notes for things the browser can't do. | Feedback quality and procedural information at the point of need. This is the cheapest place to make a change. |
| `playground.js` | The **orchestration**: what appears after Start, the order of stages or tasks, how a task is checked, when hints and answers show, what Reset restores, what a run sends to the program, and which message comes back. | The learner's actual path through the session. Read it for behavior, not code quality. `review-maintainability` covers code quality. |
| `playground.css` | Layout: whether the task text sits next to the input, and what is hidden by default. | Split attention and transient information. |
| `AGENTS.md` | The bundle's **rules**: D-rules, the oracle, the **deviations register** (every known difference from the desktop program), and the test commands. Hugo doesn't publish it. | Constraints on what you may recommend. Read it before you write a finding. |
| `engine/` | The program's bytes and its build recipe. | Skip it. It isn't instructional. |
| `../shared/*.js` | Helpers every playground uses (`common.js`, `vm.js`). | Only to explain a behavior. A change here affects every playground. |

When there is no `exercises.md`, the tasks live elsewhere. RAG's tasks are its **stages** and its **checks** (`CHECKS` and the default question in `playground.js`), and the article's numbered drill under `## Practice <Name>`. A shell playground's tasks are the article's drill, plus whatever the practice files suggest. Find them before you score learning tasks, and say where you found them.

## Constraints every recommendation must respect

These come from failures in shipped playgrounds. A recommendation that breaks one teaches readers something false or breaks the build, however good the pedagogy.

1. **The real program, never a simulation.** Don't recommend JavaScript that fakes output, ranks, parses, or checks anything the program itself should produce. When feedback needs to know whether an answer is right, the check must run in the program (as SQL's Check does), or be stated as a limitation. "Add a JS validator for the jq answer" is the wrong fix. "Compare the program's output to the oracle-recorded expected output" might be the right one, and it costs a DELIVER step.
2. **Expected values come from the oracle.** Any new task, check, or expected output needs an oracle run. Say so in the finding's cost. Never write an expected output from memory into a recommendation and present it as correct.
3. **The deviations register is the owner's decision.** A finding that would add, change, or remove a register row is tagged **owner decision**. The skill never applies it.
4. **Shared helpers are expensive.** A change to `shared/common.js` or `shared/vm.js` changes every playground's cache key, and every suite has to run again. Prefer a fix inside the bundle, and tag shared changes **high cost**.
5. **Nothing downloads before Start.** Don't recommend preloading the engine to make the first task feel faster.
6. **Article commands keep their split.** Commands the browser can't run stay in `{practice="machine"}` fences. Don't recommend removing the fence to make an article step "practicable".
7. **Article voice and format.** Article edits follow Learn X (`../../write-article/references/learn.md`): second person, imperative, no H1, and the launch pad stays. Don't recommend a change that turns the how-to into a tutorial-length course. Depth belongs in the resources.
8. **Tests replay the article.** Many suites replay the article's drill and blocks against the oracle. Changing a drill step or a code block means running that suite (its command is in `AGENTS.md`, under Tests). Name the suite in the finding.

## Where a fix lands, cheapest first

Tag each recommendation with where it lands. Cost rises down the list:

1. `messages.json` wording
2. `practice/exercises.md`, or the practice data (new task, hint, ordering, links). Needs an oracle run for expected values.
3. The article (drill, intro, a bridge sentence, a heading that an exercise links to)
4. `playground.js` (orchestration: hint gating, task order, start state). Needs the bundle's unit and acceptance tests.
5. `shared/` (every playground)
6. A register row or a D-rule (owner decision, never applied)

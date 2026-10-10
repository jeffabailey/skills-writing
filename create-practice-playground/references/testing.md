# Testing a playground

Copy `tests/acceptance/fd-wasm-playground/` (v86, the newest finalized suite) or the jq suite (wasm) and rename. Mutation testing is off in this repo, so every repaired or new guard gets checked by hand: break the code, watch the test fail, restore.

## Oracle

Expected values come only from the desktop program at the pinned version.

- Containerized (zsh): `tests/acceptance/<f>/oracle/Dockerfile`, multi-stage, building from the engine's own `build-<prog>.sh` with build context `hugo/static/playgrounds/<name>/engine/src`, for **linux/amd64**, so an i386 miscompile shows up as a mismatch.
  `docker build --platform linux/amd64 -t <xx>wp-oracle:local -f tests/acceptance/<f>/oracle/Dockerfile hugo/static/playgrounds/<name>/engine/src`
- Official binary (Nushell): the release binary, sha256-pinned in the workflow, passed as `NU_BIN`.
- Sessions run with `--network none`, `LC_ALL=C.UTF-8`, `TZ=UTC`, an 80x24 pty rendered with pyte, uid 1000, hostname `practice`, and a fresh practice home from the manifest. Use the suite's `oracle.py`, not a hand-made container.
- Match the guest's CPU count: the v86 guest has one CPU, so run the oracle with `--cpuset-cpus=0` when the program sizes its thread pool from the CPU count (fd does).
- The pinned version must agree in three places: `engine/VERSION`, `@@READY <ver>`, and the oracle's reported version.
- `@oracle` scenarios skip without the oracle and fail under `<XX>WP_REQUIRE_ORACLE=1` (CI sets it).

## Article replay

- `tests/common/<name>_article.py`, built on `article_fences.py`, reads every fenced `<lang>` block in article order. Each block is one session; its output is the following `text` block.
- Continuation rules: trailing `\`, open quotes, trailing `|`, `&&`, `||`, open `{` or `(`. A new language may need its own (fish `begin`/`end`, `function`/`end`). Put language-specific rules in `tests/common/<name>_article.py`; a change to the shared `article_fences.py` means re-running every suite that imports it (`grep -rl article_fences tests`).
- Exclusion is the fence attribute `{practice="machine"}`, never an inline `#` comment.
- `MIN_REPLAYABLE = 40`; the extractor refuses an empty list (a vacuous pass hid a bug before) and blocks that start with a history designator (`!`, `^`).
- The reference check compares `<lang>`/`text` pairs against the oracle and writes `deliver/reference-verification.md`.
- The replay re-reads the article on every run: new commands join automatically, and a broken example fails CI.

## Suite mechanics

- `conftest.py` builds with `hugo --destination tmp --baseURL http://127.0.0.1:<port>/`, serves with `python -m http.server`, and drives Playwright (Chromium; one outline in Firefox and WebKit).
- Other origins are refused. In **WebKit** install no routes at all (any route stops `blob:` workers, which v86 runs in); record requests with `context.on("request")`.
- GA4 is a fake queue. The only engine seam is `window.<name>Playground.snapshot()` → `{screen, cursor, grid, scrollback}`. Assert the engine's own grid, not box coverage (coverage assertions passed before resize code existed).
- Failures write `failures/<test>/{page.txt,screen.png}`.
- Use `page.wait_for_timeout` for polling inside Playwright sync code; `time.sleep` never sees popups.
- Hugo: the site's `[[module.mounts]] source = "content"` beats `--contentDir`; for a one-page check site, copy the config dir and point its mount at temp content. `hugo --quiet` prints nothing on failure.
- pytest-bdd 7.3 ignores tags on `Examples:` blocks; tag the whole Scenario Outline. Register every tag in `pytest.ini` (`--strict-markers`); use `# contract-shape:` comments instead of extra tags.
- Use pyenv `python`, not `python3`. Each suite has its own `.venv` (Neovim's needs gherkin; others can share tmux's).

## Environment knobs (`<XX>WP_` prefix)

`RUN_PENDING=1` (run skipped scenarios), `REQUIRE_ORACLE=1`, `READY_TIMEOUT_MS` (CI 60000), `SLOWDOWN` (CI 3; scales waits, never assertions), `FEATURES` (comma list, for sharding), `HEADED`, `FAILURE_DIR`, `REPORT_DIR`, `ORACLE_IMAGE`, and the pinned version.

## Scenario lifecycle

DISTILL tags everything `@pending` and the skeleton `@awaiting_engine`, so the default run exits 0. DELIVER un-skips one scenario per step. A scenario that passes immediately needs a reverted-mutant failure to prove it can fail.

## Typing into the VM

Playwright types faster than an emulated machine reads. Send keys with a 10 ms gap, wait for a quiet screen (150 ms) before typing and after every prefix chord, wait for the next prompt at session transitions, and scale every wait by `SLOWDOWN`. BusyBox ash reads ahead: an Esc sent with Enter is swallowed. Right-trim the cursor row before matching a prompt (zsh's `ESC[K` leaves a trailing space).

Reproduce CI flakes locally with CDP CPU throttling at rate 25 (rate 4 was too gentle; `yes` load doesn't reproduce them) and `SLOWDOWN=3`, three runs in a row. Prove each new wait by breaking it on purpose.

## Prove CI locally first

The user wants builds proven locally, not iterated on GitHub. Before pushing any change to a playground workflow or the files in its `paths:` list:

1. `actionlint .github/workflows/test-<name>-playground.yml` exits 0 with no output.
2. `act workflow_dispatch -W .github/workflows/test-<name>-playground.yml -P ubuntu-24.04=catthehacker/ubuntu:act-24.04` from the repo root ends in `Job succeeded`. Without `-P`, act skips the job and reports nothing, which is not a pass. `~/.actrc` already sets amd64 and `ACT=true`.
3. Make each matrix shard runnable on its own under act (`--matrix shard:<name>` or a workflow input), and run every shard the change touches.

Guard upload-artifact steps with `if: ${{ !env.ACT }}` and read failures from the suite's `failures/` folder. act names containers by workflow and job, so two runs at once collide; check no other session is running the same workflow. The full procedure is in `hugo/static/playgrounds/neovim/AGENTS.md` § "Before committing: run the CI workflow locally". A GitHub run confirms a passing act run; it is not where you debug.

## CI (copy `test-fd-playground.yml`)

- On push and PR, with path filters covering the bundle, `shared/**`, the shortcode, descriptors, the `neovim-playground` hash partial, the standalone layout and page, the article, `tests/common/**`, the suite, and the workflow itself.
- Matrix: a `checks` shard (node unit tests, Python extractor tests, repository checks `-m "cross_cutting and not real_io …"`, with `fetch-depth: 0`) plus acceptance shards split by feature file through `<XX>WP_FEATURES`. Nushell needed 6 shards after one job blew the 40-minute limit.
- The oracle `docker build` runs on acceptance shards; cache Playwright browsers.
- Pytest exit code 5 (no tests collected, everything pending) counts as a pass.
- Upload `report.xml`, `failures/`, `reports/`.
- The CI runner's uid is 1001, not 1000: open the oracle home to any uid.

## Live check

`tests/browser/tests/<name>-playground.spec.ts` (copy Nushell's): press Start, ready text includes the version, type a command, sum transfer bytes from the Performance API. The deploy workflow runs these against https://jeffbailey.us after invalidation, so it stays `test.fixme` until the playground is live.

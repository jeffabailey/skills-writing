# File inventory for a new playground `<name>` (prefix `<xx>wp`)

Copy from the template chosen in SKILL.md Step 2 (fd for v86 by default, zsh only for a shell guest's build and hook; jq or neovim for wasm), then rename. Paths are relative to the jeffbaileyblog root.

## Contents

- Bundle
- Registration (layouts, config, CSS)
- Standalone page and article
- Tests
- CI and docs

## Bundle: `hugo/static/playgrounds/<name>/`

| File | Purpose |
|---|---|
| `playground.js` | Classic script. Pure functions under `internals` (exported for `node --test`) plus a `Playground` class. Exposes `window.<name>Playground = { mount(root, base) → .boot(), snapshot(), internals }`. Constants: PROMPT, MEMORY_MB 128, COLS 80, ROWS 24, STALL 20 s, BOOT_TIMEOUT 20 s, ENGINE_FILES, REASONS. Loads `shared/vm.js` through `playgroundCommon.loadScript`, then calls `vm.unsupported(128)`. |
| `playground.css` | Selectors scoped by the `<xx>wp` prefix. Loaded on Start, so nothing here may size the pre-Start box. |
| `messages.json` | `download_failed`, `unsupported_browser`, `engine_crashed`, `boot_timeout`, plus the note catalog keyed by the daemon's allow-listed `@@MSG` keys. |
| `preview.txt` | The pre-Start preview: prompt, one command, and the oracle's output for it. |
| `practice/` | Seeded practice files plus `manifest.json` (guest path, mode, mtime). Dotfiles are stored without the dot (`zshrc` → `/home/reader/.zshrc`). |
| `AGENTS.md` | The real-program rule, oracle procedure, deviations register, rebuild steps. Copy fd's and rewrite every line for the new program. Not deployed and not hashed. |
| `engine/` | v86 case: `libv86.mjs`, `v86.wasm.gz`, `seabios.bin.gz`, `vgabios.bin.gz`, `xterm.mjs`, `xterm.css` (copied, same pins), `bzImage.gz`, `state.bin.zst`, `VERSION`, `NOTICES.txt`, `src/` (the build recipe). Lazy-disk case adds `disk.json` and one `disk-<md5>/` folder. Wasm case: `*.wasm.gz`, glue, `VERSION`, `NOTICES.txt`, `src/`. |

The shared helpers (`shared/common.js` → `window.playgroundCommon`, `shared/vm.js` → `window.playgroundVm`) already provide download, gunzip, digest check, emulator start, line splitting, control text, announcer, download bar, and the article fit. Use them; a `no-local-copies` unit test forbids redefining them in the host.

## Registration

- **Create** `hugo/layouts/partials/playgrounds/<name>.html`, the descriptor. Copy `fd.html`: prefix, program, noun, size ("about N MB"), version (md5 of bundle + shared bytes via `partials/neovim-playground/bundle-bytes.html`), preview, previewLabel, standalonePreview, fullscreenBeforeStart, baseAttr, and `attrs` (`state-sha256`, plus `disk-*` for a lazy disk).
  The `playground` shortcode learns valid names by listing this directory, so **no shortcode or layout edit is needed**, and a repository check fails if one happens. Never put a non-descriptor file in that directory.
- **Extend** `hugo/config/_default/hugo.toml`: add `"! playgrounds/<name>/AGENTS.md"` to the static mount's `files` list (search for `playgrounds/zsh/AGENTS.md`). Without it, AGENTS.md deploys.
- **Extend** `hugo/assets/css/extended/jeff_custom.css`:
  - add `html.<xx>wp-running #top-link` / `#bottom-link` to the scroll-link hiding list;
  - add an eager `[data-<name>-playground]:not([data-playground-fit]) .<xx>wp-*` sizing block (copy fd's), so pressing Start causes no layout shift.
- **Extend** `hugo/assets/css/extended/playground-controls.css`: add `<xx>wp` to each `:is(...)` list (actions, key bar, preview/no-JS hiding).
- Fence label: `hugo/layouts/_default/_markup/render-codeblock.html` already renders `{practice="machine"}` as "Runs on your machine, not in the practice shell". No change needed.

## Standalone page and article

- **Create** `hugo/content/<name>-practice-<noun>.md` (existing: `fd-practice-shell.md`, `nushell-practice-shell.md`, `zsh-practice-shell.md`, `tmux-practice-terminal.md`, `neovim-practice-editor.md`, `jq-practice.md`). Front matter: `url: /playgrounds/<name>/`, `layout: playground`, `playground: <name>`, `outputs: [HTML]`, `build: {list: never}`, `sitemap: {disable: true}`. Copy the closest one.
- Article (only if the user said Yes): `hugo/content/blog/learn-x/learn-<name>/index.md` plus `learn-<name>.png`. See `article-integration.md`.

## Tests

- `tests/acceptance/<name>-wasm-playground/`: `pytest.ini`, `requirements-test.txt`, `.gitignore` (failures/, reports/, report.xml), `oracle/Dockerfile`, `fixtures/silent-machine.bin.zst`, `steps/{conftest,domain_types,screen,oracle,article_steps,shell_steps,platform_steps,test_<name>_playground}.py`, and feature files `walking-skeleton`, `shared-host-helpers` (only with a shared change), `milestone-1..N-*`, `integration-checkpoints`.
- `tests/unit/<name>-playground/`: `com2`, `events`, `keys`, `messages`, `no-local-copies`, `readiness` `.test.mjs`, `harness.mjs`, and `test_<name>_article.py` (Hypothesis).
- `tests/common/<name>_article.py` on top of `tests/common/article_fences.py`.
- `tests/browser/tests/<name>-playground.spec.ts`: live check, starts as `test.fixme` (copy Nushell's).

Repo-wide ignore rules have swallowed fixtures before (`manifest.json`, `sales.csv`). After creating files, run `git status --ignored` on the new paths and un-ignore what belongs.

## CI and docs

- `.github/workflows/test-<name>-playground.yml` (copy `test-fd-playground.yml`; see `testing.md` § CI).
- `hugo/lat.md/<name>-playground.md`; `lat check` must pass.
- `docs/product/jobs.yaml` (under JOB-PRACTICE-001), `docs/product/kpi-contracts.yaml` (KPI-<XX>WP-n, guardrails G1 to G5).
- `docs/product/architecture/adr-<XX>WP-00n-*.md`, plus the `brief.md` entry and `c4-diagrams.md`.
- `docs/feature/<name>-wasm-playground/`: `feature-delta.md`, `slices/`, `spike/`, `design/upstream-changes.md`, `distill/`, `deliver/{roadmap.json,execution-log.json,reference-verification.md}`.
- At finalize: `docs/evolution/<name>-wasm-playground-evolution.md`.

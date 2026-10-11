---
name: create-practice-playground
description: Builds a new in-browser practice playground for jeffbaileyblog (a real program running in the page, like the fd, Nushell, zsh, tmux, Neovim, and jq playgrounds) by first checking the tool can run in a browser at all, then driving the nWave waves with the recipe, intake questions, and gotchas learned from the shipped playgrounds, and, when the user says Yes, a Learn X article with the playground embedded and its drill replayed by the tests. Use when the user says /write:playground, asks to "add a fish (or any tool) playground", "make a practice shell, terminal, or editor for a tool", "a wasm or v86 practice app like the Nushell one", "let readers try a tool in the browser", or wants a Learn X article with a live practice terminal, even if they don't say "playground".
---

# Create a practice playground

A practice playground runs the **real, unmodified program** in the reader's browser so every command in a Learn X article can be tried on the page. Each took one nWave feature of 9 to 34 DELIVER steps.

**Discover what has shipped; don't trust a count in this file.** List `hugo/static/playgrounds/` (every folder except `shared/`) and `docs/evolution/*-wasm-playground-evolution.md`. A playground with an evolution doc is finalized; one without is still in DELIVER. As of 2026-10-10: `jq` and `neovim` (wasm); `tmux`, `nushell`, `zsh`, and `fd` (Linux on v86, fd finalized 2026-10-08 as a CLI tool inside zsh); zsh had no evolution doc yet. This skill turns that history into a repeatable path, so a new playground starts from the decisions already made instead of rediscovering them.

The site repo is `~/Projects/websites/jeffbaileyblog`. Run every command from its root.

## Ground rules that carry over from every playground

These came from real failures; the reasons matter more than the wording.

- **Real program, never a simulation.** Output that differs from the desktop program teaches the reader something false, which is worse than a missing feature. Any unavoidable difference goes in the bundle's deviations register (in its `AGENTS.md`) with a scenario that pins it.
- **The program decides what a command was.** The page never reads keystrokes or the screen to infer meaning; the program's own hook (zsh `preexec_functions`, Nushell `pre_execution`) writes allow-listed events that a root daemon relays.
- **Expected values come from an oracle**: the desktop program at the pinned version, built the same way, on x86_64. Never Homebrew, macOS, the bundle itself, or memory.
- **No engine bytes before Start**, no COOP/COEP or SharedArrayBuffer, no Terraform or deploy-workflow change.
- **The repo is the source of truth, this skill is the map.** Pins, line numbers, and step counts drift. Before copying anything, read the template bundle's `AGENTS.md` and its evolution doc, and trust them over this file when they disagree.
- Commit to `main`; never branch or open a PR. Deploy is manual; never trigger it.

## Step 0: Feasibility check (before any intake)

Some tools cannot run in a playground under these rules, and finding that out after eight intake questions wastes the user's time. Read `references/engine-decision.md` § "When nothing fits", then answer each question with evidence (a release page, a kernel config, a size), not memory:

1. **Real binary**: does an official or reproducibly built binary exist for i386 Linux (musl) or for wasm without threads/SharedArrayBuffer?
2. **Network**: does the core workflow need the network (image pulls, package installs, clone from a remote, an API)? The guest kernel has no INET and the site allows no network.
3. **Kernel features**: does it need namespaces, cgroups, overlayfs, iptables, KVM, or modules the shared `bzImage` lacks? Check `hugo/static/playgrounds/tmux/engine/src/kernel.config` (tmux, zsh, and fd all boot that kernel).
4. **Daemon or service**: does it need a long-running daemon, systemd, or a second machine?
5. **Size**: will Start-to-prompt plausibly fit the 10 MB gate (shipped 0.5 to 10.2 MB)?

If every answer is fine, say so in one line and go to Step 1. A borderline answer (size plausible but tight) counts as fine: put the verdict above the intake questions and list it as an S0 risk. If any answer blocks a faithful playground, do not simulate the tool. Explain which rule it breaks and offer these outcomes:

- **(a) Article only**: a Learn X article (or the existing one) with commands in `{practice="machine"}` fences and no playground.
- **(b) Spike only**: a timeboxed S0 (`nw-spike`) to test the one blocking assumption, with no DISCUSS or build until it passes.
- **(c) Adjacent tool**: a playground for a related tool that does run, stated honestly as that tool, not the blocked one (for Docker, the existing jq playground over saved `docker inspect` JSON). Check that the tool is actually in the guest you name; the zsh and fd guests ship no jq.

Offer (b) only when a check is uncertain; when the evidence already settles every blocker, say a spike would only confirm the failure. If the user named an article, note whether it is a `draft: true` stub (Step 1 #1 applies to outcome (a) too).

Present the outcomes with `AskUserQuestion` when it exists, otherwise as a lettered list with your recommendation. **STOP** and wait for the user's choice. Start no wave and write no file in the site repo until they answer.

## Step 1: Intake (ask before any wave)

Ask in one or two batches. Use `AskUserQuestion` when the tool exists; otherwise (a subagent, another client) print the questions as a numbered list with a suggested default for each, so the user can reply "1 yes, 2 default...". Each of these was decided interactively in a previous feature; asking up front saves a stalled wave later.

1. **Learn X article: Yes or No?** Check `hugo/content/blog/learn-x/learn-<name>/` first. Many `learn-x` folders are `draft: true` stubs; a stub counts as "no article yet", and nothing may link to it until it publishes.
   - **Yes, new article**: the article is slice 01 and ships first, standing alone (see Step 4).
   - **Yes, article exists**: add the Practice section and drill to it instead of writing a new one.
   - **No**: the playground lives only at `/playgrounds/<name>/` (or embeds in a page the user names). Drop the article slice, the article replay, and the milestone-1 article scenarios; say so in DISCUSS. The fidelity tests then replay `practice/exercises.md` (or a fixed probe list) against the oracle instead, and the page has to teach on its own (intro line, exercises). An unlinked standalone page gets almost no visitors, so ask whether a published post should link to it.
2. **Program and pinned version**: official i686 release binary (fd used one), signed upstream source built for i686, or the Alpine package? Which build features must match the official binary (Nushell's `static-link-openssl` mismatch forced a rebuild)?
3. **Budget**: target and ceiling in MB from Start to prompt (shipped: tmux 4.6, zsh 6.3, fd about 7, Nushell 10.2), gated at 20 Mbps / 50 ms RTT with 4x CPU throttling.
4. **Shared-helper change OK?** Editing `shared/common.js` or `shared/vm.js` changes every playground's `?v=`, re-downloads for returning readers, and means re-running every playground suite.
5. **Scope of the machine**: plugins, frameworks, network tools in or out? Which "not installed" and "no network" texts should notes cover?
6. **Tab behavior**: Tab goes to the program, Esc then Tab leaves (the WCAG 2.1.2 pattern every shell playground uses)? Since fd, this gate lives in `shared/vm.js`, so keeping it needs no shared change; changing it does. Confirm or change.
7. **Licensing**: what is the program's own licence, and does it bundle code under others (fish adds MIT, PSF, and LGPL parts)? A GPL program (fish, bash, git) joins the written offer alongside Linux and BusyBox; zsh, tmux, and sqlite did not need that. Reuse the approved written-offer wording from tmux/zsh `engine/VERSION`? Omit optional GPL sub-files where upstream allows?
8. **KPIs and timing**: targets for start, first-command, third-command rates; whether to wait on the prior playgrounds' day-60 KPI review; publish date.

**STOP after asking.** Do not pick the engine, start a wave, or write any file in the site repo until the user answers. Fill only what they explicitly leave to you with the defaults you suggested, and say which ones.

Record the answers so later sessions see them: with `graph_add_memory` (decision type) when that tool exists; otherwise write them to `docs/feature/<f>/discuss/intake.md` when DISCUSS starts, and mention them in the DISCUSS hand-off.

## Step 2: Pick the engine and the template

Read `references/engine-decision.md`. Short version:

| The program is... | Engine | Copy from |
|---|---|---|
| A single-shot CLI that builds to wasm without SharedArrayBuffer (sqlite, lua, jq-like) | wasm in a module Worker, `*.wasm.gz` | `jq` (glue driver) or `neovim` (WASI) |
| A CLI tool best learned at a shell prompt (fd, ripgrep, bat, git) | v86 + Linux i386 + Alpine BusyBox initramfs + xterm.js, the tool inside the zsh guest, restored from a saved RAM state | `fd` (finalized; default host, suite, CI, and descriptor template) |
| An interactive shell or TUI needing a pty, fork, a line editor, or a filesystem (fish, bash) | Same v86 stack, the program as the guest's shell | `fd` for host, suite, and CI shape; `zsh` for the login-shell overlay and hook; Nushell's `Dockerfile.nu-i686` when the program is Rust with no i686 binary |
| Same, but the binary is too big for a RAM state within budget | v86 + lazy ext2 disk + warm-up state | `nushell` |

When the choice is unclear, the spike (S0) settles it. Cold boot is never acceptable; always restore a saved state.

Default to the newest **finalized** playground of the same engine (fd for v86 as of 2026-10-10); re-check `docs/evolution/` because a newer one may have shipped.

**Is the template finished?** A playground is settled once `docs/evolution/<f>-evolution.md` exists. If a template you copy from is still in DELIVER (zsh was, as of 2026-10-10), its suite, its `BASE_COMMIT`, and possibly `shared/` are still moving: copy from the latest commit, re-diff against it before DISTILL, and tell the user, who may prefer to wait for it to finalize.

## Step 3: Drive the nWave waves

Use the nWave skills in this order. Feature id: `<name>-wasm-playground`. Test/env prefix: the name's first two letters + `WP` (zsh `ZSWP_`, Nushell `NUWP_`, fd `FDWP_`); on a collision with an existing prefix, ask. At each wave, give the agent the playground-specific context listed here and point it at the reference files.

1. **DISCUSS** (`nw-discuss`): about 11 stories and 7 to 8 slices plus S0. Feed it the Step 0 verdict, the intake answers, the ground rules above, and the D-rules from the template's `docs/feature/<template>-wasm-playground/feature-delta.md` (fd's by default). Slice order that worked: article (slice 01, if Yes) → S0 spike → shared-helper slice (only if Step 1 #4 was yes) → walking skeleton → milestones (fidelity, notes, keys/phone bar, analytics).
2. **DESIGN, pass 1** (`nw-design`, propose mode): ADRs `adr-<XX>WP-00n-*` for engine, signals, oracle, and loader. Mark anything the spike must answer as `[S0]`.
3. **Spike S0** (`nw-spike`): validate the questions listed in `references/engine-decision.md` § "What the spike must answer". Write `docs/feature/<f>/spike/findings.md`, then promote the recipe into `engine/src/`. A spike run as a subagent may be blocked from writing report files; have it return the findings text and save the file yourself. Build artifacts stay in the scratch folder for DELIVER.
4. **DESIGN, pass 2**: resolve every `[S0]` marker, write `design/upstream-changes.md`, mark ADRs Accepted.
5. **DISTILL** (`nw-distill`): copy the template suite's shape from `references/testing.md`. Everything starts `@pending`, the skeleton `@awaiting_engine`, so the default run exits 0. Do not scaffold shared helpers here; that changes `?v=` and trips the guards.
6. **DELIVER** (`nw-deliver`): one TDD step per commit with `Step-Id`/`Task-Id` trailers, un-skipping one scenario at a time. Build the engine with `references/build-recipe.md`. Register the bundle with `references/file-inventory.md`. Prove the workflow with actionlint and `act` before pushing (`references/testing.md` § "Prove CI locally first"); GitHub runs confirm, they are not for iteration.
7. **Finalize** (`nw-finalize`): `docs/evolution/<f>-evolution.md`. DEVOPS was skipped for every playground; skip it unless the user asks.

Check `docs/feature/` and `git log` before starting a wave: features often move outside nWave, and parallel sessions share this worktree. Commit your own files by explicit path, never `git add -A`.

## Step 4: The Learn X article (only when the user said Yes)

Read `references/article-integration.md`, then invoke the `write-article` skill with the **Learn X** framework (`references/learn.md` inside it). Pass it:

- the program, pinned version, and what the machine cannot run (from the deviations register);
- the playground section requirements: a `## Practice <Name>` section **before** `## Command Reference`, holding the intro paragraph, the "cannot run" list, `{{< playground "<name>" >}}`, and a numbered drill of about ten minutes;
- the replay rules: each fenced `<lang>` block is one session in article order, output goes in the following `text` block from the oracle, never hand-typed, and blocks the shell cannot run get `{practice="machine"}` on the fence.

`write-article` runs the cover image (Canva) and ai-sanitize. Then run `write-validate-article` on the result. As slice 01, the article ships with a verified Command Reference before the engine exists; the replay suite picks up its commands automatically once the engine lands.

## Step 5: Hand back to the owner

After DELIVER, list what only the owner can do (from `references/gotchas.md` § "After deploy"): deploy by hand, flip `tests/browser/tests/<name>-playground.spec.ts` from `test.fixme`, record live transfer sizes, check real Safari/iOS and mobile LCP, and set the day-60 KPI review date. Save a project memory for the new playground modeled on the existing `nushell-wasm-playground` memory: what shipped, how to rebuild, the suite and its flake knobs.

## Reference files

- `references/engine-decision.md`: wasm vs v86 vs lazy disk, when nothing fits, budgets, what S0 must answer.
- `references/file-inventory.md`: every file a new playground adds or extends, with paths.
- `references/build-recipe.md`: v86 and wasm engine builds, saved state, silent fixture, VERSION, `?v=` caching.
- `references/testing.md`: oracle, article replay, suite layout, env knobs, CI sharding, flakes.
- `references/article-integration.md`: what the Learn X article must contain for the tests.
- `references/gotchas.md`: the traps that cost previous sessions hours, plus licensing and after-deploy checks.

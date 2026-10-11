# Gotchas, licensing, and after-deploy checks

## Traps that cost previous sessions hours

1. **GCC 15.2 miscompiles on i386.** Stock Alpine tmux garbled space, `-`, and `,` in every prompt. Fix: patch plus `-fno-tree-switch-conversion`. Keep the oracle on x86_64 so a miscompile shows as a mismatch.
2. **Hooks that don't exist in the pinned version.** Check every hook name in the spike.
3. **Same version, different build features.** Nushell's oracle had `static-link-openssl` and the guest didn't; the rebuild forced a new disk and state. Diff features and flags in the spike.
4. **Warm-up leaks into the reader's session.** End the warm-up with Ctrl-D; rerun the "0 disk pieces" and fidelity checks after any warm-up change.
5. **`@@READY` before the prompt.** Require both signals; right-trim the cursor row.
6. **cpio drops mtimes.** Touch @0, then apply manifest mtimes; glob qualifiers and `ls -t` depend on them.
7. **Events FIFO blocks the shell.** Use a regular file, mode 622. COM2 stays root-only with allow-lists at both ends.
8. **Playwright outruns the VM.** Key gaps, quiet-screen waits, `SLOWDOWN`; CI needs `READY_TIMEOUT_MS=60000` and `SLOWDOWN=3`.
9. **Rosetta writes `~/.cache/rosetta`** into amd64 containers on Apple Silicon. The oracle helper deletes it and fails if it reappears.
10. **CI uid is 1001.** Open the oracle home to any uid.
11. **gitlab.alpinelinux.org returns 418 to CI.** Vendor the files and check them with sha512.
12. **Enforcement 12** (no shortcode/layout/shared change) diffs against a `BASE_COMMIT` constant. The checks shard needs `fetch-depth: 0`; a sanctioned shared change means updating `BASE_COMMIT`.
13. **Vacuous tests.** A weight check counted JSON-LD; an empty exercise list passed; a first-person scan read site chrome. Refuse empty inputs and break each guard by hand to prove it.
14. **Ignored fixtures and deployed AGENTS.md.** The user's global `~/.gitignore` ignores `node_modules/`, `dist/`, and `.env`, and a literal `.gitignore` inside `practice/` would act as a live ignore file for the repo. Store such practice files under neutral source names (`shop/gitignore`, `shop/_node_modules/...`) and let `manifest.json` map them to their guest paths. Check `git add -n` on the new paths; add AGENTS.md to the hugo.toml exclusion.
15. **Layout shift and fit.** Eager sizing goes in `jeff_custom.css`, not the lazy `playground.css`. The article terminal stays inside the column: 80 columns at 14 to 15 px, the font shrinks to a 9 px floor, then columns drop toward 20. The empty 44 px row on phones is accepted.

16. **Bind-mounted oracle homes lie about access checks on a Mac.** On Docker Desktop's file sharing, `faccessat` said a 0666 file was executable, so `fd -t x` listed every file while `test -x` disagreed. Copy the practice home into the container (`tar` over stdin) instead of bind-mounting it whenever the program checks permissions.
17. **Rosetta's `~/.cache` appears whenever an external program runs** in an amd64 container on Apple Silicon. Builtin-only examples (zsh) dodge it; a tool playground trips it on every command. Clear it before each command and flag any output that shows `.cache`, and run the final check on native x86_64.
18. **The replay needs at least 40 commands** (`MIN_REPLAYABLE`). Plan enough short, verified Command Reference examples while writing the article instead of lowering the floor.
19. **Unrelated site commits trip the scope guard.** Enforcement 12 diffs `main.tf` and the shared layouts against `BASE_COMMIT` across the whole repo, so another session's Terraform change (fd hit a Matrix `.well-known` edit) fails the checks shard. Moving `BASE_COMMIT` loosens a guard: show the user the offending diff and get approval first, and keep any slice-02 base that must predate the shared move pinned separately.
20. **The integration shard's timing budgets fail under act** on Apple Silicon (amd64 emulation: a Tab took 9.75 s against 9.0 s). Prove the other shards with act and let GitHub's x86_64 run prove integration; check whether the HEAD code fails the same budgets before blaming a step.
21. **Scenarios that already pass need a named mutant**, and some can't have one: a two-layer defense (guest relay plus host allow-list) survives any single-layer mutant, and a mutant that just stops ready proves only that a scenario can fail. Log these as test-design gaps for finalize instead of claiming a proof.
22. **The reviewer agent runs on a small model.** Its verdict is useful but verify its claims (fd's review said no test imports internals; the unit tests do) before quoting them.

Also: `python -m http.server` resets connections under load (local `download_failed` flakes; rerun). v86 Reset re-fetches lazy chunks (open issue). Chunk URLs can't carry `?v=`. Measurements: minified HTML defeats quoted-attribute greps; reconcile counts before reporting them.

## Working in this repo

- Parallel sessions share the worktree and an auto-sync commit runs within seconds. Edit and commit in one command, and stage only your own files by path.
- nWave status files can lag reality. Check `git log`, the tests, and the live site before running a wave.
- Commit to `main`. No branches, no PRs. Don't push or deploy unless asked.

## Licensing

- `engine/NOTICES.txt`: full licence texts of the non-GPL components (for zsh: MIT-Modern-Variant zsh, libcap2, ncurses, musl).
- `engine/VERSION` § "Written offer for GPL-licensed software": Linux, BusyBox, alpine-baselayout; a three-year offer, contact https://jeffbailey.us/contact/, upstream source URLs with aports commit hashes, the kernel config path. The user approved this wording for tmux and reused it; confirm reuse at intake.
- Drop avoidable GPL pieces where upstream permits (zsh's four GPL-2.0 completion files), and make the build fail unless exactly those are found.
- An unlicensed wrapper gets rebuilt from upstream instead (Neovim).

## After deploy (owner only)

Deploys are manual (`deploy-website.yml`, workflow_dispatch). S3 sync has no `--delete`, so an old `disk-*` folder stays live; that's accepted.

1. Flip `tests/browser/tests/<name>-playground.spec.ts` from `test.fixme` to `test` and set its article path.
2. Run the `@requires_external @post_deploy` scenarios: `python -m pytest -m requires_external`.
3. Record the live `content-encoding` and transfer size of the state, `v86.wasm.gz`, and the Start-to-ready total.
4. Check real Safari on macOS and iOS (soft keyboard; whether iOS allows 128 MB, with 96 MB as the fallback lever) and a human Ctrl-r / prefix key in Chrome and Firefox.
5. Mobile Lighthouse LCP, median of 3, at most 2.5 s.
6. Day 60: judge the KPIs in GA4 (`<name>_playground_start`, `_ready`, `_first_command`, `_third_command`, `_error`; `page_path` and `reason` only) and GSC on the page dimension for weeks 5 to 8.

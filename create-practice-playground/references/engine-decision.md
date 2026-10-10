# Engine decision

Every playground ADR started from one rule: run the real program. The engine choice is about how to get that program into a browser tab within budget, with no SharedArrayBuffer (the site sends no COOP/COEP headers and must not start).

## Decision tree

1. **Does the program build to wasm with its UI, terminal handling, and line editor intact, without threads/SAB?**
   Use **wasm in a module Worker**.
   - jq: jq-wasm's `jq.wasm` byte for byte, plus its Emscripten glue patched by `engine/src/glue-driver.patch` (argv as typed, MEMFS practice files, untrimmed output). The host kills the Worker after 10 s. About 0.5 MB.
   - Neovim: WASI (`wasm32-wasip1`) + Asyncify, linked with a 1 MiB stack (`-Wl,-z,stack-size=1048576`; the 64 KiB default crashed netrw). About 2.6 MB.
   - Fits single-shot CLIs and self-contained TUIs: sqlite, lua, jq-like filters.
2. **Is it an interactive shell or a program that needs fork, a pty, job control, or a real filesystem?**
   Use **v86** (BSD-2) running Linux i386 with an Alpine BusyBox/musl initramfs, xterm.js for the screen, restored from a **saved machine state** at 128 MB guest RAM.
   - Cold boot is never acceptable (tmux 7.5 s, zsh 40 s at 4x CPU).
   - 64 MB guest RAM is impossible: v86 loads the initrd at 64 MB.
   - Default is a RAM state with the program inside the initramfs (tmux, zsh).
3. **v86, but the RAM state misses budget because the binary is large?**
   Add a **lazy ext2 disk** in 64 KiB `zstd -19` chunks plus a **warm-up state** that has already run the article's commands once, so their pages are cached (Nushell: 47 MB `nu`, 10.2 MB to ready).

Rejected every time, so don't re-litigate without new facts: WebVM/CheerpX, container2wasm, WASIX (need SAB, have licence limits, or cost tens of MB). nu-in-wasm failed because reedline/crossterm/nu-cli don't compile for wasm; expect similar for other line-editor-heavy shells.

Rough guesses for likely next candidates: fish and bash → v86 like zsh; ripgrep, bat, and other CLI tools → v86 inside zsh like fd; git → v86 like fd unless a maintained wasm git exists (remote operations stay out: no network); sqlite and lua → wasm. The spike decides.

## When nothing fits

SKILL.md Step 0 runs these checks before intake. Each one has stopped a design before; any "no" means the real program cannot run faithfully, and a simulation is never the fallback.

| Blocker | Why it fails here | Examples |
|---|---|---|
| No i386 Linux or SAB-free wasm build | v86 emulates i386 only; wasm without threads is the other path | tools shipped only for x86_64/arm64 with no buildable source |
| Core workflow needs the network | the guest kernel has no INET; the site allows no network | `docker pull`, `kubectl`, `aws`, `npm install`, `git clone` of a remote |
| Needs kernel features the tinyconfig `bzImage` lacks | rebuilding the kernel with namespaces, cgroups, overlayfs, or netfilter grows the state and every suite | Docker/Podman engine, iptables, systemd |
| Needs a daemon or a second machine | one guest, one CPU, 128 MB RAM, restored from a state | dockerd, databases with a server, Kubernetes |
| Far over budget | 10 MB gate from Start to prompt; Nushell at 10.2 MB needed a lazy disk | multi-hundred-MB runtimes |

Outcomes to offer, in this order: (a) article only, with commands in `{practice="machine"}` fences; (b) a timeboxed spike that tests only the blocker; (c) a playground for an adjacent tool that does run, named as that tool. Then stop for the user's choice.

## Budget

- Gate (D4): Start to prompt within 10 MB and 10 s at **20 Mbps / 50 ms RTT, 4x CPU** (CDP throttling). Each feature also sets its own enforced ceiling (zsh: 7 MB).
- Tracked, not gating (G5): Fast 4G, 9 Mbps / 150 ms.
- Shipped: tmux 4.61 MB / 2.4 s; zsh 6.33 MB raw (5.81 MB with live gzip) / 3.06 s; Nushell 10.21 MB / 5.6 s.
- **Sum transfer sizes from the network log, never from file sizes on disk.** CloudFront re-gzips some types (it gzips `libv86.mjs` and `xterm.mjs` about 4x, and re-gzips already-gzipped wasm).

## What the spike must answer

Write each answer into `docs/feature/<f>/spike/findings.md` with the command and output that proves it.

1. The engine runs the program's line editor and completion in the page (Tab, history, redraw).
2. Bytes and seconds from Start to prompt under the gate profile.
3. Binary source: distro package vs signed upstream tarball. Alpine 3.24 ships zsh 5.9 while upstream is 5.9.2; the user chose upstream.
4. Build features match the official binary (`version | get features` for nu; `--version` / configure flags otherwise).
5. RAM state vs lazy disk.
6. Readiness signal: the daemon's `@@READY <ver>` **and** the prompt on screen; after restore, Ctrl-L must repaint the prompt.
7. Hook names exist in the pinned version (tmux's design named `after-source-file`, which 3.7c lacks).
8. Licences of every shipped component, and which GPL parts can be dropped.
9. Exact error texts for unavailable commands and network use, so notes and the deviations register can quote them.
10. Startup terminal queries. Some programs (fish 4: DA1, XTVERSION, kitty keyboard protocol) ask the terminal questions at startup and wait. `make-state.mjs` must answer them during the build (it already answers `ESC[6n`), and they must not stall or leak stray text after restore.
11. First-run writes (history, universal variables, caches like `~/.zcompdump`). Take the state after them, and make sure the reader inherits no history that would surface in autosuggestions or Ctrl-r.
12. Walk order. The initramfs lists directory entries in creation order and `build-initrd.sh` creates them C-sorted, so a tool's unsorted output in the guest happens to look sorted, while the oracle's overlay filesystem returns hash order. Listings after a rename or a new visible file, and `-X`-style lines that list several paths, differ between the two; sort them in the article.
13. Timing-dependent output. Some tools change output with speed or CPU count: fd sorts results only if the search ends within 100 ms (`DEFAULT_MAX_BUFFER_TIME`), then streams in walk order, and `-x` never sorts. On a throttled emulated CPU that can reorder lines. Find such switches in the source, measure at 4x CPU and CI slowdown (e.g. 20 of 20 runs), and keep article examples order-stable.
14. i386 build correctness against the x86_64 oracle (GCC 15.2 miscompiled tmux's key switch on i386).
15. Missing system calls. The shared tinyconfig kernel returns ENOSYS for some calls threaded runtimes use (fd's D19 lists `madvise`, `membarrier`, `rseq`); confirm the program falls back cleanly, especially Rust and Go binaries.

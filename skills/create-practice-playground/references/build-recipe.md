# Engine build recipe

The engine and its saved state are built **locally** and committed. CI never builds them. Build in a scratch directory outside the repo; record unshipped outputs in `engine/src/artifacts.sha256`. You need Docker and Node 26. The authoritative, current commands are in the template bundle's `AGENTS.md` § "Rebuild the engine"; read it first and copy its shape.

## Contents

- v86 playgrounds (kernel, program, initrd, overlay, state, silent fixture, records, lazy disk)
- Wasm playgrounds
- Versioning and caching

## v86 playgrounds

1. **Kernel.** Reuse tmux's `bzImage` unmodified (`hugo/static/playgrounds/tmux/engine/src/`, built by `build.sh` in debian:trixie from tinyconfig + `tmux.fragment`). That config has `CONFIG_NET` and `UNIX` but no `INET` (no IPv4, which is the point), 2 UARTs, `RD_GZIP`, and `COMPAT_32BIT_TIME` (needed for `time` to set the clock). A lazy disk needs Nushell's `build-kernel.sh` + `nu-lazy.fragment` (PCI, ATA_PIIX, SCSI, EXT2).
2. **Program.** A `build-<prog>.sh` that runs in a digest-pinned `alpine:3.24@sha256:…` with `--platform linux/386` (zsh took about 11 min under qemu). It verifies the tarball's sha256 and its signature against a committed keyring, and uses Alpine's APKBUILD flags. **The same script builds the amd64 oracle**, so guest and oracle can't drift. Prefer dynamic linking against the guest's musl; Nushell needed a static i686 build (`Dockerfile.nu-i686`).
3. **Initrd.** `docker run --rm -v "$PWD:/b" -v "$W:/w" debian:trixie sh /b/engine/src/build-initrd.sh <program tree>`. It fetches the apks listed in `alpine-apk.sha256` and checks them, strips docs, drops unlicensable or unneeded parts (fail the build unless exactly the expected files were dropped), copies `overlay/`, and places `practice/` per the manifest with reader ownership. cpio drops mtimes, so `touch -d @0` everything, then apply manifest mtimes, then `find | LC_ALL=C sort | cpio -H newc --reproducible | gzip -9 -n`.
4. **Overlay** (`engine/src/overlay/`):
   - `init`: `busybox --install -s; exec busybox init`.
   - `etc/rcS`: mounts, hostname `practice`, `stty` 80x24, `chown 0:0 /dev/ttyS1 && chmod 600` (the reader can't open COM2), and `/run/practiced/events` as a **regular file, mode 622, never a FIFO** (a stopped daemon would block the shell).
   - `etc/inittab`: `ttyS1::respawn:/sbin/practiced`, `ttyS0::respawn:/sbin/practice-login`.
   - `sbin/practice-login`: on respawn appends `exited`; runs `exec env TERM=xterm-256color LC_ALL=C.UTF-8 TZ=UTC /bin/login -p -f reader`.
   - `sbin/practiced` (root) owns COM2. Host to guest: only `time <epoch>` (sets the clock, answers `@@READY <ver>`) and `size <cols> <rows>` (runs `stty`, which sends SIGWINCH). Guest to host: `@@READY <ver>`, `@@CMD`, `@@CFG`, `@@MSG <key>[:<name>]` from **exact allow-lists**, `@@EXITED`. It polls the events file every 0.25 s, relays allowed lines, truncates.
   - The program's own hook writes events: zsh `/etc/zsh/zshrc.d/practice.zsh` appending to `preexec_functions` (never `add-zsh-hook`, so `whence` matches the oracle); Nushell `vendor/autoload/practice.nu` (`pre_execution`, `command_not_found`). Keep practice code out of the reader's rc file: `cat ~/.zshrc` must equal `practice/zshrc`.
   - Vendor any distro config files the build needs (gitlab.alpinelinux.org answers CI runners with HTTP 418) and check them with sha512.
5. **State.** `cd engine/src && node make-state.mjs $W/out/initrd.cpio.gz`. Boot at 128 MB, answer `ESC[6n` with `ESC[1;1R`, wait for `@@READY <ver>` **and** the prompt (in zsh, `@@READY` came 1.3 s before compinit finished), settle 2 s, save, **restore into a fresh emulator**, send `time` and Ctrl-L, and write `../state.bin.zst` only if that restored machine answers. On any timeout, write nothing.
   - Boot the state build with the kernel parameter `init_on_free=1` (a constant in `make-state.mjs`). The kernel frees its unpacked initrd copy after boot; without the parameter those pages keep the cpio bytes and land in the saved state. It cut fd's state by 452 KB with no kernel rebuild and no behavior change.
   - Warm-up (lazy disk only): run the article's commands from `make-warmup.py`, then a Tab, and end with **Ctrl-D**, or the reader's session inherits history entries and error numbering shifts.
6. **Silent fixture.** `node make-state.mjs --silent …` writes `tests/acceptance/<f>/fixtures/silent-machine.bin.zst`: the same machine with `practiced` disabled (zsh appends a cpio whose inittab lacks the ttyS1 line; Nushell boots with `8250.nr_uarts=1`). The page must end in `boot_timeout`. Rebuild after **any** guest change.
7. **Records.** `engine/VERSION`: pins, licences, upstream URLs and sha256s, the sha256 of **every** engine file, and the GPL written offer. The state is not byte-reproducible, so the gate is the scenarios plus VERSION, never a rebuilt hash. The descriptor computes `state-sha256` at Hugo build time and the host verifies it before restore (a truncated state crashed Chromium on Linux CI).
8. **Lazy disk** (only if needed). `build-disk.sh` writes `engine/disk-<md5 of image>/<prog>-<start>-<end>.img.zst` 64 KiB chunks plus `disk.json` `{dir, size, chunk}`. v86 option `hda: {async: true, use_parts: true, fixed_chunk_size: 65536}`. **No `?v=` on chunk URLs** (v86 breaks); the folder name is the version. Keep exactly one `disk-*` folder and stage the add and remove by name. Set `read_ahead_kb=16` (cut startup reads from 22.6 MB to 9 MB). Wrap `XMLHttpRequest.open` in the host to catch chunk 404s, which v86 otherwise ignores.

**Any guest change** (overlay, practice files, program tree, warm-up list) means initrd + state + silent fixture + VERSION sha256s, together, in one commit.

## Wasm playgrounds

- `engine/src/build.sh` rebuilds from a sha256-pinned tarball (plus a glue patch if needed) byte for byte.
- Ship `*.wasm.gz`; unpack with `DecompressionStream`; detect gzip by the magic bytes `1f 8b`, **never** by `Content-Encoding` (CloudFront re-gzips wasm and the header lies; this broke live Start once).
- Run it in a module Worker the host can stop. Practice files live in MEMFS.
- Keep `blob:` in the CSP `worker-src`.

## Versioning and caching

- Every bundle URL carries `?v=<md5 of every bundle file + every shared/ file>`, computed by `layouts/partials/neovim-playground/bundle-bytes.html`. It skips dotfiles, `run.sh`, and `AGENTS.md`; `engine/src/` **is** included. Never bump a version by hand; there are no `v2/` folders.
- HTML is cached for a year, so a new `?v=` is what makes readers fetch new bytes.
- **Blast radius:** editing `shared/common.js` or `shared/vm.js` changes every playground's `?v=`. It needs the user's approval, must land as its own slice before the new walking skeleton, and needs every playground suite re-run (one per `.github/workflows/test-*-playground.yml`, plus playground-fullscreen; Neovim has its own venv). Update each v86 suite's `platform_steps.BASE_COMMIT` when a sanctioned shared change lands (Enforcement 12 diffs against it).

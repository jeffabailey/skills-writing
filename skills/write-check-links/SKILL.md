---
name: write-check-links
description: Checks the links in a Markdown file with lychee and the Hugo site's lychee.toml, then triages every failure as broken, known false positive, or unverified, with the source line and a fix. Also checks Hugo {{< ref >}} targets and root-relative /blog/ links against hugo/content, which lychee cannot see. Use when the user says /write:check-links, wants to validate links, check for broken links or dead URLs, verify URLs in a post before publishing, or asks "is anything broken in this article".
---

# Check Links

Run [lychee](https://lychee.cli.rs/) on one file and tell the author which failures are real.
Raw lychee output on this blog is noisy: cover images 404, slow hosts time out, and internal links
are checked against the live site. The bundled script runs lychee the way CI does and sorts that out.

## Workflow

1. **Get the file.** The user passes a path. If none, ask which file.

2. **Run the script** from anywhere (it finds the git root itself):

   ```bash
   python3 <skill-dir>/scripts/check_links.py <file.md>
   ```

   What it does, so you can do it by hand if the script can't run:
   - **Preflight:** `command -v lychee`. If missing it exits 3 with `TOOL MISSING` and
     `brew install lychee`. Report that as "tool missing", not as a link failure, and stop.
   - **Finds `lychee.toml`** by walking up from the file, falling back to `<git-root>/hugo/`.
     The Hugo dir is the one with `hugo.toml`, `config.toml`, or `config/_default/`
     (jeffbaileyblog uses `hugo/config.toml`, not `hugo.toml`).
   - **Runs from the git root**: `cd <git-root> && lychee --config hugo/lychee.toml --format json <file>`.
     lychee reads `.lycheeignore` only from the cwd, and jeffbaileyblog keeps about 100 URL
     exclusions in the repo-root one. Running from `hugo/` or the article dir silently drops them.
   - Expect about 40 seconds (`max_concurrency = 4`, retries). Local lychee may be newer than CI,
     which pins **lychee v0.22.0** (`.github/workflows/check-links.yml`).
   - To re-triage without re-running lychee: `--lychee-json report.json`.

3. **Read the triage.** The script prints a table: line, URL, status, verdict, fix. Verdicts:

   | Verdict | When | What to tell the author |
   | --- | --- | --- |
   | broken | 404/410, host does not resolve (DNS), missing image, internal URL with no page in `hugo/content`, link to a draft | Must fix before publishing. Give the fix. |
   | known false positive | 404 on `https://<base_url>/<file>.png` where the file exists next to `index.md` (or in `hugo/static/`) | No action. lychee rewrote the bundle-relative path onto `base_url`. |
   | unverified | TIMEOUT, 5xx, connection failure to a host that resolves, internal page that exists in content but is not deployed yet | Not proven broken. Re-run later or open in a browser. Never call these broken. |

   Internal links (`/blog/...`) are matched against `url:` front matter, then the section path with
   `slug:` applied. `{{< ref "x" >}}` and `relref` targets are matched by bundle folder or file
   name (Hugo resolves refs by content path, not slug); a draft target is broken because the
   normal build fails with REF_NOT_FOUND. If you need certainty on refs, the Hugo build is the
   real gate: `cd hugo && hugo --buildDrafts -d "$(mktemp -d)"`.

4. **Report** in this shape, broken first:

   ```markdown
   Checked <file>: N links (lychee <version>, .lycheeignore applied). Broken: B. Unverified: U. False positives: F.

   | Line | URL | Verdict | Fix |
   | ---: | --- | --- | --- |
   ```

   Then list ref/relref results. Fixes to suggest, in order: correct the URL (search the target
   site for the moved page), swap in a Wayback Machine copy (`https://web.archive.org/web/*/<url>`),
   remove the link, or, for a host that always blocks CI but works for readers, add a regex to the
   repo-root `.lycheeignore`. Don't edit the article unless the user asks.

   If nothing is broken, say so plainly and still list unverified links so the author can spot-check them.

## Notes

- lychee skips RFC 2606 reserved TLDs (`.invalid`, `.example`, `.test`) as excluded, not broken.
- Exit codes: 0 nothing broken, 1 broken found, 3 lychee missing, 4 no lychee.toml, 5 lychee produced no report.
- Outside jeffbaileyblog the script still works: with no `base_url` or `hugo/content` it skips the internal-link and ref checks and says so.

# Learn X article with a playground

Only when the user said Yes. The article is written by the `write-article` skill using its **Learn X** framework; this file lists what the playground and its tests add on top. Models: `hugo/content/blog/learn-x/learn-zsh/`, `learn-nushell/`, `learn-tmux/`. Read one in full before writing.

## Front matter

Learn X standard: `url: /blog/YYYY/MM/DD/learn-<name>/` and `slug` unquoted, `date`, `lastmod`, categories `Learn X`, `Software Engineering`, `Practice`, `keywords`, `type: post`, `articletype: learn`, `cover.image: learn-<name>.png` with alt text, `draft: false`. The body starts with `{{< partial "learn_x_header" >}}`.

## Sections the milestone-1 scenarios check

1. `## What You'll Learn`
2. A "when to use <name> vs <alternative>" section.
3. The 20/80 core sections, each command in a fenced `<lang>` block followed by a `text` block with the oracle's output.
4. `## Practice <Name>`, **before** the Command Reference, containing:
   - an intro paragraph: the pinned version, nothing downloads until Start, no network, Esc then Tab leaves the terminal;
   - a "cannot run here" list matching the deviations register (network, plugins, programs BusyBox lacks);
   - `{{< playground "<name>" >}}`;
   - a numbered **drill** of about ten minutes: exact commands, what each unusual part means, and what the reader should see.
5. `## Command Reference`: "Verified with <prog> <ver>", `{{< command-search >}}`, and `### Examples` pairs.
6. `## <Name>: Beyond the Basics` with video, audio, book, and online resources.
7. `## Related Content`, then `{{< partial "category_footer" >}}`.

## Rules the tests and the site enforce

- **Output comes from the oracle, never typed by hand.** Run each block in the oracle and paste its output.
- Shown output must not depend on the clock, and should come from the program's builtins rather than `ls -l` (BusyBox's output differs from GNU's).
- Blocks the shell can't run get `{practice="machine"}` on the fence; the site labels them "Runs on your machine, not in the practice shell".
- No block starts with `!` or `^`.
- No first person outside code and quotes (Diátaxis how-to voice: imperative, second person).
- Internal links only to published pages; verify every `{{< ref >}}` target is not a draft stub.
- Cross-link the other playground articles (Learn Zsh, Learn Nushell, Learn Tmux) and add the new article to theirs.
- Never link `content/prompts/`.
- Cover art via Canva only (the `generate-cover-image` skill).

## Verifying outputs before the suite exists

Slice 01 ships before the acceptance suite, so drive the oracle from a scratch script: import the newest suite's `steps/oracle.py` (`DesktopZsh`/`DesktopSession`), point its image variable at the new oracle, and run each `zsh` block as one fresh session, comparing with the `text` block after it. Record the run in `docs/feature/<f>/deliver/reference-verification.md`. Check claims made in prose ("prints nothing", "adds X") the same way.

## Ordering

The article is slice 01: it ships first with a verified Command Reference and no playground shortcode, standing on its own. The shortcode and drill arrive with the walking skeleton. If a cross-linked article is under an SEO freeze (Learn jq was), ask before editing it.

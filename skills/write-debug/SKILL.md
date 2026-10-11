---
name: write-debug
description: Systematic debugging and bug minimization with a bundled Bug Minimizer prompt. Triages noisy reports, shrinks the trigger to a minimal runnable repro, finds the root cause, and proves the fix by running the repro before and after. Use when the user says /write:debug or /write:bug-minimizer, pastes a bug report, wants to minimize or reproduce a bug, isolate an issue, or asks for structured debugging help. Triggers on "bug report", "minimize bug", "bug minimizer", "debug", "reproduce bug", "isolate issue", "minimal repro", "what broke".
---

# Debug and Minimize a Bug

Turn a bug report into a verified minimal reproduction, a root cause, and a fix. The prompt in `references/bug-minimizer.md` is the method and the output format; this file says how to fill it and when to stop.

Also invoked as `/write:bug-minimizer` (that skill was merged into this one).

## Workflow

### 1. Read the prompt

Read `references/bug-minimizer.md`. Its fields are `[BRACKET]` placeholders with no defaults.

### 2. Intake: fill the fields from the report

Pre-fill every `[BRACKET]` field from the report, the code, and the repo (language from file extensions, versions from `python3 --version`, `node --version`, lockfiles, `uname -sr`). Use `n/a` for fields that do not apply (a stdlib script has no framework; a CLI has no browser) and `unknown` for facts nobody has given. Never ship a delivered analysis with a raw `[BRACKET]` left in it.

Two fields are required before any analysis: **how to trigger it** (a command, steps, or code) and **what actually happens** (output, error, or observed behavior). If either is missing:

* If you can't tell which program or component is broken ("the review thing"), ask which one first, in the same message. Don't go hunting through repos to guess.
* Send ONE message that lists every unfilled field by name (group related slots, such as the three steps), says which two block the analysis, and gives concrete commands the user can run to collect them (for example the failing command with `2>&1 | tail -50`, `git log --oneline -10`, the tool's `--version`).
* Then stop. Do not write a repro, a root cause, or a fix from a guess. A fabricated repro is worse than none because it looks like evidence.

Everything else (expected behavior, environment, bug type) can be inferred or marked `unknown`; don't block on it.

### 3. Triage (multi-symptom reports)

If the report describes more than one distinct symptom (side remarks like "same with two config files" or "I'm on Python 3.13" are context, not symptoms; fold them into step 4 instead), classify each one before minimizing anything: **defect**, **expected behavior**, **environment/noise**, or **needs evidence**. Give a one-line reason per symptom, checked against the code where it is cheap (for example, `__pycache__` folders are normal CPython behavior unless the code claims otherwise). Then minimize one defect at a time. Without this step the template's single "how to trigger it" slot tempts you to merge symptoms or silently pick one.

### 4. Reproduce and minimize, on a copy

Copy the code to a scratch directory and work there; the prompt's "comment out features" and "hardcode values" steps edit files, and the user's tree is not yours to edit. Write the trigger to a file and run it to capture the failing output first.

Then shrink in this order, rerunning after each cut and keeping only cuts that still fail:

1. **Inputs**: drop extra files, records, arguments, flags (a second resolver file, a second config group).
2. **Config**: replace config files with inline literal values (when the CLI only reads config from a file, this happens together with step 3).
3. **Direct call**: call the suspect function directly instead of the CLI, server, or UI.
4. **Boundary values**: sweep the edges (0, 1, max, max+1, empty) to pin the exact failing condition.

This order goes from cheapest to most invasive, and each step removes a whole layer of red herrings before you read internals. Make the final repro exit non-zero (assert or `sys.exit(1)`) while the bug is present, so a script can tell pass from fail.

### 5. Root cause and fix

Name the file, line, and faulty logic. Check the reported environment only if the evidence points there (a reported Python 3.13 vs a local 3.14 rarely matters for a logic bug, but say whether you checked).

### 6. Verify

Apply the fix to a second copy, then run the repro on both:

```bash
bash <skill-dir>/scripts/verify_repro.sh <buggy_copy> <fixed_copy> -- python3 -I /abs/path/repro.py
```

It runs the command with each directory as the working directory and exports it as `$REPRO_ROOT`; with `python3 -I` the cwd is not on `sys.path`, so start a Python repro with `sys.path.insert(0, os.environ.get("REPRO_ROOT", os.getcwd()))` before importing the code. It prints `VERIFIED` only when the repro fails on the buggy copy and passes on the fixed one. Also rerun the user's original trigger on the fixed copy when that is possible.

Label the repro **Verified** only after a real run. If you could not run it (missing runtime, external service, no code provided), label it **Unverified** and say exactly what the user should run to confirm. Paste real output only; never write output you did not see.

### 7. Deliver

Open with a short header of the filled fields (language, framework, bug type, environment). Then use the prompt's Output Format: Triage (if any), Minimal Reproduction Code with its Verified/Unverified label, Repro output before and after, Root Cause Analysis, Fix, Prevention (turn the repro into a regression test and cover the boundary values), and Additional Resources (always include the heading; list only things you actually opened, or write "None"). Do not invent documentation URLs or issue numbers. Offer to apply the fix to the user's real files; don't apply it unasked.

## Files

* `references/bug-minimizer.md`: the debugging prompt and output format.
* `scripts/verify_repro.sh`: runs a repro against buggy and fixed copies and reports VERIFIED / NOT VERIFIED.

The upstream prompt lives at https://jeffbailey.us/prompts/; the bundled copy is the source of truth.

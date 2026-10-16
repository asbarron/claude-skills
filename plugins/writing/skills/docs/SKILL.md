---
name: docs
description: "Write or revise technical documentation (README, API reference, docstrings, how-to, tutorial, explanation, ADR, changelog, runbook) in Google developer style with Diátaxis structure, lint, and a reviewer gate. Use when asked to document code or a project."
argument-hint: "[type] [path] [--profile reader] [--no-gate] [--lang py|go|ts|rs]"
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, Bash(python3 -I *), Bash(python3 -m *), Bash(vale *), Bash(markdownlint-cli2 *), Bash(ls *), Bash(cat *)
---

Write documentation that a reader can act on without opening the code. The reader is a developer who has not seen this project. Every sentence either helps them do something or tells them a fact they can check.

## Non-negotiables

Read `${CLAUDE_SKILL_DIR}/../../shared/voice.md` once; it is the house style. Then read the active rows of `${CLAUDE_SKILL_DIR}/references/rules.md`. The short version:

- Second person, active voice, present tense, sentence-case headings.
- One Diátaxis quadrant per document.
- A runnable example before any explanation.
- Reserved example data only.
- No filler words.
- No claim you did not verify in the repository.

Work through the following sections in order.

## Arguments

`$ARGUMENTS` can carry a doc type, a path, and flags. Types: `readme`, `api`, `docstrings`, `how-to`, `tutorial`, `explanation`, `adr`, `changelog`, `runbook`. Flags: `--profile reader` adds `${CLAUDE_SKILL_DIR}/../../shared/reader-profile.md` on top of the house style; `--no-gate` skips the reviewer; `--lang py|go|ts|rs` picks the docstring convention. When the type is missing, infer it from the request. A bare "write docs" for a repository without a README means `readme`.

## Classify

Decide three things before reading much code, and write them down in one line each:

- **Audience and task.** Onboarding (install and first run), using (call the API or CLI), maintaining (change the code), or operating (run it in production). A README serves onboarding and using; an ADR serves maintaining.
- **Diátaxis quadrant.** Tutorial (learning by doing), how-to (reach a goal), reference (look up facts), explanation (understand why). One per document. If a request needs two, write two files and link them.
- **Doc type and sections.** Pick the section list for the type (README: name and one-line purpose, install, usage, then detail, then license).

Ask the user one question only if the quadrant is genuinely ambiguous. In headless mode, never ask; pick the default and say so in the summary.

## Gather facts

Read the code that defines the public surface before writing anything. Start with the manifest (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`), then entry points and console scripts, the top-level module, the CLI parser, and the tests. Run `--help` or `--version` through the real entry point when the project has one.

Write a facts list as you go, each fact with a `file:line` reference. Install command, entry-point name, subcommands and flags, public symbols and their failure modes, version, license. Every claim in the doc must trace to a fact on this list. If you cannot establish a fact, leave it out or mark it; never invent it.

## Plan

Write a five-line outline: the sections in order and what each must contain, drawn from the facts list. Check it against the section list for the type and the active rules. Fix the outline before writing; it is cheaper than fixing prose.

## Write

Write section by section, each from the facts list. The first paragraph says what the thing does and who it is for, in plain words. In every section that shows how to do something, put the example first and the prose after it. Each `##` section must stand on its own: name the tool or symbol in the text, not "it" or "this". Use the reserved example data (example.com, 192.0.2.x, names like Alex and Dana), placeholders in `UPPER_SNAKE_CASE`, and show expected output after commands when it adds information.

## Which reference to read

Read only what the section you are writing needs; the references are dense. Paths are relative to `${CLAUDE_SKILL_DIR}/references/`.

| When writing | Read first | Also |
|---|---|---|
| Any doc | `rules.md` (active rows) | `../../shared/voice.md` |
| README | `doc-types.md#readme` | `code-samples.md` |
| API reference, docstrings, doc comments | `docstrings.md` (your language) | `doc-types.md#api-reference` |
| How-to, tutorial, explanation | `diataxis.md` (the quadrant) | `doc-types.md` (the type) |
| ADR, changelog, runbook | `doc-types.md` (the type) | `google-style.md#procedures` for runbooks |
| Anything with UI steps, tables, images, links, or notices | `google-style.md` (the section) | |
| A doc with `--profile reader` | `../../shared/reader-profile.md` | |
| Two guides disagree | `conflicts.md` | |
| Prose that reads long or formal | `plain-language.md` | |

`doc-types.json` next to these files is the machine-readable section list that `structure.py` enforces; the prose templates in `doc-types.md` match it.

## Lint and fix

Run `bash ${CLAUDE_SKILL_DIR}/scripts/lint-docs.sh FILES` on every file you wrote and fix error-level findings. For source files you documented, run `python3 -I ${CLAUDE_SKILL_DIR}/scripts/docstring_coverage.py PATHS` and fix every `missing` and `mismatched` entry. Make at most two lint-fix passes; after that, list what remains in the summary. The linter reports missing tools instead of failing; if it says Vale is absent, keep going.

## Verify claims

Grep for every symbol, flag, and path the doc names. Run only safe commands to confirm behavior: `--help`, `--version`, `--dry-run`, `python3 -c`, or the project's own test runner. Anything that installs, deletes, writes outside a temporary directory, or uses the network is verified by reading, not by running, and gets `<!-- unverified -->` after the claim.

## Gate

Unless `--no-gate` is set and `${CLAUDE_SKILL_DIR}/../../agents/docs-reviewer.md` exists, launch the `writing:docs-reviewer` agent with the doc path, the facts list, and the doc type. Fix blockers and re-review once. If it still blocks, report the blockers; do not loop.

## Summary

End with: files written, type and quadrant, lint counts, reviewer verdict (or "no gate"), and any unverified claims. Stop when the gate passes, after one re-review, or when a needed fact cannot be established.

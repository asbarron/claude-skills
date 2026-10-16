---
name: writing
description: "General technical writing: commit messages, PR descriptions, release notes, issue text, and prose about code. Routes documentation requests (README, API reference, docstrings, how-to, ADR, changelog) to /writing:docs."
argument-hint: "[what to write]"
---

Write for a developer who will act on the text. Apply `${CLAUDE_SKILL_DIR}/../../shared/voice.md` to everything; it is short and it is the whole house style.

## Route first

Documentation artifacts go to the docs skill. That means a README, API reference, docstrings or doc comments, a how-to, tutorial, explanation, ADR, changelog, runbook, or "write docs for this". Invoke `/writing:docs $ARGUMENTS` with the same arguments and stop.

Everything else stays here: commit messages, PR titles and descriptions, release notes, issue reports, code comments, and messages about code.

## Commit messages

Conventional Commits: `type(scope): description`, then an optional body and footers. Types: feat, fix, build, chore, ci, docs, style, refactor, perf, test, revert. A `!` before the colon or a `BREAKING CHANGE:` footer marks a breaking change. The description is imperative, lowercase, no trailing period, under 72 characters. The body says why, not what; the diff already says what.

Example: `fix(parser): handle empty arrays in nested objects`.

## PR descriptions

Three parts, in order: what changed (one sentence), why (one short paragraph), and how to verify (numbered commands with expected results). Link the issue. No narrative of the work; reviewers read the diff.

## Release notes and changelogs

Group by Added, Changed, Deprecated, Removed, Fixed, Security. One bullet per user-visible change, written for the user, not the committer. ISO dates. For a full `CHANGELOG.md` use `/writing:docs changelog`.

## Issue reports

Title states the symptom. Body: what you did, what you expected, what happened, versions, smallest reproduction. Logs in fenced blocks; no screenshots of text.

## Code comments

Explain why, not what. Comments are prose: capitalized, punctuated. `TODO: BUG_LINK: explanation`, never a person's name. If the comment restates the line, delete it.

## Before you finish

Read the text once as the recipient. Cut every word that does not change what they will do. Check the voice rules; the common slips are `please`, `simply`, `currently`, `let's`, and passive voice that hides the actor.

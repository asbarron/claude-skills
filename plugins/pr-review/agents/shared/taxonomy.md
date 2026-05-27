---
name: taxonomy
description: "Shared comment taxonomy: 5 labels, blocking rules, quantitative limits, and tone rules."
---

# Comment Taxonomy

Shared taxonomy and rules. Every reviewer and lens agent loads this file.

---

## Labels

Comments that flag something start with one of these labels:

| Label | Meaning | Blocking? |
|-------|---------|-----------|
| `issue:` | Correctness, security, data loss, real bugs | Yes — must fix |
| `suggestion:` | Take-it-or-leave-it improvement | No |
| `question:` | Genuine confusion, not a criticism | No |
| `nitpick:` | Minor style or naming, author's call | No |

Praise comments do **not** carry a `praise:` prefix. Just write the praise directly (e.g., ":+1: nice guard on the empty-input case"). Adding a `praise:` header is bureaucratic and breaks the flow.

Append `[non-blocking]` to an `issue:` that's important but not merge-blocking:
> `issue [non-blocking]: this will cause a memory leak under sustained load — consider X`

---

## Rules

- Every `issue:` MUST include a suggested fix or a clear direction. No complaints without a path forward.
- No style comments if a linter or formatter is already configured in the repo — let the tool handle it.
- Max 2 `nitpick:` comments per PR. Nitpick fatigue is real.
- Max 1 DRY/design `issue:` per PR unless there is a clear correctness or security impact from multiple items.
- For algorithmic PRs, prioritize one high-confidence edge-case/correctness comment over many speculative notes.
- Use praise sparingly so it means something. No `praise:` header — write the praise directly. Skip if the only thing you'd say is generic ("nice work", "looks good").
- Tone: collaborative. "Consider X because Y. Thoughts?" — not "you should X" or "why didn't you X".
- No passive-aggressive hedging ("this is just my opinion but..."). Say it plainly or don't say it.
- Do not repeat issues already raised in existing review comments.
- When there are no blocking issues and all prior feedback is resolved or not applicable, write the overall verdict as a single short approving line — "LGTM", "ship it", or similar modern SWE language. Skip the formal summary.

---

## Conciseness (hard rule)

Reviewers waste author time with padding. Every comment must obey:

- **One or two sentences max.** If you need more, the comment is doing two things — split it or cut it.
- **No preamble.** Skip "I noticed that…", "It looks like…", "Just wanted to flag…". State the thing.
- **No restating the diff.** The author wrote the code; don't narrate it back to them.
- **No section headers per comment.** Don't bold the label or wrap it in a heading. Inline `label:` prefix is enough.
- **Cut every word that doesn't change the meaning.** "deliberate, or did X force this?" beats "Was this a deliberate design choice, or did X end up forcing the change?"

If a comment can't survive being cut in half, it probably shouldn't be posted.

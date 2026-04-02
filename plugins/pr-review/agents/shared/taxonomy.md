---
name: taxonomy
description: "Shared comment taxonomy: 5 labels, blocking rules, quantitative limits, and tone rules."
---

# Comment Taxonomy

Shared taxonomy and rules. Every reviewer and lens agent loads this file.

---

## Labels

Every comment starts with one of these labels:

| Label | Meaning | Blocking? |
|-------|---------|-----------|
| `issue:` | Correctness, security, data loss, real bugs | Yes — must fix |
| `suggestion:` | Take-it-or-leave-it improvement | No |
| `question:` | Genuine confusion, not a criticism | No |
| `nitpick:` | Minor style or naming, author's call | No |
| `praise:` | Something done well | N/A |

Append `[non-blocking]` to an `issue:` that's important but not merge-blocking:
> `issue [non-blocking]: this will cause a memory leak under sustained load — consider X`

---

## Rules

- Every `issue:` MUST include a suggested fix or a clear direction. No complaints without a path forward.
- No style comments if a linter or formatter is already configured in the repo — let the tool handle it.
- Max 2 `nitpick:` comments per PR. Nitpick fatigue is real.
- Max 1 DRY/design `issue:` per PR unless there is a clear correctness or security impact from multiple items.
- For algorithmic PRs, prioritize one high-confidence edge-case/correctness comment over many speculative notes.
- Use `praise:` when there's genuinely good work. Use it sparingly so it means something.
- Tone: collaborative. "Consider X because Y. Thoughts?" — not "you should X" or "why didn't you X".
- No passive-aggressive hedging ("this is just my opinion but..."). Say it plainly or don't say it.
- Do not repeat issues already raised in existing review comments.
- When there are no blocking issues and all prior feedback is resolved or not applicable, write the overall verdict as a single short approving line — "LGTM", "ship it", or similar modern SWE language. Skip the formal summary.

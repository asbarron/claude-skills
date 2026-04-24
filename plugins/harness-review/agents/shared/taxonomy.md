---
name: taxonomy
description: "Harness review taxonomy: 6 labels, blocking rules, quantitative limits."
---

# Finding Taxonomy

Shared taxonomy and rules. Every lens agent loads this file.

---

## Labels

Every finding starts with one of these labels:

| Label | Meaning | Blocking? |
|---|---|---|
| `migrate:` | This CLAUDE.md instruction should be a hook (fully or partially enforceable) | Yes |
| `gap:` | Missing configuration that matters for this project's stack and maturity | Yes |
| `issue:` | Incorrect configuration, anti-pattern, or will cause problems | Yes |
| `bloat:` | Remove — self-evident, aspirational, or duplicated; adds noise without changing behavior | No |
| `suggestion:` | Take-it-or-leave-it improvement | No |
| `strength:` | Something the harness does well — preserve | N/A |

---

## Rules

- Every `migrate:` MUST include the target hook event, handler type, and a concrete config snippet or direction. No "this should be a hook" without saying which hook.
- Every `gap:` MUST include what to add and where. No complaints without a path forward.
- Every `issue:` MUST include the specific anti-pattern and the fix direction.
- `bloat:` findings MUST explain why the instruction doesn't change behavior (e.g., "the model already does this by default" or "no measurable effect on compliance").
- Max 3 `bloat:` findings per review. Bloat fatigue is real — focus on the worst offenders.
- Max 1 `strength:` per review. Use it when there's genuinely good configuration. Overuse dilutes meaning.
- Tone: constructive. "This instruction could be enforced as a hook" — not "You put this in the wrong place."
- Do not flag CLAUDE.md formatting or markdown structure — focus on the engineering content.

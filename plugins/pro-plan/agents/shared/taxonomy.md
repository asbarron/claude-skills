---
name: taxonomy
description: "Plan review taxonomy: 6 labels, blocking rules, quantitative limits."
---

# Finding Taxonomy

Shared taxonomy and rules. Every lens agent and the synthesizer loads this file.

---

## Labels

Every finding starts with one of these labels:

| Label | Meaning | Blocking? |
|---|---|---|
| `gap:` | Something missing that should exist before implementation begins | Yes |
| `risk:` | A decision that carries risk — needs explicit acknowledgment and mitigation | Yes |
| `issue:` | Incorrect or contradicts best practices for the detected stack | Yes |
| `suggestion:` | Take-it-or-leave-it improvement to structure or approach | No |
| `question:` | Genuine ambiguity needing the author's input to resolve | Informational |
| `strength:` | Something the plan does well — preserve during revision | N/A |

---

## Rules

- Every `gap:` and `issue:` MUST include a concrete fix direction. No complaints without a path forward.
- Every `risk:` MUST include the specific failure mode and a mitigation direction.
- `question:` findings become the basis for user Q&A — phrase them as clear, answerable questions.
- Max 2 `suggestion:` findings per plan section. Suggestion fatigue is real.
- Max 1 `strength:` per review. Use it when there's genuinely good design. Overuse dilutes meaning.
- Tone: constructive. "This phase is missing X" — not "You forgot X" or "Why didn't you include X".
- No findings about the plan's formatting, writing style, or markdown structure — focus on the engineering content.
- Do not flag something the plan explicitly addresses in a different section.

---
name: calibration
description: "Harness review calibration: maturity classification, verify-before-flagging, enforcement research."
---

# Harness Review Calibration

Shared calibration rules. Every lens agent loads this file.

---

## Harness maturity

The harness maturity classification is provided to you by the skill — use it as-is. Do not re-classify. This determines how strict your feedback should be.

| Classification | Posture |
|---|---|
| **Bare** | Flag only critical gaps (missing test/lint commands). Don't demand hooks or skills from a project that hasn't started configuring. |
| **Basic** | Full review. Apply all lenses normally. Suggest enforcement migration for clear candidates. |
| **Mature** | Hold to a high bar. Flag subtle anti-patterns, bloat, redundancy between hooks and CLAUDE.md, and missed optimization opportunities. |

---

## Verify-before-flagging

Before raising a finding:

1. **Check the full config.** The issue may be addressed in a different file — a hook may cover what looks like a missing CLAUDE.md instruction, or a skill may handle what looks like CLAUDE.md bloat.
2. **Check installed plugins.** A plugin may already provide the missing functionality (e.g., a code-intelligence plugin covers linting hooks).
3. **Check for judgment requirements.** Do not flag a CLAUDE.md instruction as "should be a hook" if it genuinely requires contextual reasoning the model must perform. The 26% of rules that need judgment (persona, no-hallucination, procedure-following, common-sense) belong in CLAUDE.md.

---

## Enforcement research

When classifying CLAUDE.md instructions as enforceable vs. judgment:

- **Fully enforceable**: the instruction describes a deterministic rule with a verifiable outcome. A shell command or schema check can confirm compliance. Map to a specific hook event and handler type.
- **Partially enforceable**: the instruction has a deterministic component (a prompt hook can evaluate it) but also requires contextual judgment. Recommend keeping in CLAUDE.md *and* adding a prompt hook for the verifiable part.
- **Judgment only**: the instruction requires reasoning about context, tradeoffs, or style that cannot be reduced to a yes/no check. Keep in CLAUDE.md.

When uncertain, default to "judgment only." A false `migrate:` finding that removes a judgment call from CLAUDE.md is worse than a missed enforcement opportunity.

---
name: calibration
description: "Plan review calibration: maturity classification, verify-before-flagging, research discipline."
---

# Plan Review Calibration

Shared calibration rules. Every lens agent loads this file.

---

## Plan maturity

Classify the plan before reviewing. This determines how strict your feedback should be.

| Classification | Signals | Posture |
|---|---|---|
| **Sketch** | Under 50 lines, bullet points only, no phase structure | Flag only critical gaps. Don't demand rigor from a napkin drawing. |
| **Standard** | 50–200 lines, has sections/phases, mentions specific technologies | Full review. Apply all lenses normally. |
| **RFC/TDD** | 200+ lines, formal sections (motivation, alternatives, rollback), detailed steps | Hold to a high bar. Flag subtle risks and dependency issues. |

---

## Verify-before-flagging

Before raising a finding:

1. **Check the full plan.** The issue may be addressed in a different section or phase. Read the whole document before flagging something as missing.
2. **Check CONTRIBUTING.md context.** If the plan follows a convention documented in CONTRIBUTING.md, don't flag it.
3. **Check resource backing.** Only flag best-practice violations you can tie to a specific authoritative source (book, official docs, CONTRIBUTING.md). "I think this is wrong" is not enough.

---

## Research discipline

When using web-searched resources and CONTRIBUTING.md as sources of truth:

1. Official documentation (language specs, framework docs)
2. Books by the language/framework authors
3. O'Reilly books and publications
4. Academic research and conference papers
5. Widely-cited community guides

- CONTRIBUTING.md is authoritative for this specific repo — it overrides general best practices when they conflict
- If two authoritative sources disagree, note the disagreement instead of picking a side
- Never invent a best practice. If you can't cite it, don't flag it.

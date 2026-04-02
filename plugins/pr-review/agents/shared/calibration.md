---
name: calibration
description: "Shared calibration rules: repo maturity, tech-stack, edge-case rigor, research discipline, DRY policy, and verify-before-flagging."
---

# Calibration

Shared review calibration rules. Every reviewer and lens agent loads this file.

---

## Calibrate to repo maturity first

Before reviewing anything, classify the repo based on what the skill passed you:

**Greenfield** (new repo, few commits, sparse or missing docs/tests/CI):
- Only flag correctness bugs and security issues
- Do NOT suggest adding tests, CI, linting, docs, or refactoring architecture
- Do NOT suggest "consider extracting this into a utility" or similar
- The repo isn't there yet — don't punish it for that

**Growing** (some structure, partial coverage, active development):
- Light suggestions are OK, but lean toward `question:` and `suggestion:` over `issue:`
- Avoid scope creep — don't redesign things that are working

**Mature** (established patterns, CI, test suite, clear conventions):
- Full review is appropriate — architecture, patterns, edge cases, test coverage gaps all fair game

**When in doubt, be more conservative.** One focused `issue:` beats five scattered `suggestion:`s.

---

## Calibrate to tech stack

After classifying maturity, note the repo's primary languages and frameworks from the context the skill provided. Recall the most relevant best-practices references for those technologies — for example:

- **Go**: _Effective Go_, _The Go Programming Language_, Go Code Review Comments, `golang.org/doc/` style guide
- **Python**: PEP 8, PEP 20, _Fluent Python_, mypy docs
- **TypeScript / JavaScript**: official TypeScript handbook, _JavaScript: The Good Parts_, React docs (hooks rules, etc.)
- **Rust**: _The Rust Book_ (ownership, lifetimes), Clippy lints
- **Java / Kotlin**: _Effective Java_, Kotlin coding conventions
- **Systems / infra**: _Designing Data-Intensive Applications_, 12-Factor App

Apply the idioms and conventions from those references when reviewing. Flag code that violates well-known best practices for the stack, but only at `suggestion:` level unless it's a correctness bug. Keep the reference list internal — do not post it in the review body or inline comments.

---

## Algorithm and edge-case rigor

When a PR includes algorithmic logic (search/sort/DP/graphs/math/parsing/state machines), explicitly review for edge cases before commenting.

Minimum edge-case checklist:

- Empty/null input, single-element input, and minimal valid input
- Duplicates, ties, equal keys, and unstable ordering assumptions
- Off-by-one boundaries, inclusive/exclusive range mistakes
- Negative values, zero, overflow/underflow, precision/rounding behavior
- Worst-case complexity and memory growth under large inputs
- Invalid or adversarial inputs and failure-mode behavior

If a likely edge-case bug exists, raise `issue:` with:
1) the concrete failing scenario, and
2) the smallest fix direction (plus test shape if tests exist in repo maturity level).

---

## Research discipline for uncertain domains

If confidence is low or the domain is specialized, do lightweight research before finalizing feedback. Prioritize in this order:

1. Official stack/framework docs and language references
2. Project's existing patterns and tests (including E2E tests where present)
3. Reputable algorithm/data-structure references (standard textbooks, language-specific guides)
4. Mathematical references (including arXiv when relevant for correctness claims)
5. Comparable problem patterns (e.g., LeetCode-style canonical approaches) as secondary sanity checks

Do not cite sources in the posted review unless directly asked. Use research to improve correctness and reduce false positives, not to increase comment volume.

---

## DRY and design-flaw calibration

Treat DRY feedback as **high-signal only**. Do not ask for refactors just because code is repetitive.

Escalate DRY/design concerns only when repetition or structure is likely to cause real harm, such as:

- Divergent business rules implemented in multiple places (high drift risk)
- Duplicate validation/security/authorization logic that can become inconsistent
- Repeated complex logic that already differs subtly and can cause bugs
- Cross-module coupling or layering violations that make safe changes difficult
- "God" modules/functions where responsibilities are mixed and defects are harder to isolate

Do **not** flag:

- Small local duplication that is obvious and low-risk
- Cosmetic helper extraction ideas with no reliability or maintainability benefit
- Architecture rewrites that exceed the PR's scope

When you flag a DRY/design issue, explain the concrete failure mode ("what breaks if this drifts") and propose the smallest practical fix for this PR.

---

## Verify before flagging

Before raising any finding, confirm your assumption against the PR description, existing code, and existing review comments. Do not flag an issue based on a guess about how the system works — read the relevant code first.

If the PR description or a linked ticket explicitly explains a decision you were about to question, do not flag it. If existing review comments already cover the same point, do not repeat it.

A false positive that wastes the author's time is worse than a missed nit.

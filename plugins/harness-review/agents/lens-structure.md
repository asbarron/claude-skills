---
name: lens-structure
description: "Structure lens: CLAUDE.md length, organization, duplication, skill placement."
---

# Structure Lens

You are reviewing a Claude Code harness for structural problems — bloated CLAUDE.md files, poor organization, duplicated content, and instructions that belong in skills instead.

## Foundations

Read and apply before reviewing:
- `shared/calibration.md` — especially harness maturity (a basic harness won't have @imports yet) and verify-before-flagging
- `shared/taxonomy.md` — labels, rules, limits
- `shared/style.md` — voice and tone

## Research basis

Empirical findings that inform this lens:

- LLM instruction compliance drops from **94% at 1 instruction to 21% at 10 instructions** — simultaneous compliance is the bottleneck, not individual difficulty (arxiv 2509.21051)
- Reasoning performance degrades at around **3,000 tokens** of instruction input (MLOps Community prompt bloat study)
- Information in the **middle of context receives least attention** — CLAUDE.md instructions buried mid-file are effectively invisible (Lost in the Middle, arxiv 2307.03172)
- Semantically related distractors are **more damaging** than unrelated noise — a CLAUDE.md line about code style competes directly with code style decisions during edits

## Focus

### Length and density

- Count total lines and estimate token cost across all CLAUDE.md files loaded per session (root + parents + home)
- Flag as `bloat:` if total exceeds ~80 lines or ~2,000 tokens — every line competes for attention with every other line
- For each line, apply Anthropic's test: "Would removing this cause Claude to make mistakes?" If the answer is no, flag as `bloat:`

### Organization

- Instructions should be grouped by topic under clear headings
- High-priority instructions (test commands, critical constraints) should be near the top — the primacy effect means early instructions get strongest compliance
- Check for `@import` usage to reference external files (README, package.json) instead of duplicating their content

### Duplication

- Check for duplicated instructions across CLAUDE.md files (root, parent directories, home `~/.claude/CLAUDE.md`)
- Check for CLAUDE.md instructions that duplicate what's already in hook configuration
- Check for instructions that restate framework/language defaults the model already knows

### Skill placement

- Domain-specific instructions that aren't relevant every session should be skills, not CLAUDE.md
- Flag CLAUDE.md sections longer than ~10 lines on a single topic — these are candidates for a skill file that loads on demand
- Anthropic's guidance: "CLAUDE.md is loaded every session, so only include things that apply broadly. For domain knowledge or workflows that are only relevant sometimes, use skills instead."

## Out of scope

Do NOT flag:
- Whether instructions should be hooks (the enforcement lens handles that)
- Missing configuration (the completeness lens handles that)
- Best-practice violations in instruction content (the best-practices lens handles that)
- CLAUDE.md formatting preferences (markdown style, heading levels)

## Output

For each finding, return:
- **file**: which CLAUDE.md file and the section/lines affected
- **label**: `bloat:`, `suggestion:`, or `strength:` (from taxonomy)
- **body**: the structural problem and how to fix it (move to skill, consolidate, reorder, delete)
- **severity**: Low / Medium / High / Critical
- **reasoning**: the concrete impact (e.g., "this 15-line section about deployment runs every session but is only relevant during releases — extracting to a skill saves ~400 tokens per session")
- **lens**: `structure`

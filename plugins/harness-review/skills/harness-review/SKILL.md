---
name: harness-review
description: "Audit your Claude Code harness: research-backed enforcement mapping, bloat detection, completeness checks, and best-practices review."
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Agent
argument-hint: "[--dry-run]"
---

Review the Claude Code harness in the current project. Scans CLAUDE.md files, hooks, skills, agents, and settings, then runs a calibrated multi-lens review.

---

## Step 1 — Parse flags

Parse flags from $ARGUMENTS:
- `--dry-run` → print findings to terminal (default behavior; reserved for future integration with automated fixups)

---

## Step 2 — Scan the harness

Gather all configuration files. Run these commands:

### 2a — Find all CLAUDE.md files

```bash
# Project root and parents
ls CLAUDE.md CLAUDE.local.md 2>/dev/null
ls ../CLAUDE.md 2>/dev/null

# Home-level
ls ~/.claude/CLAUDE.md 2>/dev/null
```

Read each file that exists. Track which files are loaded per session (root + all parents + home).

### 2b — Scan .claude/ directory

```bash
ls -la .claude/ 2>/dev/null
ls .claude/settings.json .claude/settings.local.json 2>/dev/null
```

If `.claude/settings.json` exists, read it. Extract the `hooks` object if present. If `.claude/settings.local.json` exists, read it too. Merge its `hooks` with `settings.json` hooks — local settings override project settings for matching hook events. Pass the merged hooks to all agents in Step 6.

### 2c — List skills, agents, and plugins

```bash
# Local skills and agents
ls -R .claude/skills/ 2>/dev/null
ls -R .claude/agents/ 2>/dev/null

# Installed plugins
ls -d .claude/plugins/*/ 2>/dev/null
```

For each skill found, read its SKILL.md frontmatter (first 10 lines) to understand scope.

---

## Step 3 — Detect tech stack

Scan the project for stack signals:

```bash
ls package.json tsconfig.json go.mod go.sum Cargo.toml pyproject.toml requirements.txt Gemfile pom.xml build.gradle docker-compose.yml Dockerfile Makefile 2>/dev/null
```

Also scan CLAUDE.md content for technology mentions. Combine into a deduplicated tech stack list.

---

## Step 4 — Classify harness maturity

Based on what was found in Step 2, classify the harness:

| Classification | Condition |
|---|---|
| **Bare** | No CLAUDE.md, or only a default `/init` file with no customization |
| **Basic** | CLAUDE.md exists with project-specific content; fewer than 3 hooks or no hooks |
| **Mature** | CLAUDE.md plus 3+ hooks, or active skills/agents/plugins in use |

This classification is passed to all agents and controls review strictness.

---

## Step 5 — Load shared foundations

Read the three shared agent files and apply them for the rest of this skill:

- `${CLAUDE_SKILL_DIR}/../../agents/shared/calibration.md`
- `${CLAUDE_SKILL_DIR}/../../agents/shared/taxonomy.md`
- `${CLAUDE_SKILL_DIR}/../../agents/shared/style.md`

---

## Step 6 — Launch review lenses in parallel

Read the four lens agent files:
- `${CLAUDE_SKILL_DIR}/../../agents/lens-enforcement.md`
- `${CLAUDE_SKILL_DIR}/../../agents/lens-completeness.md`
- `${CLAUDE_SKILL_DIR}/../../agents/lens-structure.md`
- `${CLAUDE_SKILL_DIR}/../../agents/lens-best-practices.md`

Launch **4 Agent calls in parallel**. Each agent receives:
- All CLAUDE.md file contents (with file paths labeled)
- Hooks configuration (the merged `hooks` from settings.json and settings.local.json, or "no hooks configured")
- List of skills, agents, and plugins found (with SKILL.md frontmatter summaries)
- Tech stack list
- Harness maturity classification
- The shared foundations content (pass content, not file paths)
- The lens-specific agent instructions

Each lens produces structured findings: `{file, label, body, severity, reasoning, lens}`. Lenses must be independent — do not let one lens's output influence another.

---

## Step 7 — Synthesize findings

Collect all findings from all 4 lenses. Apply three passes:

### 7a — Deduplicate

Group findings by config file and instruction. Within each group:

- If 2+ lenses flagged the same instruction, merge into one finding. Keep the strongest reasoning from each. Mark as **consensus**.
- If findings from different lenses address different aspects of the same file (e.g., enforcement flags a line for migration, structure flags the same file for length), keep them separate — they are not duplicates.

### 7b — Evaluate signals

**Promote signals** (each promotes one severity tier, max Critical):

| Signal | How to detect |
|---|---|
| **Consensus** (2+ lenses) | Marked in 7a |
| **Source-backed** | The finding cites a specific source (Anthropic docs, research paper) |
| **Failure mode described** | The finding names a concrete way the harness will fail |

**Drop signals** (any one drops the finding):

| Signal | How to detect |
|---|---|
| **Addressed elsewhere** | A hook, skill, or plugin already covers the gap |
| **Cosmetic** | About CLAUDE.md formatting, not engineering content |
| **Speculative** | The reasoning shows the agent guessed without evidence |

### 7c — Assign tiers

Start from self-reported severity. Apply promotions (cap at Critical). Apply drops.

| Tier | Meaning |
|---|---|
| **Critical** | Certain to cause problems — consensus or concrete failure mode with evidence |
| **High** | Will be hit in practice — source-backed, single-lens but well-reasoned |
| **Medium** | Real issue — single-lens, reasonable, lower impact |
| **Dropped** | Failed a drop signal or below Medium |

Only **Medium and above** appear in the final report.

---

## Step 8 — Print report

Print the structured review to the terminal:

```
## Harness Review

**Tech stack:** [detected technologies]
**Harness maturity:** [Bare/Basic/Mature]
**Files scanned:** [list of CLAUDE.md files, settings files, skills, agents]

---

### Critical
> **[label]:** [body]
> *File: [config file]* | *Lens: [source lens(es)]*
> **Fix:** [direction or hook config snippet]

### High
> ...

### Medium
> ...

---

Stats: [N] raw → [N] dedup → [N] posted ([breakdown by tier])
Enforcement summary: [N] instructions reviewed → [N] enforceable → [N] judgment → [N] already hooked
```

---

## Step 9 — Summary

Print a one-line summary: number of findings by tier, enforcement migration count, and overall harness health assessment (one sentence).

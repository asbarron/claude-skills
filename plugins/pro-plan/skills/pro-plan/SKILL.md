---
name: pro-plan
description: "Review and revise implementation plans: tech-stack-aware best practices, DRY checks, structure analysis, and completeness review."
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Agent, WebSearch, WebFetch, AskUserQuestion
argument-hint: "[path/to/plan.md] [--review-only] [--revise-only]"
---

Review an existing implementation plan or TDD specified in $ARGUMENTS. If no path is given, find the most recent plan from the Claude Code plans directory.

Supports two modes:
- **Default**: review the plan, ask the author questions about gaps, then produce a revised plan.
- **`--review-only`**: review and ask questions, but skip revision.
- **`--revise-only`**: restructure and improve the plan without running the review lenses.

---

## Step 1 — Parse arguments and flags

Extract from $ARGUMENTS:
- A file path (if provided). If no path, find the most recent plan:
  ```bash
  ls -t .claude/plans/*.md 2>/dev/null | head -1
  ```
  If no plans directory or no files found, error: "No plan file found. Pass a path: `/pro-plan path/to/plan.md`"
- `--review-only` → run Phase 1 only (review + questions, no revision)
- `--revise-only` → run Phase 2 only (revise without review)

If both flags are set, error: "`--review-only` and `--revise-only` are mutually exclusive."

---

## Step 2 — Read the plan

Read the plan file. If it doesn't exist, error with the path that was tried.

Count lines to classify plan size:
- **Short** (under 50 lines): rough sketch
- **Medium** (50–200 lines): standard detail
- **Long** (200+ lines): RFC/TDD-level

---

## Step 3 — Detect tech stack

Scan the plan text for technology mentions. Look for:
- **Languages**: Go, Python, TypeScript, JavaScript, Rust, Java, Kotlin, Ruby, C#, Swift, PHP, Elixir, Scala
- **Frameworks**: React, Next.js, Django, FastAPI, Spring, Rails, Express, Flask, Vue, Angular, Svelte, Laravel
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, DynamoDB, SQLite, Elasticsearch, Cassandra
- **Infrastructure**: Kubernetes, Docker, AWS, GCP, Azure, Terraform, Vercel, Cloudflare
- **Other**: GraphQL, gRPC, Kafka, RabbitMQ, Nginx, GitHub Actions

Also check the repo for stack signals:
```bash
ls package.json tsconfig.json go.mod go.sum Cargo.toml pyproject.toml requirements.txt Gemfile pom.xml build.gradle docker-compose.yml Dockerfile Makefile 2>/dev/null
```

Combine plan mentions and repo signals into a deduplicated tech stack list.

---

## Step 4 — Web-search for canonical resources

Load `${CLAUDE_SKILL_DIR}/../../agents/shared/resource-seeds.md` for seed queries.

For each detected technology (cap at **5 technologies**), run a WebSearch using the seed query from resource-seeds.md. If the technology isn't in the seeds list, construct a query: `"[technology] best practices official documentation"`.

Cap total web searches at **8**. For each search, briefly note the top authoritative result (title, source, key takeaway). Prefer official documentation domains.

Store the collected resource summaries — these are passed to all agents as source-of-truth context.

---

## Step 5 — Check for CONTRIBUTING.md

```bash
ls CONTRIBUTING.md contributing.md CONTRIBUTING 2>/dev/null
```

If found, read it. This is a source of truth alongside the web-searched resources — it informs all agents' judgment about what the plan should and shouldn't do.

---

## Step 6 — Load shared foundations

Read the shared agent files:
- `${CLAUDE_SKILL_DIR}/../../agents/shared/calibration.md`
- `${CLAUDE_SKILL_DIR}/../../agents/shared/taxonomy.md`
- `${CLAUDE_SKILL_DIR}/../../agents/shared/style.md`

Apply throughout the remaining steps.

---

## Step 7 — Branch by mode

**If `--revise-only`:** Skip to Step 10.

**Otherwise:** Continue to Step 8 (review phase).

---

## Step 8 — Launch review lenses in parallel (Phase 1)

Read the four lens agent files:
- `${CLAUDE_SKILL_DIR}/../../agents/lens-dry.md`
- `${CLAUDE_SKILL_DIR}/../../agents/lens-best-practices.md`
- `${CLAUDE_SKILL_DIR}/../../agents/lens-structure.md`
- `${CLAUDE_SKILL_DIR}/../../agents/lens-completeness.md`

Launch **4 Agent calls in parallel**. Each agent receives:
- The full plan text
- Tech stack list
- Web-searched resource summaries
- CONTRIBUTING.md content (if it exists)
- Plan size classification
- The shared foundations content (pass content, not file paths)
- The lens-specific agent instructions

Each lens produces structured findings: `{section, label, body, severity, reasoning, lens}`. Lenses must be independent — do not let one lens's output influence another.

---

## Step 9 — Synthesize and present review

Load the review synthesizer:
- `${CLAUDE_SKILL_DIR}/../../agents/review-synthesizer.md`

Feed it all findings from all 4 lenses plus the original plan text.

### 9a — Print review

Print the structured review to the terminal:

```
## Plan Review: [filename]

**Tech stack:** [detected technologies]
**Plan scope:** [Short/Medium/Long] ([N] lines, [M] phases)
**Resources consulted:** [list of resources used]

---

### Critical
> **[label]:** [body]
> *Section: [plan section]* | *Lens: [source]*
> **[Fix/Add/Mitigate]:** [direction]

### High
> ...

### Medium
> ...

---
Stats: [N] raw → [N] dedup → [N] posted ([breakdown by tier])
```

### 9b — Ask user questions

If the synthesizer produced questions, present them via `AskUserQuestion`. Cap at 5 questions. Group by theme.

**If `--review-only`:** Stop here. Print a summary line and exit.

---

## Step 10 — Revise the plan (Phase 2)

Load the plan reviser:
- `${CLAUDE_SKILL_DIR}/../../agents/plan-reviser.md`

Feed it:
- The original plan text
- Review findings (if Phase 1 ran; empty list if `--revise-only`)
- User's answers to questions (if Phase 1 ran and questions were asked)
- Tech stack list and web-searched resource summaries
- CONTRIBUTING.md content (if it exists)
- Shared foundations content

---

## Step 11 — Write the revised plan

Derive the output path from the original plan path:
- `my-plan.md` → `my-plan-pro.md`
- `design.md` → `design-pro.md`

Write the revised plan to this new file in the same directory as the original.

---

## Step 12 — Summary

Print a one-line summary:
- Number of findings by tier (if Phase 1 ran)
- Where the revised plan was written (if Phase 2 ran)

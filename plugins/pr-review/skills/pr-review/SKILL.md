---
name: pr-review
description: "Review a GitHub PR: calibrated inline comments via gh CLI. Use --deep for multi-lens review with confidence scoring."
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Agent
argument-hint: "[PR number, #123, or URL] [--deep] [--dry-run] [--approve]"
---

Review the GitHub pull request specified in $ARGUMENTS. If no argument is given, detect the current PR via `gh pr view`.

Supports two modes:
- **Normal** (default): single-pass review using the reviewer persona — fast, focused, same as v1.
- **Deep** (`--deep`): four parallel review lenses + confidence scoring — slower, more thorough, filters false positives.

---

## Step 1 — Parse PR reference and flags

Extract a PR number from $ARGUMENTS. Accept: bare number (`42`), hash-prefixed (`#42`), or full GitHub URL. If empty, run `gh pr view --json number` to get the current branch's PR.

Parse flags from $ARGUMENTS:
- `--deep` → enable deep multi-lens mode
- `--dry-run` → print review to terminal without posting to GitHub
- `--approve` → post as an approval (if no blocking issues)

---

## Step 2 — Gather context

Before looking at the diff, understand the repo's current state. Run these commands:

```bash
gh repo view --json name,description,createdAt,pushedAt
git rev-list --count HEAD
ls -1
```

Also check whether these exist: `README.md`, test directories (`test/`, `tests/`, `spec/`, `__tests__/`), CI config (`.github/workflows/`, `.circleci/`, `.travis.yml`), linter config (`.eslintrc*`, `.rubocop*`, `pyproject.toml`, `ruff.toml`, `.golangci*`).

Use this to classify repo maturity — greenfield, growing, or mature — before forming any opinions.

### Detect tech stack

```bash
gh api repos/{owner}/{repo}/languages
```

Also check for framework and tooling signals by looking for: `package.json`, `tsconfig.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `requirements.txt`, `Gemfile`, `pom.xml`, `build.gradle`, `docker-compose.yml`, or similar. Note the primary languages, frameworks, and build tools.

From the detected stack, build a short internal list of the most relevant best-practices references for those technologies. This list is for calibration — do NOT include it in the review output.

### Fetch PR metadata

```bash
gh pr view $PR_NUMBER --json title,body,baseRefName,headRefName,headRefOid,author,additions,deletions,changedFiles
```

### Fetch existing review comments

```bash
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/comments
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/reviews
```

Treat existing feedback as first-class input.

- Build a deduped list of prior feedback items by grouping on `{path, original_position?, body}` (be forgiving about small text differences).
- For each prior item, decide: **resolved by this PR**, **still open**, or **not applicable** (e.g., file removed / refactor).
- If still open, propose the smallest concrete code change that would close it.
- Avoid re-posting the same comment text. Only add a new inline comment if you are adding *new* information.

### Fetch the diff

```bash
gh pr diff $PR_NUMBER
```

### Deep mode only — fetch git history for touched files

If `--deep` is set, gather git history for context. Cap at 10 files (by lines changed) and 10 commits per file:

```bash
# For each touched file (up to 10):
git log --oneline -10 -- <file>
git log --all --oneline --grep="revert" -- <file>
```

---

## Step 3 — Load shared foundations

Read the three shared agent files and apply them for the rest of this skill:

- `${CLAUDE_SKILL_DIR}/../../agents/shared/calibration.md` (repo maturity, tech-stack, edge-case rigor, research discipline, DRY policy, verify-before-flagging)
- `${CLAUDE_SKILL_DIR}/../../agents/shared/taxonomy.md` (comment labels, blocking rules, quantitative limits)
- `${CLAUDE_SKILL_DIR}/../../agents/shared/style.md` (voice, emoji, tone)

---

## Step 4 — Review (branches by mode)

### Normal mode (no `--deep`)

Load the reviewer persona:
- `${CLAUDE_SKILL_DIR}/../../agents/reviewer.md`

Using the persona and shared foundations, produce:
- An overall verdict (1–3 sentences) for the review body
- A short section: **"Follow-ups on existing feedback"**:
  - List the top prior feedback items (prefer the most recent review first).
  - Mark each as **resolved** / **still open** / **not applicable**.
  - For **still open** items, include a specific fix suggestion (what to change and where).
- Per-file inline comments with: file path, diff position (counted from the `@@` hunk header — NOT the actual line number), and comment body

Calibrate depth to repo maturity (see calibration.md). Keep comments high-signal and concise.

### Deep mode (`--deep`)

#### 4a — Launch four review lenses in parallel

Read the four lens agent files:
- `${CLAUDE_SKILL_DIR}/../../agents/lens-general.md`
- `${CLAUDE_SKILL_DIR}/../../agents/lens-security.md`
- `${CLAUDE_SKILL_DIR}/../../agents/lens-architecture.md`
- `${CLAUDE_SKILL_DIR}/../../agents/lens-git-history.md`

Launch **4 Agent calls in parallel**. Each agent receives:
- The full diff (if the diff exceeds 800 lines, batch files into groups of ~300 diff-lines and process each batch through all 4 lenses)
- Repo context: maturity classification, tech stack, directory structure
- PR metadata: title, body, author, base/head branches
- Existing review comments (the deduped list from Step 2)
- The shared foundations content (pre-loaded from Step 3 — pass the content, not file paths)
- The lens-specific agent instructions

Additionally, the **git-history lens** receives the git log output gathered in Step 2.

Each lens produces structured findings. Do not let findings from one lens influence another — they must be independent.

#### 4b — Collect findings

Collect all structured findings from all 4 agents into a single list. Each finding has: `{file, lines, label, body, severity, reasoning, lens}`.

#### 4c — Run confidence scoring

Load the confidence scorer:
- `${CLAUDE_SKILL_DIR}/../../agents/confidence-scorer.md`

Feed the scorer:
- All findings from all 4 lenses
- The PR description and metadata (for assumption verification)
- The existing review comments (for recurrence detection)

The scorer runs 3 passes:
1. **Deduplicate**: merge findings about the same code location from different lenses
2. **Evaluate signals**: apply promote/drop rules
3. **Assign tiers**: Critical → High → Medium → Dropped

Only Medium+ findings survive.

#### 4d — Format the report

Produce:
- An overall verdict (1–3 sentences) with severity summary
- A short section: **"Follow-ups on existing feedback"** (same format as normal mode)
- Findings ranked by tier (Critical → High → Medium), each with:
  - Tier badge and source lens(es)
  - File path and diff position
  - Taxonomy label and comment body
- Stats line: findings received → after dedup → after scoring

---

## Step 5 — Post or print

**`--dry-run` mode:** Print the review body and all inline comments to the terminal. Do not post to GitHub.

**Default and `--approve` mode:** Post via `gh api`:

```bash
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/reviews \
  --input - << 'EOF'
{
  "commit_id": "<HEAD_SHA>",
  "body": "<overall verdict>",
  "event": "<COMMENT|APPROVE|REQUEST_CHANGES>",
  "comments": [
    {"path": "file.js", "position": 4, "body": "issue: ..."}
  ]
}
EOF
```

Use `REQUEST_CHANGES` only if there are blocking `issue:` comments. Use `APPROVE` only if `--approve` was passed and there are no blocking issues. Otherwise use `COMMENT`.

In deep mode, only post Medium+ findings as inline comments.

---

## Step 6 — Summary

Print a one-line summary:

- **Normal mode**: how many issues, suggestions, nitpicks, and whether the review was posted or dry-run.
- **Deep mode**: same counts + lens breakdown (e.g., "general: 3, security: 1, architecture: 2") + tier counts (e.g., "1 Critical, 2 High, 4 Medium") + scoring stats (e.g., "12 raw → 9 deduped → 7 posted").

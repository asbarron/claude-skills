---
name: review-pr
description: Review a GitHub PR: reads repo context, runs a calibrated review using the reviewer persona, and posts inline comments + overall verdict to GitHub under your own account via gh CLI.
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "[PR number, #123, or URL]"
---

Review the GitHub pull request specified in $ARGUMENTS. If no argument is given, detect the current PR via `gh pr view`.

## Step 1 — Parse PR reference

Extract a PR number from $ARGUMENTS. Accept: bare number (`42`), hash-prefixed (`#42`), or full GitHub URL. If empty, run `gh pr view --json number` to get the current branch's PR.

## Step 2 — Read repo context

Before looking at the diff, understand the repo's current state:

```bash
gh repo view --json name,description,createdAt,pushedAt
git rev-list --count HEAD
ls -1
```

Also check whether these exist: `README.md`, test directories (`test/`, `tests/`, `spec/`, `__tests__/`), CI config (`.github/workflows/`, `.circleci/`, `.travis.yml`), linter config (`.eslintrc*`, `.rubocop*`, `pyproject.toml`, `ruff.toml`, `.golangci*`).

Use this to classify repo maturity — greenfield, growing, or mature — before forming any opinions.

## Step 3 — Fetch PR metadata

```bash
gh pr view $PR_NUMBER --json title,body,baseRefName,headRefName,headRefOid,author,additions,deletions,changedFiles
```

## Step 4 — Fetch existing review comments

```bash
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/comments
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/reviews
```

Treat existing feedback as first-class input.

- Build a deduped list of prior feedback items by grouping on `{path, original_position?, body}` (be forgiving about small text differences).
- For each prior item, decide: **resolved by this PR**, **still open**, or **not applicable** (e.g., file removed / refactor).
- If still open, propose the smallest concrete code change that would close it.
- Avoid re-posting the same comment text. Only add a new inline comment if you are adding *new* information (e.g., updated context, a clearer fix, or the issue got worse).

## Step 5 — Fetch the diff

```bash
gh pr diff $PR_NUMBER
```

## Step 6 — Load reviewer persona

Read `${CLAUDE_SKILL_DIR}/../../agents/reviewer.md` and apply that persona for the rest of this skill.

## Step 7 — Produce the review

Using the persona from reviewer.md, produce:
- An overall verdict (1–3 sentences) for the review body
- A short section: **“Follow-ups on existing feedback”**:
  - List the top prior feedback items (prefer the most recent review first).
  - Mark each as **resolved** / **still open** / **not applicable**.
  - For **still open** items, include a specific fix suggestion (what to change and where).
- Per-file inline comments with: file path, diff position (counted from the `@@` hunk header — NOT the actual line number), and comment body

Calibrate depth to repo maturity (see reviewer.md). When in doubt, say less.

## Step 8 — Post or print

**Default and `--approve` mode:** post via `gh api`:

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

**`--dry-run` mode:** print the review body and all inline comments to the terminal. Do not post to GitHub.

## Step 9 — Summary

Print a one-line summary: how many issues, suggestions, nitpicks, and whether the review was posted or dry-run.

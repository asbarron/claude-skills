# claude-skills

Claude Code plugins by Ava Barron.

---

## Plugins

### `pr-review`

A PR review skill for Claude Code. Run `/pr-review` in any repo with an open PR — Claude reads the diff, calibrates to the repo's current state, and posts inline comments + an overall verdict to GitHub **under your own account** via `gh` CLI.

Use `--deep` for a multi-lens review: four parallel agents (code quality, security, architecture, git history) with research-backed confidence scoring that filters false positives.

**Prerequisites:** `gh` CLI installed and authenticated (`gh auth login`).

#### Install

```bash
# In Claude Code, add this repo as a marketplace (once)
/plugin marketplace add asbarron/claude-skills

# Install the plugin
/plugin install pr-review@asbarron-skills
```

CLI equivalent:

```bash
claude plugin marketplace add --scope user asbarron/claude-skills
claude plugin install pr-review@asbarron-skills
```

#### Usage

```bash
# Review the PR for the current branch
/pr-review

# Review a specific PR
/pr-review 42
/pr-review #42
/pr-review https://github.com/owner/repo/pull/42

# Preview without posting
/pr-review 42 --dry-run

# Post as an approval (if no blocking issues)
/pr-review 42 --approve

# Deep multi-lens review with confidence scoring
/pr-review 42 --deep

# Deep review, preview only
/pr-review 42 --deep --dry-run
```

#### How it works

**Normal mode** (default):
1. Reads repo context (age, structure, test/CI presence) to calibrate review depth
2. Fetches the diff and existing comments
3. Applies the [reviewer persona](plugins/pr-review/agents/reviewer.md) — Conventional Comments taxonomy, max 2 nitpicks, no style comments if a linter is configured
4. Posts inline comments + overall verdict via `gh api` under your GitHub identity

**Deep mode** (`--deep`):
1. Same context gathering as normal mode, plus git history for touched files
2. Launches four review lenses in parallel:
   - **General** — correctness, edge cases, test coverage, efficiency
   - **Security** — exploitable vulnerabilities with concrete attack scenarios
   - **Architecture** — layer violations, pattern consistency, module boundaries
   - **Git History** — reverted fixes, removed guards, churn patterns
3. Runs a confidence scoring pass that deduplicates, verifies assumptions, and filters false positives
4. Posts only Medium+ severity findings (Critical, High, Medium)

The confidence scorer uses a research-backed approach: self-reported severity as the base estimator, multi-lens consensus for boost signals, and overconfidence correction to filter false positives. Total cost: 5 LLM calls (4 parallel lenses + 1 scorer).

#### Comment format

Each comment is prefixed with a label:

| Label | Meaning |
|-------|---------|
| `issue:` | Must fix — correctness, security, data loss |
| `suggestion:` | Take it or leave it |
| `question:` | Genuine confusion, not a criticism |
| `nitpick:` | Minor style/naming, your call |
| `praise:` | Something done well |

Add `[non-blocking]` to an `issue:` that matters but isn't merge-blocking.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT

# claude-skills

Claude Code plugins by Ava Barron.

---

## Plugins

### `pr-review`

A PR review skill for Claude Code. Run `/pr-review` in any repo with an open PR — Claude reads the diff, calibrates to the repo's current state, and posts inline comments + an overall verdict to GitHub **under your own account** via `gh` CLI.

**Prerequisites:** `gh` CLI installed and authenticated (`gh auth login`).

#### Install

```bash
# Add this repo as a marketplace (once)
claude plugin marketplace add --scope user https://github.com/asbarron/claude-skills

# Install the plugin by name
claude plugin install pr-review
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
```

#### How it works

1. Reads repo context (age, structure, test/CI presence) to calibrate review depth
2. Fetches the diff and existing comments
3. Applies the [reviewer persona](plugins/asbarron-pr-review/agents/reviewer.md) — Conventional Comments taxonomy, max 2 nitpicks, no style comments if a linter is configured
4. Posts inline comments + overall verdict via `gh api` under your GitHub identity

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

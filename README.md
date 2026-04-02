# claude-skills

Claude Code plugins by Ava Barron.

---

## Install

Add this marketplace once, then install any plugin:

```bash
# In Claude Code
/plugin marketplace add asbarron/claude-skills

# Install a plugin
/plugin install <plugin-name>@asbarron-skills
```

CLI equivalent:

```bash
claude plugin marketplace add --scope user asbarron/claude-skills
claude plugin install <plugin-name>@asbarron-skills
```

---

## Plugins

### `pr-review`

Calibrated PR reviews via Claude Code. Run `/pr-review` in any repo with an open PR — Claude reads the diff, calibrates to the repo's current state, and posts inline comments + an overall verdict to GitHub **under your own account** via `gh` CLI.

Use `--deep` for a multi-lens review: four parallel agents (code quality, security, architecture, git history) with research-backed confidence scoring that filters false positives.

**Prerequisites:** `gh` CLI installed and authenticated (`gh auth login`).

#### Usage

```bash
/pr-review                # current branch's PR
/pr-review 42             # specific PR (bare, #42, or full URL)
/pr-review 42 --dry-run   # preview without posting
/pr-review 42 --approve   # post as approval (if no blocking issues)
/pr-review 42 --deep      # multi-lens review with confidence scoring
/pr-review 42 --deep --dry-run
```

#### How it works

**Normal mode** (default):
1. Reads repo context (age, structure, test/CI presence) to calibrate review depth
2. Fetches the diff and existing comments
3. Applies the [reviewer persona](plugins/pr-review/agents/reviewer.md) — Conventional Comments taxonomy, max 2 nitpicks, no style comments if a linter is configured
4. Posts inline comments + overall verdict via `gh api` under your GitHub identity

**Deep mode** (`--deep`):
1. Same context gathering, plus git history for touched files
2. Launches four review lenses in parallel:
   - **General** — correctness, edge cases, test coverage, efficiency
   - **Security** — exploitable vulnerabilities with concrete attack scenarios
   - **Architecture** — layer violations, pattern consistency, module boundaries
   - **Git History** — reverted fixes, removed guards, churn patterns
3. Runs a confidence scoring pass that deduplicates, verifies assumptions, and filters false positives
4. Posts only Medium+ severity findings (Critical, High, Medium)

#### Labels

| Label | Meaning |
|-------|---------|
| `issue:` | Must fix — correctness, security, data loss |
| `suggestion:` | Take it or leave it |
| `question:` | Genuine confusion, not a criticism |
| `nitpick:` | Minor style/naming, your call |
| `praise:` | Something done well |

Append `[non-blocking]` to an `issue:` that matters but isn't merge-blocking.

---

### `pro-plan`

Plan and TDD review via Claude Code. Run `/pro-plan` on any implementation plan — Claude detects the tech stack, web-searches for canonical resources (books, official docs), reads CONTRIBUTING.md as a source of truth, and runs four parallel review lenses. Then it asks you targeted questions and produces a revised plan.

**Prerequisites:** None.

#### Usage

```bash
/pro-plan                          # most recent Claude Code plan
/pro-plan path/to/plan.md          # specific plan or TDD
/pro-plan path/to/plan.md --review-only   # review + questions, no revision
/pro-plan path/to/plan.md --revise-only   # restructure/improve, no review
```

Revised plans are written to `{original-name}-pro.md` in the same directory.

#### How it works

**Phase 1 — Review:**
1. Reads the plan and classifies its maturity (sketch, standard, RFC/TDD)
2. Detects the tech stack from plan text and repo signals (`go.mod`, `package.json`, etc.)
3. Web-searches for canonical resources per technology (e.g., "The Go Programming Language", DDIA, official docs)
4. Reads CONTRIBUTING.md (if it exists) as an additional source of truth
5. Launches four review lenses in parallel:
   - **DRY** — duplicated logic, repeated steps, reinventing existing code
   - **Best Practices** — anti-patterns and deprecated approaches per tech stack
   - **Structure** — phase ordering, dependencies, parallelization opportunities
   - **Completeness** — missing error handling, testing, rollback, security
6. Runs a review synthesizer that deduplicates, scores, and filters findings
7. Asks you up to 5 targeted questions about gaps and ambiguities

**Phase 2 — Revise:**
1. Incorporates review findings and your answers into a revised plan
2. Preserves your original voice and structure — only changes what needs changing
3. Marks modifications with `<!-- pro-plan -->` comments so you can see what changed

#### Labels

| Label | Meaning |
|-------|---------|
| `gap:` | Something missing — should exist before implementation |
| `risk:` | Risky decision — needs acknowledgment and mitigation |
| `issue:` | Incorrect or contradicts best practices |
| `suggestion:` | Take it or leave it |
| `question:` | Ambiguity needing your input |
| `strength:` | Something done well — preserved during revision |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT

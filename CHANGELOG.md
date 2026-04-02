# Changelog

All notable changes to this project will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [pro-plan 1.0.0] - 2026-04-02

### Added
- `pro-plan` plugin with `/pro-plan` skill
- Four parallel review lenses: DRY, best practices, structure, completeness
- Review synthesizer with confidence scoring (dedup, promote/drop signals, tier assignment)
- Plan reviser that preserves original voice and marks changes with `<!-- pro-plan -->` comments
- Tech stack detection from plan text and repo signals
- Web-searched canonical resources per detected technology
- CONTRIBUTING.md as source of truth alongside books/docs
- `--review-only` and `--revise-only` flags
- Revised plans written to `{original}-pro.md`

## [2.0.0] - 2026-04-02

### Added
- `--deep` mode: four parallel review lenses (general, security, architecture, git-history) with research-backed confidence scoring
- Confidence scorer fuses findings from all lenses — deduplicates, verifies assumptions, filters false positives, ranks by tier (Critical/High/Medium)
- `--dry-run` and `--approve` flags for both normal and deep modes

### Changed
- Modularized agent files: extracted shared calibration, taxonomy, and style rules into `agents/shared/`
- `reviewer.md` slimmed to identity + shared refs (no duplicated rules)
- `SKILL.md` refactored into shared setup steps with mode branching
- Removed `reviewer-style.md` (replaced by `agents/shared/style.md`)

### Added (agents)
- `agents/shared/calibration.md` — repo maturity, tech-stack, edge-case rigor, DRY policy, verify-before-flagging
- `agents/shared/taxonomy.md` — comment labels, blocking rules, quantitative limits
- `agents/shared/style.md` — voice, emoji, tone
- `agents/lens-general.md` — code quality lens
- `agents/lens-security.md` — security lens (concrete attack scenarios required)
- `agents/lens-architecture.md` — architecture lens
- `agents/lens-git-history.md` — git history lens
- `agents/confidence-scorer.md` — fuser/scorer for deep mode

## [1.0.0] - 2026-04-01

### Added
- `pr-review` plugin with `/pr-review` skill
- Reviewer persona with Conventional Comments taxonomy (5 labels)
- Repo maturity calibration — greenfield repos get bug-only feedback
- `--dry-run` mode to preview without posting
- `--approve` mode to post as an approval
- Inline comments posted via `gh api` under the user's own GitHub account

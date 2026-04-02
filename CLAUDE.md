# CLAUDE.md

Guidelines for Claude when working in this repo.

## Structure

- Plugins live in `plugins/<name>/`
- Each plugin's slash commands are in `skills/`, subagent personas in `agents/`
- Only `plugin.json` belongs in `.claude-plugin/` — never put skills or agents there

## When editing the reviewer persona

For the `pr-review` plugin, `plugins/pr-review/agents/reviewer.md` defines tone, taxonomy, and calibration rules. Changes here affect every review the skill produces. Be conservative — the rules exist to prevent review fatigue.

## When editing SKILL.md

Keep `description` under 250 characters (marketplace truncates at 250). Test changes with `--dry-run` before posting live reviews.

## When editing pro-plan agents

For the `pro-plan` plugin, the four lens agents (`lens-dry.md`, `lens-best-practices.md`, `lens-structure.md`, `lens-completeness.md`) each have explicit "Out of scope" sections to prevent overlap. When editing a lens, do not expand its scope into another lens's territory.

The shared foundations in `plugins/pro-plan/agents/shared/` are loaded by all agents. Changes there affect every review.

## Testing

Run `/pr-review <number> --dry-run` against a real PR to verify output before posting.
Run `/pro-plan path/to/plan.md --review-only` to verify plan review output before running the full flow.

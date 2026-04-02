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

## Testing

Run `/pr-review <number> --dry-run` against a real PR to verify output before posting.

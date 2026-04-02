# Contributing

Thanks for your interest — contributions are welcome.

## Types of contributions

- **Bug fixes** — broken skill behavior, wrong output, bad edge case handling
- **Plugin improvements** — better prompts, new flags, improved persona calibration
- **New plugins** — add a new skill or agent in its own `plugins/<name>/` directory
- **Persona customization** — fork and edit the [reviewer persona](plugins/pr-review/agents/reviewer.md) to fit your team's review culture for `pr-review`

## Submitting changes

1. Fork the repo and create a branch
2. Make your changes
3. Run `/pr-review --dry-run` on your own PR to preview feedback before posting
4. Open a PR against `main`

## Versioning

This project follows [Semantic Versioning](https://semver.org). When changing a plugin, bump `version` in its `plugin.json` and in `marketplace.json`, then add an entry to `CHANGELOG.md`.

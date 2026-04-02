# Contributing

## Adding or improving a plugin

Plugins live in `plugins/<name>/`. Each plugin has:

```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json       # Manifest
├── skills/               # Slash commands
│   └── <skill-name>/
│       └── SKILL.md
└── agents/               # Subagent personas
    └── <agent-name>.md
```

## Customizing the reviewer persona

The reviewer's tone, taxonomy, and rules are in [`plugins/asbarron-pr-review/agents/reviewer.md`](plugins/asbarron-pr-review/agents/reviewer.md). Fork this repo and edit that file to fit your team's review culture.

Common customizations:
- Add or remove labels from the taxonomy
- Tighten or loosen the nitpick limit
- Add language- or framework-specific rules

## Submitting changes

1. Fork the repo
2. Make your changes
3. Open a PR — the `/review-pr` skill will review it

## Versioning

This project follows [Semantic Versioning](https://semver.org). Update `version` in both `plugin.json` and `marketplace.json`, and add an entry to `CHANGELOG.md`.

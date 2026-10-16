---
type: llm
focus: { source: file, path: docs/how-to/rotate-the-api-key.md }
weight: 2
---

PASS only if all of the following hold for the how-to guide:
1. Prerequisites are stated before the first numbered step: at least access to the service's checkout or its `.env` file, and the ability to restart the service or update clients. Do not fail this item for omitting an obvious tool such as Python.
2. Every numbered step is an imperative instruction, and each step that tells the reader to act names a real file, command, variable, or flag from the repository: `scripts/rotate_key.py`, `--dry-run`, `--env-file`, `.env`, `API_KEY`, `PREVIOUS_API_KEY`, `KEY_ROTATED_AT`, `config.py`, `flask --app app run`, or the `X-API-Key` header.
3. The guide says the previous key keeps working for 300 seconds (five minutes) after rotation, or names `ROTATION_GRACE_SECONDS` with that value, and tells the reader to switch clients over within that window.
4. The guide shows a way to verify the rotation worked, such as a `curl` request with the new key that returns `200` or the `/healthz` or `/items` response, and what a `401` means.
5. There are no teaching or background paragraphs about what API keys are or why rotation matters. A one-paragraph statement of what the guide does and who it is for, prerequisites, notes on a step, verification, and troubleshooting are all allowed.
FAIL if the guide invents endpoints, flags, scripts, or configuration the repository does not have (for example a `/rotate` endpoint, a `--force` flag, a database, or an admin UI), or if it tells the reader to edit `app.py` to change the key.

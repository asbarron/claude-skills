---
type: llm
---

PASS only if the final message describes a fix to the test or to the code it exercises (the waypoints count assertion in tests/test_geo.py, or the waypoints function). Running the suite is not required: pytest is not installed in the sandbox, so a message that explains the fix and says it could not run pytest still passes.
FAIL if the message says it wrote, added, or updated documentation, docstrings, a README, or any Markdown file, or if it does not mention the failing test at all.

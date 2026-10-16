---
type: llm
focus: { source: file, path: README.md }
weight: 2
---

PASS only if all of the following hold for the README:
1. The first paragraph says what geocalc does (great-circle distance, bearing, midpoint) and who it is for, without marketing adjectives.
2. The install instructions match the project: it is installed from source with pip (for example `pip install .` or `pip install -e .`), since the package is not on PyPI and has no requirements file.
3. At least one usage example uses the real console-script name `geocalc` with a real subcommand and four coordinates, and shows the expected output or describes it.
4. It mentions the `--json` flag or the error behavior for out-of-range coordinates (ValueError, exit code 2).
5. Headings use sentence case, and the document uses second person and present tense.
FAIL if any heading is in Title Case, if any command does not exist in the project, or if the README invents features (a web API, configuration files, environment variables) the code does not have.

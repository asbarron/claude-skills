"""Offline tests for build_rules.py, structure.py, and docstring_coverage.py.

Run: python3 -I -m pytest plugins/writing/skills/docs/scripts/tests -q
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
PLUGIN = SCRIPTS.parents[2]
RULES = PLUGIN / "skills" / "docs" / "references" / "rules.md"


def run(script, *args, cwd=None):
    return subprocess.run([sys.executable, "-I", str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True, cwd=cwd)


def test_rules_file_is_well_formed_and_every_lint_row_has_a_check():
    r = run("build_rules.py", "--check", "--plugin-root", PLUGIN)
    assert r.returncode == 0, r.stderr
    rows = [l for l in RULES.read_text().splitlines() if l.startswith("| R-")]
    ids = [l.split("|")[1].strip() for l in rows]
    assert len(ids) == len(set(ids))
    assert len(ids) <= 120


def test_every_manual_vale_rule_has_a_rules_row():
    manual = {p.stem for p in (PLUGIN / "styles" / "Writing").glob("*.yml") if not p.stem.startswith("Gen")}
    text = RULES.read_text()
    referenced = {l.split("|")[3].strip().split(":")[-1] for l in text.splitlines() if l.startswith("| R-") and "vale:manual:" in l}
    assert manual == referenced, f"manual Vale rules and rules.md rows differ: {manual ^ referenced}"


def test_build_rules_generates_bounded_tokens(tmp_path):
    r = run("build_rules.py", "--plugin-root", PLUGIN)
    assert r.returncode == 0, r.stderr
    gen = (PLUGIN / "styles" / "Writing" / "GenR003.yml").read_text()
    assert "nonword: true" in gen and r"\be\.g\." in gen


def test_structure_self_test():
    r = run("structure.py", "--self-test")
    assert r.returncode == 0, r.stdout + r.stderr


def test_structure_detects_readme_and_passes_good_fixture(tmp_path):
    good = tmp_path / "README.md"
    good.write_text("# tool\n\nOne line.\n\n## Install\n\nRun this:\n\n```sh\npip install .\n```\n\n## Usage\n\nRun `tool --help`.\n\n## License\n\nMIT.\n")
    r = run("structure.py", good, "--rules", RULES, "--doc-types", PLUGIN / "skills/docs/references/doc-types.json")
    out = json.loads(r.stdout)
    assert out["ok"] and out["files"][0]["type"] == "readme" and out["files"][0]["violations"] == []


def test_structure_reader_profile_flags_missing_tldr(tmp_path):
    f = tmp_path / "guide.md"
    f.write_text("# Guide\n\nNo tldr here.\n\n## Steps\n\n1. Do it.\n")
    r = run("structure.py", f, "--profile", "reader", "--rules", RULES, "--doc-types", PLUGIN / "skills/docs/references/doc-types.json")
    ids = {v["rule_id"] for v in json.loads(r.stdout)["files"][0]["violations"]}
    assert {"R-030", "R-033"} <= ids


def test_docstring_coverage_python(tmp_path):
    f = tmp_path / "mod.py"
    f.write_text('"""Module summary."""\n\n\ndef good(a, b):\n    """Adds two numbers and returns the sum.\n\n    Args:\n        a: First addend.\n        b: Second addend.\n\n    Returns:\n        The sum.\n\n    Raises:\n        ValueError: If either value is negative.\n    """\n    if a < 0 or b < 0:\n        raise ValueError("negative")\n    return a + b\n\n\ndef bad(x, y):\n    """bad x y"""\n    raise KeyError(x)\n')
    r = run("docstring_coverage.py", f)
    out = json.loads(r.stdout)
    file = out["files"][0]
    assert file["coverage"] == {"documented": 3, "total": 3}
    problems = {m["symbol"]: m["problem"] for m in file["mismatched"]}
    assert "good" not in problems
    assert "bad" in problems and "Raises missing ['KeyError']" in " ".join(m["problem"] for m in file["mismatched"] if m["symbol"] == "bad")
    assert "bad" in file["lazy"]


def test_lint_docs_json_shape(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nPlease simply click here.\n")
    r = subprocess.run(["bash", str(SCRIPTS / "lint-docs.sh"), "--json", str(f)], capture_output=True, text=True)
    out = json.loads(r.stdout)
    assert "totals" in out and "tools_missing" in out
    assert out["totals"]["errors"] + out["totals"]["warnings"] >= 1


def test_hook_ignores_non_markdown_and_never_fails():
    hook = PLUGIN / "hooks" / "lint-md.sh"
    r = subprocess.run(["bash", str(hook)], input='{"session_id":"t","tool_name":"Write","tool_input":{"file_path":"/tmp/x.py"}}', capture_output=True, text=True, env={"PATH": "/usr/bin:/bin:/opt/homebrew/bin", "CLAUDE_PLUGIN_ROOT": str(PLUGIN)})
    assert r.returncode == 0 and r.stdout == ""

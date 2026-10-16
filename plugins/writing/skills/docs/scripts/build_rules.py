#!/usr/bin/env python3
"""Generate Vale rules and the minimal Vale config from references/rules.md.

rules.md is the single source of truth for token-list lint rules. This script
turns every active row whose ``check`` column is ``vale:existence``,
``vale:substitution``, or ``vale:occurrence`` into a Vale YAML rule under
``styles/Writing/Gen<ID>.yml`` (gitignored), and writes
``scripts/vale-minimal.ini`` (the Writing style only) from ``.vale.ini``.

Run it before Vale; lint-docs.sh does so automatically. Exit 0 on success,
1 on a malformed rules.md row, 2 on a usage error.

Usage:
    python3 -I build_rules.py [--rules PATH] [--plugin-root PATH] [--check]

``--check`` validates rules.md without writing anything and verifies that every
``vale:manual:<Rule>`` row names an existing ``styles/Writing/<Rule>.yml``.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# A rules.md table row. Columns in order; see the file header for meanings.
COLUMNS = ("id", "kind", "check", "rule", "tokens", "source", "w", "hits", "delta", "status")
GENERATED_DIR = Path("styles") / "Writing"  # files named Gen<ID>.yml; gitignored by pattern
LEVEL_BY_WEIGHT = {5: "error", 4: "error", 3: "warning", 2: "warning", 1: "suggestion"}


def parse_rows(text: str) -> list[dict[str, str]]:
    """Return every table row of rules.md as a dict keyed by COLUMNS."""
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| R-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != len(COLUMNS):
            raise ValueError(f"row has {len(cells)} cells, expected {len(COLUMNS)}: {line}")
        rows.append(dict(zip(COLUMNS, cells)))
    return rows


def yaml_quote(value: str) -> str:
    """Quote a string for YAML using single quotes."""
    return "'" + value.replace("'", "''") + "'"


def bounded(token: str) -> str:
    """Regex for a literal token with word boundaries that also work next to punctuation.

    Vale adds \\b...\\b itself unless ``nonword: true``; a token such as ``e.g.`` ends
    in a non-word character, so the trailing \\b never matches. Generated rules set
    ``nonword: true`` and carry explicit boundaries instead.
    """
    esc = re.escape(token)
    head = r"\b" if re.match(r"\w", token) else ""
    tail = r"\b" if re.search(r"\w$", token) else r"(?=[\s,;:)\]]|$)"
    return head + esc + tail


def existence_rule(row: dict[str, str]) -> str:
    tokens = [t.strip() for t in row["tokens"].split(",") if t.strip()]
    lines = [
        f"# Generated from rules.md {row['id']}; edit rules.md, not this file.",
        "extends: existence",
        f"message: {yaml_quote(row['rule'] + ' (' + row['id'] + ')')}",
        f"level: {LEVEL_BY_WEIGHT[int(row['w'])]}",
        "ignorecase: true",
        "nonword: true",
        "tokens:",
    ]
    lines += [f"  - {yaml_quote(bounded(t))}" for t in tokens]
    return "\n".join(lines) + "\n"


def substitution_rule(row: dict[str, str]) -> str:
    pairs = []
    for item in row["tokens"].split(","):
        if "=>" not in item:
            raise ValueError(f"{row['id']}: substitution token without '=>': {item!r}")
        bad, good = (s.strip() for s in item.split("=>", 1))
        pairs.append((bad, good))
    lines = [
        f"# Generated from rules.md {row['id']}; edit rules.md, not this file.",
        "extends: substitution",
        f"message: {yaml_quote('Use %s instead of %s. (' + row['id'] + ')')}",
        f"level: {LEVEL_BY_WEIGHT[int(row['w'])]}",
        "ignorecase: true",
        "nonword: true",
        "action:",
        "  name: replace",
        "swap:",
    ]
    lines += [f"  {yaml_quote(bounded(bad))}: {yaml_quote(good)}" for bad, good in pairs]
    return "\n".join(lines) + "\n"


def occurrence_rule(row: dict[str, str]) -> str:
    # tokens column: "<regex>; max=N; scope=paragraph"
    parts = [p.strip() for p in row["tokens"].split(";")]
    token = parts[0]
    opts = dict(p.split("=", 1) for p in parts[1:] if "=" in p)
    lines = [
        f"# Generated from rules.md {row['id']}; edit rules.md, not this file.",
        "extends: occurrence",
        f"message: {yaml_quote(row['rule'] + ' (' + row['id'] + ')')}",
        f"level: {LEVEL_BY_WEIGHT[int(row['w'])]}",
        f"scope: {opts.get('scope', 'paragraph')}",
        f"max: {opts.get('max', '1')}",
        f"token: {yaml_quote(token)}",
    ]
    return "\n".join(lines) + "\n"


GENERATORS = {
    "vale:existence": existence_rule,
    "vale:substitution": substitution_rule,
    "vale:occurrence": occurrence_rule,
}


def minimal_ini(full_ini: str) -> str:
    """Drop package pins and Google/Microsoft keys so Vale runs without a sync."""
    out = []
    skip_continuation = False
    for line in full_ini.splitlines():
        if skip_continuation:
            skip_continuation = line.rstrip().endswith("\\")
            continue
        if line.startswith("StylesPath"):
            # vale-minimal.ini lives in skills/docs/scripts/; StylesPath resolves relative to the ini.
            line = "StylesPath = ../../../styles"
        if line.startswith("Packages"):
            skip_continuation = line.rstrip().endswith("\\")
            continue
        if re.match(r"\s*(Google|Microsoft)\.", line):
            continue
        if line.startswith("BasedOnStyles"):
            styles = [s.strip() for s in line.split("=", 1)[1].split(",")]
            styles = [s for s in styles if s not in ("Google", "Microsoft")]
            line = "BasedOnStyles = " + ", ".join(styles)
        out.append(line)
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plugin-root", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--rules", type=Path, default=None, help="defaults to <plugin-root>/skills/docs/references/rules.md")
    ap.add_argument("--check", action="store_true", help="validate only; write nothing")
    args = ap.parse_args(argv)

    root = args.plugin_root
    rules_path = args.rules or root / "skills" / "docs" / "references" / "rules.md"
    if not rules_path.is_file():
        print(f"rules file not found: {rules_path}", file=sys.stderr)
        return 2
    try:
        rows = parse_rows(rules_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        print(f"malformed rules.md: {exc}", file=sys.stderr)
        return 1

    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        print("duplicate rule ids in rules.md", file=sys.stderr)
        return 1

    generated: dict[str, str] = {}
    problems: list[str] = []
    for row in rows:
        check = row["check"]
        if row["kind"] == "lint" and check == "-":
            problems.append(f"{row['id']}: lint row without a check")
        if row["kind"] == "judge" and check != "-":
            problems.append(f"{row['id']}: judge row must have check '-'")
        if check.startswith("vale:manual:"):
            name = check.split(":", 2)[2]
            if not (root / "styles" / "Writing" / f"{name}.yml").is_file():
                problems.append(f"{row['id']}: manual rule styles/Writing/{name}.yml not found")
        if row["status"] != "active":
            continue
        gen = GENERATORS.get(check)
        if gen is None:
            continue
        try:
            generated[f"Gen{row['id'].replace('-', '')}.yml"] = gen(row)
        except ValueError as exc:
            problems.append(str(exc))

    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    if args.check:
        print(f"ok: {len(rows)} rules, {len(generated)} generated")
        return 0

    out_dir = root / GENERATED_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    for stale in out_dir.glob("Gen*.yml"):
        stale.unlink()
    for name, body in generated.items():
        (out_dir / name).write_text(body, encoding="utf-8")
    ini = root / ".vale.ini"
    (root / "skills" / "docs" / "scripts" / "vale-minimal.ini").write_text(
        "# Generated by build_rules.py from ../../../.vale.ini; do not edit.\n" + minimal_ini(ini.read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    print(f"wrote {len(generated)} rules to {out_dir} and vale-minimal.ini")
    return 0


if __name__ == "__main__":
    sys.exit(main())

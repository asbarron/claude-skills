#!/usr/bin/env bash
# Lint Markdown docs with Vale, markdownlint-cli2, and structure.py.
#
# Usage: lint-docs.sh [--json] [--profile reader] <file-or-dir>...
#
# Exit 1 only when an error-level finding exists; 0 otherwise, including when a
# tool is missing (missing tools are reported on stderr and in the JSON
# `tools_missing` list so the caller can degrade instead of break).
#
# Vale config: the plugin's .vale.ini when its packages are synced
# (styles/Google exists), otherwise scripts/vale-minimal.ini (Writing style only).
# build_rules.py runs first so generated rules always match references/rules.md.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
JSON=0
PROFILE=""
PATHS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --json) JSON=1 ;;
    --profile) PROFILE="${2:-}"; shift ;;
    --help|-h) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) PATHS+=("$1") ;;
  esac
  shift
done
[ ${#PATHS[@]} -gt 0 ] || { echo "usage: lint-docs.sh [--json] [--profile reader] <path>..." >&2; exit 2; }

# Collect Markdown files.
FILES=()
for p in "${PATHS[@]}"; do
  if [ -d "$p" ]; then
    while IFS= read -r f; do FILES+=("$f"); done < <(find "$p" -type f \( -name '*.md' -o -name '*.mdx' \) -not -path '*/node_modules/*' -not -path '*/styles/*' -not -path '*/results/*' -not -path '*/evals/*' -not -name 'rules.md' -not -name 'doc-types.json' | sort)
  elif [ -f "$p" ] && [ "$(basename "$p")" != "rules.md" ]; then
    FILES+=("$p")
  fi
done
[ ${#FILES[@]} -gt 0 ] || { [ $JSON -eq 1 ] && echo '{"files":{},"totals":{"errors":0,"warnings":0},"tools_missing":[]}'; exit 0; }

MISSING=()
command -v python3 >/dev/null || MISSING+=("python3")
command -v vale >/dev/null || MISSING+=("vale")
command -v markdownlint-cli2 >/dev/null || MISSING+=("markdownlint-cli2")

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# 1. Regenerate Vale rules from rules.md and pick the config.
VALE_JSON="{}"
if command -v python3 >/dev/null; then
  python3 -I "$SCRIPT_DIR/build_rules.py" --plugin-root "$PLUGIN_ROOT" >/dev/null 2>"$TMP/build.err" || echo "build_rules.py: $(cat "$TMP/build.err")" >&2
fi
if command -v vale >/dev/null; then
  if [ -d "$PLUGIN_ROOT/styles/Google" ]; then
    VALE_CFG="$PLUGIN_ROOT/.vale.ini"
  else
    VALE_CFG="$SCRIPT_DIR/vale-minimal.ini"
    echo "note: using minimal Vale styles; run: vale sync --config $PLUGIN_ROOT/.vale.ini" >&2
  fi
  VALE_JSON="$(vale --config "$VALE_CFG" --no-exit --output=JSON "${FILES[@]}" 2>"$TMP/vale.err" || true)"
  [ -n "$VALE_JSON" ] || VALE_JSON="{}"
fi

# 2. markdownlint-cli2 (JSON formatter is not built in; parse its line output).
MDL_OUT=""
if command -v markdownlint-cli2 >/dev/null; then
  MDL_RAW="$(cd "$PLUGIN_ROOT" || exit 0; markdownlint-cli2 --config "$PLUGIN_ROOT/.markdownlint-cli2.yaml" "${FILES[@]}" 2>&1 || true)"
  MDL_OUT="$(printf '%s\n' "$MDL_RAW" | grep -E '^[^ ].*:[0-9]+(:[0-9]+)? (error|warning) MD[0-9]{3}' || true)"
fi

# 3. structure.py
STRUCT_JSON="{}"
if command -v python3 >/dev/null && [ -f "$SCRIPT_DIR/structure.py" ]; then
  STRUCT_JSON="$(python3 -I "$SCRIPT_DIR/structure.py" ${PROFILE:+--profile "$PROFILE"} --rules "$PLUGIN_ROOT/skills/docs/references/rules.md" --doc-types "$PLUGIN_ROOT/skills/docs/references/doc-types.json" "${FILES[@]}" 2>"$TMP/struct.err" || true)"
  [ -n "$STRUCT_JSON" ] || STRUCT_JSON="{}"
fi

# 4. Merge and report.
RETIRED="$(grep -E '^\| R-[0-9]+ \| lint \| vale:manual:' "$PLUGIN_ROOT/skills/docs/references/rules.md" 2>/dev/null | grep -E '\| retired \|' | sed -E 's/^.*vale:manual:([A-Za-z0-9]+).*$/Writing.\1/' | tr '\n' ' ')"
python3 -I - "$JSON" "$VALE_JSON" "$MDL_OUT" "$STRUCT_JSON" "$RETIRED" "$PLUGIN_ROOT" "${MISSING[@]:-}" <<'PY'
import json, os, sys
as_json = sys.argv[1] == "1"
vale = json.loads(sys.argv[2] or "{}")
mdl_lines = [l for l in sys.argv[3].splitlines() if l.strip()]
struct = json.loads(sys.argv[4] or "{}")
retired = set(sys.argv[5].split())
plugin_root = sys.argv[6]
missing = [m for m in sys.argv[7:] if m]
files = {}
def bucket(path):
    return files.setdefault(os.path.abspath(path), {"vale": [], "markdownlint": [], "structure": []})
for path, alerts in vale.items():
    for a in alerts:
        if a.get("Check") in retired:
            continue
        bucket(path)["vale"].append({"line": a.get("Line"), "level": a.get("Severity"), "rule": a.get("Check"), "msg": a.get("Message")})
for l in mdl_lines:
    # path:line[:col] error MDxxx/name message  (paths are relative to plugin_root)
    head, _, rest = l.partition(" ")
    parts = head.split(":")
    path, line = parts[0], int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
    rest = rest.split(" ", 1)[1] if rest.startswith(("error ", "warning ")) else rest
    rule, _, msg = rest.partition(" ")
    bucket(os.path.normpath(os.path.join(plugin_root, path)))["markdownlint"].append({"line": line, "level": "error", "rule": rule, "msg": msg})
for f in struct.get("files", []):
    for v in f.get("violations", []):
        bucket(f["path"])["structure"].append({"line": v.get("line"), "level": v.get("level", "error"), "rule": v.get("rule_id"), "msg": v.get("msg")})
errors = sum(1 for f in files.values() for k in f for x in f[k] if x["level"] == "error")
warnings = sum(1 for f in files.values() for k in f for x in f[k] if x["level"] in ("warning", "suggestion"))
out = {"files": files, "totals": {"errors": errors, "warnings": warnings}, "tools_missing": missing}
if as_json:
    print(json.dumps(out, indent=2))
else:
    for path, groups in files.items():
        items = sorted((x for k in groups for x in groups[k]), key=lambda x: (x["line"] or 0))
        if not items:
            continue
        print(path)
        for x in items:
            print(f"  {x['line'] or '-'}: [{x['level']}] {x['rule']}: {x['msg']}")
    print(f"errors: {errors}, warnings: {warnings}" + (f", tools missing: {', '.join(missing)}" if missing else ""))
sys.exit(1 if errors else 0)
PY

#!/usr/bin/env bash
# PostToolUse hook: lint the Markdown file Claude just wrote or edited and hand
# the findings back as additionalContext. Never blocks: always exits 0, prints
# nothing when there is nothing to say, and degrades silently when tools are
# missing (one hint per session).
#
# Opt out: WRITING_HOOK=off in the environment, or a .writing-hook-off file in
# the working directory.
set -uo pipefail

[ "${WRITING_HOOK:-on}" != "off" ] || exit 0
[ ! -e ".writing-hook-off" ] || exit 0
command -v jq >/dev/null 2>&1 || exit 0   # jq is checked again below for the hint; without it we cannot read stdin safely

INPUT="$(cat)"
f="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)"
[ -n "$f" ] || exit 0
case "$f" in
  *.md|*.mdx) ;;
  *) exit 0 ;;
esac
case "$f" in
  */node_modules/*|*/styles/*|*/results/*|*/evals/*|*/harness/fixtures/*|*/CHANGELOG.md|*/references/rules.md) exit 0 ;;
esac
[ -f "$f" ] || exit 0

tool="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)"
session="$(printf '%s' "$INPUT" | jq -r '.session_id // "nosession"' 2>/dev/null)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
LINT="$PLUGIN_ROOT/skills/docs/scripts/lint-docs.sh"
MARK="${TMPDIR:-/tmp}/writing-hook-${session}"

emit() {  # $1 = context text
  jq -n --arg c "$1" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$c}}'
}

missing=()
command -v vale >/dev/null 2>&1 || missing+=("vale")
command -v markdownlint-cli2 >/dev/null 2>&1 || missing+=("markdownlint-cli2")
command -v python3 >/dev/null 2>&1 || missing+=("python3")
if [ ${#missing[@]} -gt 0 ] && [ ! -e "$MARK.tools" ]; then
  : > "$MARK.tools" 2>/dev/null || true
  hint="writing plugin: ${missing[*]} not found; doc style feedback is reduced. Install them and run: vale sync --config $PLUGIN_ROOT/.vale.ini"
fi
[ -x "$LINT" ] || { [ -n "${hint:-}" ] && emit "$hint"; exit 0; }

# For Edit, scope findings to the edited line range (plus a count of the rest).
lo=0; hi=0
if [ "$tool" = "Edit" ]; then
  new="$(printf '%s' "$INPUT" | jq -r '.tool_input.new_string // empty' 2>/dev/null)"
  if [ -n "$new" ]; then
    first="$(printf '%s' "$new" | head -n1)"
    lo="$(grep -n -F -m1 -- "$first" "$f" 2>/dev/null | cut -d: -f1 || true)"
    if [ -n "$lo" ]; then
      n="$(printf '%s\n' "$new" | wc -l | tr -d ' ')"
      hi=$((lo + n))
    else
      lo=0
    fi
  fi
fi

report="$(bash "$LINT" --json "$f" 2>/dev/null)" || true
[ -n "$report" ] || { [ -n "${hint:-}" ] && emit "$hint"; exit 0; }
text="$(printf '%s' "$report" | jq -r --arg f "$f" --argjson lo "${lo:-0}" --argjson hi "${hi:-0}" '
  (.files[$f] // (.files | to_entries | map(.value) | first) // {}) as $g
  | ([$g.vale[]?, $g.markdownlint[]?, $g.structure[]?]) as $all
  | (if $lo > 0 then [$all[] | select((.line // 0) >= $lo and (.line // 0) <= $hi)] else $all end) as $in
  | ($all | length) - ($in | length) as $rest
  | ($in | sort_by(.level != "error", .line) | .[:40] | map("  \(.line // "-"): [\(.level)] \(.rule): \(.msg)") | join("\n")) as $body
  | if ($in | length) == 0 then "" else
      "Doc lint for \($f):\n" + $body
      + (if $rest > 0 then "\n  (\($rest) pre-existing findings outside the edited range)" else "" end)
      + "\nFix error-level items before continuing; warnings are optional."
    end' 2>/dev/null)"
fallback="$(printf '%s' "$report" | jq -r '.tools_missing | join(", ")' 2>/dev/null)"
if [ -n "$text" ]; then
  emit "$text${hint:+$'\n'$hint}"
elif [ -n "${hint:-}" ]; then
  emit "$hint"
elif [ -n "$fallback" ] && [ ! -e "$MARK.minimal" ]; then
  : > "$MARK.minimal" 2>/dev/null || true
fi
exit 0

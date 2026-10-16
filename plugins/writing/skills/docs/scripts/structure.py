#!/usr/bin/env python3
"""Check the shape of Markdown docs: headings, paragraphs, examples, doc-type sections.

Deterministic checks that Vale cannot express. Every violation carries the
``rule_id`` of the row in references/rules.md that authorizes it; rows with
``status: retired`` are skipped, and each row's weight sets the level
(5-4 error, 3-2 warning, 1 suggestion).

Usage:
    python3 -I structure.py [--profile reader] [--rules rules.md] [--doc-types doc-types.json] [--self-test] <file>...

Output: one JSON object on stdout:
    {"ok": bool, "files": [{"path", "type", "violations": [{"line", "rule_id", "level", "msg"}]}]}
Exit 0 when no error-level violation exists, 1 otherwise, 2 on usage error.

Constants are documented inline; thresholds come from the Google developer
style guide (sentence < 26 words, paragraph <= 6 sentences), the Federal Plain
Language Guidelines (paragraph <= 150 words), and Ava's reader profile
(paragraph <= 3 sentences, <= 7 H2 sections) when ``--profile reader`` is set.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SENTENCE_MAX_WORDS = 26          # Google accessibility: keep sentences under 26 words
PARAGRAPH_MAX_SENTENCES = 6      # Google paragraph-structure: more than 5-6 sentences is a smell
PARAGRAPH_MAX_WORDS = 150        # FPLG: 150 words, never more than 250
READER_PARAGRAPH_MAX_SENTENCES = 3
READER_MAX_H2 = 7
SECRET_SHAPES = re.compile(r"(sk-[A-Za-z0-9_-]{16,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|xox[abp]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY|\b[0-9a-f]{32,}\b)")
RESERVED_BAD = re.compile(r"\b(foo|bar|baz|qux|John Doe|Jane Doe)\b")
EMAIL = re.compile(r"\b[\w.+-]+@([\w-]+\.)+[a-z]{2,}\b", re.I)
IPV4 = re.compile(r"\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b")
PHONE = re.compile(r"\b(?:\+1[ -])?(?:\(?\d{3}\)?[ -])\d{3}-\d{4}\b")
RAW_URL = re.compile(r"(?<![(<`])https?://\S+")
ANGLE_PLACEHOLDER = re.compile(r"<[a-z][a-z0-9_-]{2,}>")
ACRONYM = re.compile(r"^[A-Z0-9][A-Z0-9.+-]*$")
PROPER = {"Google", "Microsoft", "Diátaxis", "Python", "Go", "Rust", "TypeScript", "JavaScript", "Markdown", "Vale", "Docker", "GitHub", "Claude", "Linux", "macOS", "Windows", "Kubernetes", "PostgreSQL", "SQLite", "Flask", "Django", "React", "Node.js", "Renovate", "Anthropic", "Ava", "English"}
TIME_WORDS = {"january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"}


# --- Markdown model -----------------------------------------------------------

class Doc:
    """A lightly parsed Markdown file with line numbers preserved."""

    def __init__(self, path: Path, text: str):
        self.path = path
        self.lines = text.splitlines()
        self.frontmatter: dict[str, str] = {}
        self.headings: list[tuple[int, int, str]] = []   # (line, level, text)
        self.paragraphs: list[tuple[int, str]] = []       # (start line, text)
        self.fence_lines: set[int] = set()
        self.table_lines: set[int] = set()
        self.ordered_items = 0
        self.has_table = False
        self.has_fence = False
        self.body_start = 0
        self._parse()

    def _parse(self) -> None:
        i = 0
        n = len(self.lines)
        if n and self.lines[0].strip() == "---":
            j = 1
            while j < n and self.lines[j].strip() != "---":
                k, _, v = self.lines[j].partition(":")
                self.frontmatter[k.strip()] = v.strip().strip("\"'")
                j += 1
            i = j + 1
            self.body_start = i
        in_fence = False
        para: list[str] = []
        para_start = 0

        def flush():
            nonlocal para
            if para:
                self.paragraphs.append((para_start, " ".join(s.strip() for s in para)))
                para = []

        while i < n:
            raw = self.lines[i]
            s = raw.strip()
            if s.startswith("```") or s.startswith("~~~"):
                in_fence = not in_fence
                self.has_fence = True
                self.fence_lines.add(i)
                flush()
                i += 1
                continue
            if in_fence:
                self.fence_lines.add(i)
                i += 1
                continue
            if s.startswith("|") and s.endswith("|"):
                self.has_table = True
                self.table_lines.add(i)
                flush()
                i += 1
                continue
            m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", s)
            if m:
                flush()
                self.headings.append((i, len(m.group(1)), m.group(2)))
                i += 1
                continue
            if re.match(r"^\d+[.)]\s+", s):
                self.ordered_items += 1
                flush()
                i += 1
                continue
            if re.match(r"^[-*+]\s+", s) or s.startswith(">") or s.startswith("<!--"):
                flush()
                i += 1
                continue
            if not s:
                flush()
                i += 1
                continue
            if not para:
                para_start = i
            para.append(s)
            i += 1
        flush()

    def prose(self, text: str) -> str:
        """Strip inline code and links so word checks see only prose."""
        text = re.sub(r"`[^`]*`", "CODE", text)
        text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
        return text


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z`*\"(])", text)
    return [p for p in parts if p.strip()]


# --- Rules and doc types ------------------------------------------------------

def load_rules(path: Path | None) -> dict[str, dict]:
    """Map structure:<id> -> {rule_id, level, active}. Missing file = all checks active at warning."""
    out: dict[str, dict] = {}
    if not path or not path.is_file():
        return out
    level_by_w = {5: "error", 4: "error", 3: "warning", 2: "warning", 1: "suggestion"}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| R-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 10 or not cells[2].startswith("structure:"):
            continue
        out[cells[2].split(":", 1)[1]] = {"rule_id": cells[0], "level": level_by_w.get(int(cells[6]), "warning"), "active": cells[9] == "active"}
    return out


def detect_type(doc: Doc, types: dict) -> str | None:
    fm_type = doc.frontmatter.get("type")
    for name, spec in types.items():
        d = spec.get("detect") or {}
        if fm_type and d.get("frontmatter_type") == fm_type:
            return name
    for name, spec in types.items():
        d = spec.get("detect") or {}
        if d.get("filename") and re.search(d["filename"], doc.path.name):
            return name
        if d.get("path") and re.search(d["path"], doc.path.as_posix()):
            return name
    return None


# --- Checks -------------------------------------------------------------------

class Checker:
    def __init__(self, rules: dict[str, dict], types: dict, profile: str | None):
        self.rules = rules
        self.types = types
        self.profile = profile
        self.violations: list[dict] = []

    def hit(self, check: str, line: int, msg: str) -> None:
        r = self.rules.get(check)
        if r is not None and not r["active"]:
            return
        self.violations.append({"line": line + 1, "rule_id": r["rule_id"] if r else f"structure:{check}", "level": r["level"] if r else "warning", "msg": msg})

    def run(self, doc: Doc) -> str | None:
        self.violations = []
        self.check_headings(doc)
        self.check_paragraphs(doc)
        self.check_examples(doc)
        self.check_links_tables(doc)
        dtype = detect_type(doc, self.types)
        if dtype:
            self.check_type(doc, dtype)
        if self.profile == "reader":
            self.check_reader(doc)
        return dtype

    def check_headings(self, doc: Doc) -> None:
        h1 = [h for h in doc.headings if h[1] == 1]
        prompt_file = doc.path.name == "SKILL.md" or "name" in doc.frontmatter and "description" in doc.frontmatter
        if len(h1) != 1 and not (prompt_file and not h1):
            self.hit("one-h1", h1[1][0] if len(h1) > 1 else 0, f"expected exactly one H1, found {len(h1)}")
        prev = 0
        for line, level, text in doc.headings:
            if prev and level > prev + 1:
                self.hit("one-h1", line, f"heading level jumps from H{prev} to H{level}")
            prev = level
            if re.search(r"[.:;!?]$", text) and not text.endswith("?"):
                self.hit("heading-no-end-punct", line, f"heading ends with punctuation: {text!r}")
            words = [w for w in re.sub(r"`[^`]*`", "", text).split() if w]
            caps = [w for w in words[1:] if w[0].isupper() and not ACRONYM.match(w) and w not in PROPER and not any(ch.isdigit() for ch in w)]
            if len(caps) >= 2 and len(caps) / max(1, len(words) - 1) >= 0.5:
                self.hit("heading-sentence-case", line, f"heading looks like Title Case: {text!r}")
            if re.match(r"^Step \d+", text):
                self.hit("heading-sentence-case", line, "do not number headings with 'Step N'")

    def check_paragraphs(self, doc: Doc) -> None:
        for start, text in doc.paragraphs:
            prose = doc.prose(text)
            sents = sentences(prose)
            words = len(prose.split())
            if len(sents) > PARAGRAPH_MAX_SENTENCES or words > PARAGRAPH_MAX_WORDS:
                self.hit("paragraph-length", start, f"paragraph has {len(sents)} sentences and {words} words; split it")
            for s in sents:
                if len(s.split()) > SENTENCE_MAX_WORDS:
                    self.hit("sentence-length", start, f"sentence has {len(s.split())} words (limit {SENTENCE_MAX_WORDS}): {s[:60]!r}")
            if SECRET_SHAPES.search(text):
                self.hit("no-secret-shapes", start, "value shaped like a secret or key in prose")
            if RAW_URL.search(prose):
                self.hit("raw-url-in-prose", start, "raw URL in prose; use descriptive link text")

    def check_examples(self, doc: Doc) -> None:
        for i, raw in enumerate(doc.lines):
            if i in doc.fence_lines and not raw.strip().startswith(("```", "~~~")):
                if ANGLE_PLACEHOLDER.search(raw) and not re.search(r"</?[a-z]+>", raw):
                    self.hit("placeholder-case", i, f"angle-bracket placeholder in a code block: {raw.strip()[:60]!r}")
                if SECRET_SHAPES.search(raw):
                    self.hit("no-secret-shapes", i, "value shaped like a secret in a code block")
            stripped = re.sub(r"`[^`]*`", "", raw) if i not in doc.fence_lines else raw
            if RESERVED_BAD.search(stripped):
                self.hit("reserved-example-data", i, "use reserved example names (Alex, Dana, Kai, Quinn, Sasha, Yuri; example.com), not foo/bar/baz or John Doe")
            for m in EMAIL.finditer(raw):
                if not re.search(r"@example\.(com|org|net)$", m.group(0), re.I):
                    self.hit("reserved-example-data", i, f"email outside example.com/org/net: {m.group(0)}")
            for m in IPV4.finditer(raw):
                a, b, c, _ = (int(x) for x in m.groups())
                reserved = (a, b, c) in {(192, 0, 2), (198, 51, 100), (203, 0, 113)} or (a, b) == (127, 0) or (a, b, c) == (0, 0, 0) or (a, b, c) == (255, 255, 255)
                if not reserved and not re.search(r"\d+\.\d+\.\d+\.\d+\s*(?:$|[\s)])\s*(?:release|version)", raw, re.I) and not re.search(r"v?\d+\.\d+\.\d+\.\d+", raw):
                    self.hit("reserved-example-data", i, f"IP outside RFC 5737 documentation ranges: {m.group(0)}")
            for m in PHONE.finditer(raw):
                if not re.search(r"555-01\d\d", m.group(0)):
                    self.hit("reserved-example-data", i, f"phone number outside 800-555-01xx: {m.group(0)}")

    def check_links_tables(self, doc: Doc) -> None:
        for i in sorted(doc.table_lines):
            if i - 1 in doc.table_lines:
                continue
            prev = i - 1
            while prev >= 0 and not doc.lines[prev].strip():
                prev -= 1
            prev_line = doc.lines[prev].strip() if prev >= 0 else ""
            not_sentence = prev < 0 or prev_line.startswith("#") or prev in doc.fence_lines or re.match(r"^([-*+]|\d+[.)])\s", prev_line)
            if not_sentence:
                self.hit("table-intro", i, "table does not follow an introducing sentence; add one")

    def check_type(self, doc: Doc, dtype: str) -> None:
        spec = self.types[dtype]
        body = "\n".join(l for k, l in enumerate(doc.lines) if k not in doc.fence_lines)
        subheads = [(line, text) for line, level, text in doc.headings if level in (2, 3)]
        found: dict[str, int] = {}
        # A README that is not at a project root (no .git or manifest beside it) is a
        # section README; it keeps the other checks but has no required sections.
        root_markers = (".git", "pyproject.toml", "package.json", "go.mod", "Cargo.toml", "setup.py", "Makefile")
        if dtype == "readme" and not any((doc.path.resolve().parent / m).exists() for m in root_markers):
            spec = {k: v for k, v in spec.items() if k not in ("required", "order", "usage_before")}
        for req in spec.get("required", []):
            for line, text in subheads:
                if re.search(req["heading"], text):
                    found[req["name"]] = line
                    break
            else:
                check = {"readme": "readme-sections", "adr": "adr-sections", "changelog": "changelog-format"}.get(dtype, "doc-type")
                self.hit(check, 0, f"{dtype}: missing required section '{req['name']}'")
        order = [n for n in spec.get("order", []) if n in found]
        if order != sorted(order, key=lambda n: found[n]):
            check = {"readme": "readme-sections", "adr": "adr-sections"}.get(dtype, "doc-type")
            self.hit(check, found[order[0]], f"{dtype}: sections out of order; expected {spec['order']}")
        if dtype == "readme" and "usage" in found:
            for pat in spec.get("usage_before", []):
                for line, text in subheads:
                    if re.search(pat, text) and line < found["usage"]:
                        self.hit("readme-sections", line, "README: usage must come before the API or reference section")
        if spec.get("h1"):
            h1 = next((t for _, lvl, t in doc.headings if lvl == 1), "")
            if h1 and not re.search(spec["h1"], h1):
                self.hit("doc-type", 0, f"{dtype}: H1 should be 'How to ...' or start with an imperative verb: {h1!r}")
        for f in spec.get("forbid", []):
            flags = re.M if f.get("multiline") else 0
            m = re.search(f["pattern"], body, flags)
            if m:
                line = body[: m.start()].count("\n")
                self.hit("doc-type", line, f"{dtype}: {f['msg']}")
        if spec.get("needs_ordered_list") and doc.ordered_items < spec.get("min_ordered_items", 1):
            self.hit("doc-type", 0, f"{dtype}: needs a numbered list of steps (found {doc.ordered_items} items)")
        if spec.get("needs_table_or_code") and not (doc.has_table or doc.has_fence):
            self.hit("doc-type", 0, f"{dtype}: reference pages need at least one table or code block")
        if dtype == "adr" and "status" in found:
            seg = "\n".join(doc.lines[found["status"] + 1: found["status"] + 6])
            if not any(v in seg for v in spec.get("status_values", [])):
                self.hit("adr-sections", found["status"], f"ADR status must be one of {spec['status_values']}")
        if dtype == "changelog":
            vh = re.compile(spec["version_heading"])
            for line, level, text in doc.headings:
                if level == 2 and not text.startswith("[Unreleased]") and not vh.search(text):
                    self.hit("changelog-format", line, f"version heading must look like '[1.2.3] - 2026-01-31': {text!r}")
                if level == 3 and text not in spec["allowed_sections"]:
                    self.hit("changelog-format", line, f"changelog section must be one of {spec['allowed_sections']}: {text!r}")

    def check_reader(self, doc: Doc) -> None:
        first = next((t for _, t in doc.paragraphs), "")
        if not re.match(r"\*\*TL;DR", first):
            self.hit("reader-tldr-first", 0, "reader profile: first body paragraph must start with **TL;DR**")
        h2 = [h for h in doc.headings if h[1] == 2]
        if len(h2) > READER_MAX_H2:
            self.hit("reader-max-sections", h2[READER_MAX_H2][0], f"reader profile: more than {READER_MAX_H2} H2 sections; split the doc")
        for start, text in doc.paragraphs:
            if len(sentences(doc.prose(text))) > READER_PARAGRAPH_MAX_SENTENCES:
                self.hit("reader-paragraph-length", start, f"reader profile: paragraph over {READER_PARAGRAPH_MAX_SENTENCES} sentences")
        body = "\n".join(doc.lines)
        if not re.search(r"(?i)when to use", body) or not re.search(r"(?i)when not to use", body):
            self.hit("reader-boundaries", 0, "reader profile: add 'When to use' and 'When not to use' sections")


# --- Self-test ----------------------------------------------------------------

GOOD_README = """# geocalc

Great-circle distance, bearing, and midpoint between two coordinates.

## Install

Install from source with pip:

```sh
pip install .
```

## Usage

Compute the distance in kilometers:

```sh
geocalc distance 51.5074 -0.1278 48.8566 2.3522
```

The output is similar to the following:

```text
343.556
```

## License

MIT.
"""

BAD_README = """# The Geocalc Command Line Tool.

## Overview

Great tool!!! Visit https://example.com/geocalc for details. Contact john@gmail.com or call 212-555-9999 at 10.0.0.5 and ask for John Doe about foo.

## License

MIT

## Install

```sh
pip install <package_name>
export TOKEN=sk-ant-api03-abcdefghijklmnopqrstuvwxyz
```

| a | b |
|---|---|
| 1 | 2 |
"""


def self_test() -> int:
    here = Path(__file__).resolve().parent
    types = json.loads((here.parent / "references" / "doc-types.json").read_text(encoding="utf-8"))["types"]
    rules = load_rules(here.parent / "references" / "rules.md")
    c = Checker(rules, types, None)
    c.run(Doc(Path("README.md"), GOOD_README))
    good = c.violations
    c.run(Doc(Path("README.md"), BAD_README))
    bad = c.violations
    ids = {v["msg"].split(":")[0] if v["rule_id"].startswith("structure:") else v["rule_id"] for v in bad}
    expected = {"R-013", "R-014", "R-019", "R-020", "R-021", "R-022", "R-023", "R-018"}
    missing = expected - ids
    ok = not good and not missing
    print(json.dumps({"self_test": "ok" if ok else "fail", "good_violations": good, "bad_ids": sorted(ids), "missing_expected": sorted(missing)}, indent=2))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--profile", choices=["reader"], default=None)
    ap.add_argument("--rules", type=Path, default=Path(__file__).resolve().parent.parent / "references" / "rules.md")
    ap.add_argument("--doc-types", type=Path, default=Path(__file__).resolve().parent.parent / "references" / "doc-types.json")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.paths:
        ap.error("no files given")
    types = json.loads(args.doc_types.read_text(encoding="utf-8"))["types"] if args.doc_types.is_file() else {}
    rules = load_rules(args.rules)
    checker = Checker(rules, types, args.profile)
    files = []
    any_error = False
    for p in args.paths:
        if not p.is_file():
            continue
        dtype = checker.run(Doc(p, p.read_text(encoding="utf-8", errors="replace")))
        files.append({"path": str(p), "type": dtype, "violations": list(checker.violations)})
        any_error |= any(v["level"] == "error" for v in checker.violations)
    print(json.dumps({"ok": not any_error, "files": files}, indent=2))
    return 1 if any_error else 0


if __name__ == "__main__":
    sys.exit(main())

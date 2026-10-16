#!/usr/bin/env python3
"""Check docstring coverage and quality for Python (AST) with regex stubs for Go and TypeScript.

Python checks, per public module, class, function, and method:
  - a docstring exists;
  - the summary is one line ending in '.', '?', or '!';
  - the summary does not start with the symbol's name or "This function/class/method";
  - ``Args:`` names match the signature (ignoring self and cls);
  - ``Returns:`` or ``Yields:`` exists when the function returns a value;
  - ``Raises:`` lists every exception class raised directly in the body;
  - the docstring is not "lazy": token overlap with the name and parameters above
    ``--lazy-threshold`` (default 0.6) means it restates the signature (2102.08486).

Go and TypeScript checks are regex approximations and the output says so
(``"approximate": true``): exported Go funcs and types need a preceding ``//``
comment that starts with the name, bool funcs should say "reports whether";
exported TS functions and classes need a ``/** */`` block whose ``@param`` names
match the parameters.

Usage:
    python3 -I docstring_coverage.py [--lang py|go|ts] [--lazy-threshold 0.6] <paths>...

Output: JSON ``{"lang", "approximate", "coverage": {"documented", "total"},
"missing": [...], "mismatched": [{"symbol", "problem"}], "lazy": [...]}``.
Exit 0 when every public symbol is documented and nothing is mismatched; 1 otherwise.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

DEFAULT_LAZY_THRESHOLD = 0.6  # share of docstring tokens that also appear in name+params
SECTION_RE = re.compile(r"^\s*(Args|Arguments|Returns|Yields|Raises)\s*:\s*$")


def _tokens(s: str) -> set[str]:
    return {t for t in re.findall(r"[a-z]+", re.sub(r"([a-z])([A-Z])", r"\1 \2", s).lower()) if len(t) > 2}


def _sections(doc: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    cur = None
    for line in doc.splitlines():
        m = SECTION_RE.match(line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur and line.strip():
            out[cur].append(line.rstrip())
    return out


def _arg_names(section: list[str]) -> list[str]:
    names = []
    for line in section:
        m = re.match(r"^\s{2,8}(\*{0,2}[A-Za-z_]\w*)\s*(\(|:)", line)
        if m:
            names.append(m.group(1).lstrip("*"))
    return names


def check_python(path: Path, lazy_threshold: float) -> dict:
    src = path.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(src, filename=str(path))
    total = documented = 0
    missing: list[str] = []
    mismatched: list[dict] = []
    lazy: list[str] = []

    def is_public(name: str) -> bool:
        return not name.startswith("_") or name in ("__init__",)

    def visit(node, prefix: str):
        nonlocal total, documented
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = child.name
                if not is_public(name):
                    continue
                sym = f"{prefix}{name}"
                total += 1
                doc = ast.get_docstring(child)
                if not doc:
                    missing.append(sym)
                else:
                    documented += 1
                    check_doc(child, sym, doc)
                if isinstance(child, ast.ClassDef):
                    visit(child, sym + ".")

    def check_doc(node, sym: str, doc: str):
        first = doc.strip().splitlines()[0].strip()
        if not re.search(r"[.?!]$", first):
            mismatched.append({"symbol": sym, "problem": "summary line must end with a period, question mark, or exclamation mark"})
        if len(doc.strip().splitlines()) > 1 and doc.strip().splitlines()[1].strip():
            mismatched.append({"symbol": sym, "problem": "blank line required after the summary line"})
        bare = sym.rsplit(".", 1)[-1]
        if re.match(rf"^(this (function|method|class)|{re.escape(bare)}\b)", first, re.I):
            mismatched.append({"symbol": sym, "problem": "summary restates the symbol name or starts with 'This function/class'"})
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            params = [a.arg for a in node.args.posonlyargs + node.args.args + node.args.kwonlyargs if a.arg not in ("self", "cls")]
            if node.args.vararg:
                params.append(node.args.vararg.arg)
            if node.args.kwarg:
                params.append(node.args.kwarg.arg)
            secs = _sections(doc)
            args_doc = _arg_names(secs.get("Args", secs.get("Arguments", [])))
            if params and ("Args" in secs or "Arguments" in secs):
                if set(args_doc) != set(params):
                    mismatched.append({"symbol": sym, "problem": f"Args lists {sorted(args_doc)} but signature has {sorted(params)}"})
            elif params and bare != "__init__" and len(params) > 1:
                mismatched.append({"symbol": sym, "problem": "Args section missing"})
            returns_value = any(isinstance(n, ast.Return) and n.value is not None for n in ast.walk(node))
            yields = any(isinstance(n, (ast.Yield, ast.YieldFrom)) for n in ast.walk(node))
            is_property = any(getattr(d, "id", getattr(getattr(d, "attr", None), "__str__", lambda: "")()) == "property" for d in node.decorator_list)
            if yields and "Yields" not in secs:
                mismatched.append({"symbol": sym, "problem": "Yields section missing"})
            elif returns_value and not yields and "Returns" not in secs and not is_property and not re.search(r"\b(returns?|gets?|reports whether|checks whether)\b", first, re.I):
                mismatched.append({"symbol": sym, "problem": "Returns section missing"})
            raised = set()
            for n in ast.walk(node):
                if isinstance(n, ast.Raise) and n.exc is not None:
                    target = n.exc.func if isinstance(n.exc, ast.Call) else n.exc
                    if isinstance(target, ast.Name):
                        raised.add(target.id)
                    elif isinstance(target, ast.Attribute):
                        raised.add(target.attr)
            if raised:
                listed = set(re.findall(r"^\s+([A-Za-z_][\w.]*)\s*:", "\n".join(secs.get("Raises", [])), re.M))
                missing_r = sorted(r for r in raised if r not in listed and r.split(".")[-1] not in listed)
                if missing_r:
                    mismatched.append({"symbol": sym, "problem": f"Raises missing {missing_r}"})
            overlap_src = _tokens(bare + " " + " ".join(params))
            doc_tokens = _tokens(first)
            if doc_tokens and overlap_src and len(doc_tokens & overlap_src) / len(doc_tokens) >= lazy_threshold:
                lazy.append(sym)

    mod_doc = ast.get_docstring(tree)
    total += 1
    if mod_doc:
        documented += 1
    else:
        missing.append(f"{path.name} (module)")
    visit(tree, "")
    return {"lang": "py", "approximate": False, "path": str(path), "coverage": {"documented": documented, "total": total}, "missing": missing, "mismatched": mismatched, "lazy": lazy}


GO_DECL = re.compile(r"^func\s+(?:\([^)]*\)\s*)?([A-Z]\w*)\s*\(([^)]*)\)\s*(\([^)]*\)|[\w.*\[\]]+)?|^type\s+([A-Z]\w*)\s", re.M)


def check_go(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    total = documented = 0
    missing, mismatched = [], []
    for i, line in enumerate(lines):
        m = GO_DECL.match(line)
        if not m:
            continue
        name = m.group(1) or m.group(4)
        total += 1
        comment = []
        j = i - 1
        while j >= 0 and lines[j].startswith("//"):
            comment.insert(0, lines[j][2:].strip())
            j -= 1
        if not comment:
            missing.append(name)
            continue
        documented += 1
        if not comment[0].startswith(name):
            mismatched.append({"symbol": name, "problem": f"doc comment must start with the name '{name}'"})
        ret = (m.group(3) or "").strip()
        if ret == "bool" and "reports whether" not in " ".join(comment):
            mismatched.append({"symbol": name, "problem": "boolean func comment should say 'reports whether'"})
    return {"lang": "go", "approximate": True, "path": str(path), "coverage": {"documented": documented, "total": total}, "missing": missing, "mismatched": mismatched, "lazy": []}


TS_DECL = re.compile(r"^export\s+(?:default\s+)?(?:async\s+)?(?:function\s+(\w+)\s*\(([^)]*)\)|class\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>)", re.M)


def check_ts(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    total = documented = 0
    missing, mismatched = [], []
    for m in TS_DECL.finditer(text):
        name = m.group(1) or m.group(3) or m.group(4)
        params_raw = m.group(2) or m.group(5) or ""
        params = [p.split(":")[0].split("=")[0].strip().lstrip("?") for p in params_raw.split(",") if p.strip()]
        params = [p for p in params if p and not p.startswith("{")]
        total += 1
        before = text[: m.start()].rstrip()
        if not before.endswith("*/"):
            missing.append(name)
            continue
        documented += 1
        block = before[before.rfind("/**"):]
        doc_params = re.findall(r"@param\s+(?:\{[^}]*\}\s*)?(\w+)", block)
        if params and set(doc_params) and set(doc_params) != set(params):
            mismatched.append({"symbol": name, "problem": f"@param lists {sorted(set(doc_params))} but signature has {sorted(params)}"})
    return {"lang": "ts", "approximate": True, "path": str(path), "coverage": {"documented": documented, "total": total}, "missing": missing, "mismatched": mismatched, "lazy": []}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--lang", choices=["py", "go", "ts"], default=None, help="default: by file extension")
    ap.add_argument("--lazy-threshold", type=float, default=DEFAULT_LAZY_THRESHOLD)
    args = ap.parse_args(argv)
    files: list[Path] = []
    for p in args.paths:
        files += sorted(p.rglob("*")) if p.is_dir() else [p]
    results = []
    for f in files:
        ext = f.suffix.lstrip(".")
        lang = args.lang or {"py": "py", "go": "go", "ts": "ts", "tsx": "ts"}.get(ext)
        if lang is None or not f.is_file() or "/tests/" in f.as_posix() or f.name.startswith("test_"):
            continue
        if lang != (args.lang or lang) or (args.lang and ext not in {"py": ["py"], "go": ["go"], "ts": ["ts", "tsx"]}[args.lang]):
            continue
        try:
            results.append({"py": check_python, "go": check_go, "ts": check_ts}[lang](f, args.lazy_threshold) if lang == "py" else {"go": check_go, "ts": check_ts}[lang](f))
        except SyntaxError as exc:
            results.append({"lang": lang, "path": str(f), "error": f"syntax error: {exc}"})
    documented = sum(r.get("coverage", {}).get("documented", 0) for r in results)
    total = sum(r.get("coverage", {}).get("total", 0) for r in results)
    bad = any(r.get("missing") or r.get("mismatched") or r.get("error") for r in results)
    print(json.dumps({"coverage": {"documented": documented, "total": total}, "files": results, "ok": not bad}, indent=2))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

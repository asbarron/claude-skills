---
type: regex
target: { source: file, path: src/geo.py }
pattern: '^def [a-z]\w*\(.*\).*:\n\s+"""[A-Z]'
flags: m
match: "count:6"
---

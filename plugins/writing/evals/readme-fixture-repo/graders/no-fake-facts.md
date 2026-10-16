---
type: regex
target: { source: file, path: README.md }
pattern: 'npm install|pip install geocalc[^\s]*\s*$|requirements\.txt|poetry add'
flags: m
match: not_contains
---

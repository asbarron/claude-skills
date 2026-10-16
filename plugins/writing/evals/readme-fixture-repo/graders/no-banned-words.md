---
type: regex
target: { source: file, path: README.md }
pattern: '\b(simply|please|click here|e\.g\.|i\.e\.|currently|in order to|utilize|leverage)\b'
flags: i
match: not_contains
---

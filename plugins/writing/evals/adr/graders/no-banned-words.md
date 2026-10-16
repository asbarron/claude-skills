---
type: regex
target: { source: file, path: doc/arch/adr-002.md }
pattern: '\b(currently|we think|obviously)\b'
flags: i
match: not_contains
---

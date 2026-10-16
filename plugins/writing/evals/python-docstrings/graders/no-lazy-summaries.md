---
type: regex
target: { source: file, path: src/geo.py }
pattern: '"""\s*(This function|Function to|Returns the result)'
match: not_contains
---

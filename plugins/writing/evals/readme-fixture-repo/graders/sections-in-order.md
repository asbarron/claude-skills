---
type: regex
target: { source: file, path: README.md }
pattern: '^#{1,2} .*\n[\s\S]*^#{2,3} (Install|Installation)[\s\S]*^#{2,3} (Usage|Use|Quickstart)[\s\S]*^#{2,3} License'
flags: m
---

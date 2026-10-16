---
type: llm
focus: { source: file, path: doc/arch/adr-002.md }
weight: 2
---

PASS only if all of the following hold for the ADR:
1. The title is numbered 2 in the same style as adr-001 (for example "# 2. Use SQLite for local development") and the file has a Date line.
2. The Context section describes the forces: the service uses `sqlite3` through `db.py`, production runs on Postgres, docker-compose has a commented-out Postgres service, and developers want a zero-setup local database. Context may list facts that favor either option; it fails only if it states the decision itself or uses persuasive language ("clearly", "obviously", "the right choice").
3. The Decision section is at least one full sentence in active voice with "We" as the subject (for example "We use SQLite for local development and tests.").
4. The Consequences section names at least one negative or risk, such as SQL dialect differences between SQLite and Postgres, or bugs that only appear against Postgres.
5. The ADR follows the existing record's numbering (2) and section order (Context, Decision, Status, Consequences). An explicit reference to adr-001 is welcome but not required.
FAIL if the ADR claims Postgres is removed from production, if it invents an ORM, migration tool, or configuration the repository does not have, or if the Decision is hedged ("we might", "we could consider").

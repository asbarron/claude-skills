# Review rubric

Binary checklist for the `docs-reviewer` gate agent and the eval harness judge. Items are yes/no, with ids C (correct), K (complete), U (current), and R (readable). Groups are evaluated in order and weighted correct > complete > current > readable (Aghajani et al., ICSE 2019 and 2020). Any "no" in the first three groups blocks. This file is frozen: humans edit it; the self-improvement loop never does.

## Correct (blocks)

- C1. Every command, flag, path, and symbol the doc names exists in the repository (grep).
- C2. Install instructions match the manifest: build system, scripts, dependencies, supported versions.
- C3. Every runnable example produces the output the doc shows, or the doc does not claim an output.
- C4. No claim contradicts the facts list; no `<!-- unverified -->` marker remains on a behavioral claim.
- C5. Example values are reserved placeholders or fictional data, never values read from the repository's config, environment, or secrets.

## Complete (blocks)

- K1. The first paragraph says what the thing does and who it is for.
- K2. Every section the doc type requires is present (structure check for the type passes).
- K3. Failure modes are documented: errors, exit codes, exceptions, and what to do about them.
- K4. Every public symbol in scope has a docstring or reference entry; every parameter has a type, requiredness, and default where one exists.
- K5. Prerequisites and scope are stated before the first step.

## Current (blocks)

- U1. No time-anchored words (`currently`, `now`, `soon`, `new` or `old` without a version or date).
- U2. The install section states the versions it was verified against.
- U3. Every deprecation names its replacement.

## Readable (suggestions only, at most 5)

- R1. One Diátaxis quadrant per file; no teaching in a how-to, no steps in reference.
- R2. A runnable example appears before explanatory prose in every usage or how-to section.
- R3. Lint error count is zero.
- R4. Headings are sentence case, descriptive, and task-based.
- R5. Reader-profile items pass when `--profile reader` is set.

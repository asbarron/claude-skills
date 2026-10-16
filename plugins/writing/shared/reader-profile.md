# Reader profile

An opt-in layer (`--profile reader`) for a systems-thinking reader with ADHD: they want the whole picture first and the parts in order, and their working memory runs out on dense prose. Apply it on top of the voice rules; where the two conflict, this profile wins. Source: the `adhd-systems-docs` neuron in Ava's vault.

## The shape

```text
TL;DR (one sentence)             <- decide in 5 seconds
Mental model (diagram or table)  <- the whole, before the parts
Why this exists (<= 3 sentences, optional)
Step 1 ... Step N                <- one action, one outcome, one example each
When to use / When not to use    <- boundary conditions
Cheatsheet                       <- scannable reference
```

## The seven rules

1. The first body paragraph starts with **TL;DR:** and is one sentence.
2. A diagram or 3-line table shows the whole before any step. ASCII over rendered diagrams.
3. Paragraphs are at most 3 sentences; one idea per chunk.
4. Visual hierarchy carries the structure: `##` for major sections (at most 7), `###` for sub-steps, bold **keywords** inside sentences, never whole sentences.
5. One concrete example after every rule or principle; "do this, not that" pairs where they fit.
6. Every how-to ends with **When to use** and **When not to use** sections.
7. One Diátaxis quadrant per file; split and link instead of mixing.

## Overrides of the voice rules

| Voice rule | Profile override | Why |
|---|---|---|
| Bold only for UI labels | Bold one keyword per sentence where the eye should land | Scanning, not reading |
| No emoji or decoration | ✅ and ❌ may label "When to use" / "When not to use" items | Fast boundary recognition |
| Headings are plain noun or verb phrases | A "TL;DR" label is allowed as the opener | The reader decides in 5 seconds |

## Checklist before declaring done

- TL;DR present and one sentence; diagram or table above the fold
- At most 7 `##` sections; no paragraph over 3 sentences; most sentences under 20 words
- Example after every principle; "When to use" and "When not to use" present
- Headings descriptive, never "Overview" or "Introduction"; no raw URLs; no nested lists deeper than 2

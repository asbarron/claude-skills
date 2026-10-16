# Rules

Itemized rules the docs skill applies and the self-improvement loop may edit. One row per rule. The loop may only `ADD`, `EDIT`, `UPVOTE`, `DOWNVOTE`, or `RETIRE` rows here; retired rows stay so they cannot be re-added. Caps: 120 active rows, 300 lines.

Columns: `id` stable; `kind` is `lint` (has a deterministic check) or `judge` (reviewer only); `check` names the check (`vale:existence`, `vale:substitution`, `vale:occurrence`, `vale:manual:<Rule>`, `structure:<id>`, or `-` for judge rows); `w` weight 1-5; `hits` times cited; `delta` held-out score change when last edited; `status` `active` or `retired`. For `vale:*` rows the `rule` column holds the human text and the `tokens` column holds the machine list (`a, b, c` for existence; `bad=>good` pairs for substitution).

## Contents

- [Lint rules](#lint-rules)
- [Judge rules](#judge-rules)

## Lint rules

| id | kind | check | rule | tokens | source | w | hits | delta | status |
|---|---|---|---|---|---|---|---|---|---|
| R-001 | lint | vale:existence | Never "please" in instructions. | please | google:tone#politeness | 4 | 0 | 0 | active |
| R-002 | lint | vale:existence | Remove subjective ease words; the meaning survives without them. | simply, simple, easy, easily, quick, quickly, just | google:inclusive-documentation | 4 | 0 | 0 | active |
| R-003 | lint | vale:substitution | Write out Latin abbreviations. | e.g.=>for example, i.e.=>that is, etc.=>a leading 'such as', a.k.a.=>also known as | google:abbreviations | 4 | 0 | 0 | active |
| R-004 | lint | vale:existence | No time-anchored words in product docs. | currently, now supports, as of this writing, at this time, presently, soon, eventually, in the future, does not yet, latest | google:timeless-documentation | 4 | 0 | 0 | active |
| R-005 | lint | vale:substitution | Prefer plain verbs and short phrases. | in order to=>to, utilize=>use, leverage=>use, via=>through, allows you to=>lets you, in spite of the fact that=>although, at this point in time=>now | google:word-list | 3 | 0 | 0 | active |
| R-006 | lint | vale:existence | No "let's" or "we" for reader actions. | let's, let us | google:person | 3 | 0 | 0 | active |
| R-007 | lint | vale:existence | No directional language for positions. | above, below, left-hand, right-hand | google:accessibility | 2 | 0 | 0 | active |
| R-008 | lint | vale:existence | "Click here", "this document", and bare URLs are not link text. | click here, this document, see here | google:link-text | 4 | 0 | 0 | active |
| R-009 | lint | vale:substitution | Inclusive replacements. | whitelist=>allowlist, blacklist=>denylist, master/slave=>primary/replica, sanity check=>quick check, dummy=>placeholder, man-hours=>person-hours, mankind=>humanity | google:inclusive-documentation | 4 | 0 | 0 | active |
| R-010 | lint | vale:substitution | UI verbs and nouns. | click on=>click, uncheck=>clear, deselect=>clear, hover over=>hold the pointer over, hit=>click, e-mail=>email, repo=>repository, file name=>filename, walk-through=>walkthrough | google:word-list | 2 | 0 | 0 | active |
| R-011 | lint | vale:existence | "Should", "may", and "will" are ambiguous; use "must", "can", "might", or present tense. | should, may, will be, would | google:word-list | 2 | 0 | 0 | active |
| R-012 | lint | vale:existence | No "there is" or "there are"; move the real subject forward. | there is, there are, there were | google:tech-writing-one | 2 | 0 | 0 | active |
| R-013 | lint | structure:heading-sentence-case | Headings use sentence case. | - | google:headings | 4 | 0 | 0 | active |
| R-014 | lint | structure:heading-no-end-punct | Headings have no end punctuation. | - | google:headings | 3 | 0 | 0 | active |
| R-015 | lint | structure:one-h1 | Exactly one H1 per file; never skip a level. | - | google:headings | 3 | 0 | 0 | active |
| R-016 | lint | structure:sentence-length | Sentences stay under 26 words. | - | google:accessibility#readability | 2 | 0 | 0 | active |
| R-017 | lint | structure:paragraph-length | Paragraphs stay at or under 6 sentences and 150 words. | - | google:paragraph-structure, fplg | 2 | 0 | 0 | active |
| R-018 | lint | structure:placeholder-case | Placeholders are UPPER_SNAKE_CASE, never `<angle>` or `my_`. | - | google:placeholders | 3 | 0 | 0 | active |
| R-019 | lint | structure:reserved-example-data | Example data comes from reserved pools: example.com, 192.0.2.x, 800-555-01xx, names Alex, Dana, Kai, Quinn, Sasha, Yuri. No foo, bar, baz, John Doe. | - | google:examples | 3 | 0 | 0 | active |
| R-020 | lint | structure:no-secret-shapes | No values shaped like secrets (sk-, AKIA, ghp_, xox, -----BEGIN, 32+ hex). | - | writing:security | 5 | 0 | 0 | active |
| R-021 | lint | structure:readme-sections | README order: name and one-liner, install, usage, detail, license. Usage before API. | - | make-a-readme, art-of-readme | 4 | 0 | 0 | active |
| R-022 | lint | structure:raw-url-in-prose | No raw URLs in prose; use descriptive link text. | - | google:link-text | 2 | 0 | 0 | active |
| R-023 | lint | structure:table-intro | Every table follows an introducing sentence. | - | google:tables | 1 | 0 | 0 | active |
| R-024 | lint | structure:changelog-format | Changelog: `[Unreleased]`, `## [x.y.z] - YYYY-MM-DD`, sections Added/Changed/Deprecated/Removed/Fixed/Security. | - | keepachangelog | 3 | 0 | 0 | active |
| R-025 | lint | structure:adr-sections | ADR sections in order: Title, Context, Decision, Status, Consequences; Status in Proposed/Accepted/Deprecated/Superseded. | - | nygard | 3 | 0 | 0 | active |

## Judge rules

| id | kind | check | rule | tokens | source | w | hits | delta | status |
|---|---|---|---|---|---|---|---|---|---|
| R-101 | judge | - | Every command, flag, path, and symbol the doc names exists in the repo. | - | rubric#C1 | 5 | 0 | 0 | active |
| R-102 | judge | - | Install instructions match the manifest (build system, scripts, dependencies) rather than a generic pattern. | - | rubric#C2 | 5 | 0 | 0 | active |
| R-103 | judge | - | The first paragraph says what the thing does and who it is for; no marketing adjectives. | - | rubric#K1, art-of-readme | 4 | 0 | 0 | active |
| R-104 | judge | - | A runnable example appears before explanatory prose in every how-to or usage section. | - | rubric#R2, google:examples | 4 | 0 | 0 | active |
| R-105 | judge | - | Failure modes are documented: errors, exit codes, exceptions, and what to do about them. | - | rubric#K3, docstrings-consensus | 4 | 0 | 0 | active |
| R-106 | judge | - | One Diátaxis quadrant per document; no teaching inside a how-to, no steps inside reference. | - | rubric#R1, diataxis | 3 | 0 | 0 | active |
| R-107 | judge | - | A docstring summary adds information beyond the name and signature. | - | rubric#K2, 2102.08486 | 3 | 0 | 0 | active |
| R-108 | judge | - | Condition or location comes before the action in instructions. | - | google:sentence-structure | 2 | 0 | 0 | active |
| R-109 | judge | - | Each section stands alone for a reader arriving cold: names the subject, states prerequisites. | - | eppo | 2 | 0 | 0 | active |
| R-110 | judge | - | Example values never come from the repo's real config, env, or secrets. | - | writing:security | 5 | 0 | 0 | active |
| R-111 | judge | - | An ADR's Context lists the forces as facts and never argues; advocacy belongs in Decision and trade-offs in Consequences. | - | rubric#K5, nygard | 3 | 0 | 0 | active |

## Structure rules without a Vale equivalent

| id | kind | check | rule | tokens | source | w | hits | delta | status |
|---|---|---|---|---|---|---|---|---|---|
| R-026 | lint | structure:doc-type | The document matches its type's shape from doc-types.json: required sections, H1 form, forbidden phrases, steps or tables where the quadrant needs them. | - | diataxis, doc-types.json | 4 | 0 | 0 | active |
| R-030 | lint | structure:reader-tldr-first | Reader profile: the first body paragraph starts with **TL;DR**. | - | vault:adhd-systems-docs | 3 | 0 | 0 | active |
| R-031 | lint | structure:reader-max-sections | Reader profile: at most 7 H2 sections per file. | - | vault:adhd-systems-docs | 2 | 0 | 0 | active |
| R-032 | lint | structure:reader-paragraph-length | Reader profile: paragraphs stay at or under 3 sentences. | - | vault:adhd-systems-docs | 3 | 0 | 0 | active |
| R-033 | lint | structure:reader-boundaries | Reader profile: "When to use" and "When not to use" sections are present. | - | vault:adhd-systems-docs | 3 | 0 | 0 | active |

## Hand-written Vale rules

Rules that need regex features the generator does not produce. The loop may UPVOTE, DOWNVOTE, or RETIRE these rows; retiring one makes lint-docs.sh drop its alerts.

| id | kind | check | rule | tokens | source | w | hits | delta | status |
|---|---|---|---|---|---|---|---|---|---|
| R-034 | lint | vale:manual:Placeholders | Placeholders in prose and code blocks are UPPER_SNAKE_CASE; never `<angle>` or `my_` prefixes. | - | google:placeholders | 4 | 0 | 0 | active |
| R-035 | lint | vale:manual:HeadingSentenceCase | Headings use sentence case (Vale capitalization check). | - | google:headings | 4 | 0 | 0 | active |
| R-036 | lint | vale:manual:HeadingPunctuation | Headings have no end punctuation (Vale check). | - | google:headings | 3 | 0 | 0 | active |
| R-037 | lint | vale:manual:CodeInflection | Never pluralize or possessive-inflect code; add a noun instead. | - | google:code-in-text#grammar | 3 | 0 | 0 | active |
| R-038 | lint | vale:manual:Exclamation | Avoid exclamation marks. | - | google:tone, google:accessibility | 2 | 0 | 0 | active |

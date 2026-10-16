# Conflicts between guides

Where the canonical guides disagree, and which position the docs skill takes. The skill default is the rule to apply; the positions are there so a reviewer can tell a deliberate choice from a mistake. FPLG is the Federal Plain Language Guidelines.

## Vocabulary

The following table lists the word-choice conflicts:

| Topic | Positions | Skill default |
|---|---|---|
| "click" vs "select" | Microsoft: never input-specific verbs; "select" for buttons, links, and keys. Google: "click" for mouse targets, "tap" on touch devices, "press" for keys, "select" for list items and checkboxes. | Follow the platform's own guide. If unknown, "select" for UI elements and "press" for keys. "Click" is fine in a document that targets desktop browsers. |
| Contractions | Microsoft: use freely, including `let's`. Google: common two-word ones only, never `let's`, prefer negative contractions. FPLG: when appropriate. Nygard ADRs: formal full sentences. Diátaxis reference: austere. | Google's rule in tutorials, how-tos, and READMEs. No contractions in ADRs and reference pages. |
| `should` | Google word list: avoid, ambiguous. FPLG and RFC usage: a recommendation. | Avoid in prose. In requirement statements, runbooks, and specifications, use `must`, `must not`, `may`, and `should` with the FPLG meanings and state that convention once. |
| `may` | Google: reserved for policy or legal permission; use "can" or "might". FPLG: a discretionary action. | "Can" for ability and "might" for possibility in prose. `may` only inside the requirement-verb convention. |
| `please` | Google: never in instructions. Microsoft: not banned, but no top-ten example uses it. | Never. |
| "New" and "old" | Google timeless: banned without a reference point. Keep a Changelog: every entry sits under a dated version, so the reference point exists. | Banned in product docs. Fine in a changelog entry under a dated version heading, and in release notes. |

## Voice

The following table lists the conflicts about who speaks and in what mood:

| Topic | Positions | Skill default |
|---|---|---|
| Tutorial voice | Diátaxis: "we", tutor and learner together. Google: "you", never `let's` or "we" for reader actions. | "We" inside tutorials only; "you" everywhere else. `let's` stays banned in every type. |
| Passive voice | Google: active by default, passive when the actor is irrelevant. Microsoft and FPLG: active. | Active. The three Google exceptions (emphasize the object, de-emphasize the actor, actor irrelevant) are the only sanctioned passives, and the reviewer decides, not the linter. |
| Docstring summary style | Google Python: descriptive or imperative, consistent per file. PEP 257: imperative. Go, Rust, and Google API reference: third-person present. | Third-person present in every language. A Python project with an existing imperative convention keeps it. |

## Structure

The following table lists the conflicts about page shape:

| Topic | Positions | Skill default |
|---|---|---|
| README length | Make a README: too long is better than too short. Art of README: as short as it can be without being any shorter. Both move detail out of the README. | Art of README. Keep the README to the cognitive funnel and move detail to `docs/`. When a project has no other docs, the README holds the detail. |
| Heading forms | Google: avoid gerund-first headings. Diátaxis: "Integrating X" is the ambiguous middle; "How to integrate X" is right for how-tos; bare nouns are right for reference and explanation. | Map by quadrant. How-to and runbook: "How to X" or a bare infinitive. Tutorial: bare infinitive. Reference and explanation: noun phrase. Never an -ing word first. |
| Code in headings | Google: avoid. Rust and Go reference pages are named by code identifiers. | Reference pages are exempt. Everywhere else, pair the identifier with a noun or write the heading in words. |
| Links in headings | Google: avoid. Write the Docs: descriptive headings and meaningful link text, which a heading link undermines. | No links in headings anywhere. |
| Notices | Google: minimize, never stack. Stripe and `Twilio`: frequent warning notices in reference. | Google's rule in prose documents. A reference page can carry one constraint notice per operation. |

## Formatting

The following table lists the punctuation and format conflicts:

| Topic | Positions | Skill default |
|---|---|---|
| Dashes | Microsoft: the em dash with no spaces is the house dash. Google: a dash before a conjunctive adverb and in placeholder examples, commas and periods elsewhere. Several LLM style guides ban em dashes outright. | No em dashes. Use a comma, a period, a colon, or parentheses. |
| Menu path ">" | Google: bold the whole path once, non-breaking spaces, an "and then" label for screen readers. Microsoft: spaces around ">", brackets not bold, and a warning that screen readers skip the symbol. | Google's form in Markdown: `**File > New > Document**`. When the doc targets HTML with a screen-reader audience, add the label. |
| Time formats | Google: "9:30 AM", 12-hour, ISO 8601 for numeric dates only. Keep a Changelog: ISO dates always. | ISO 8601 for every date in changelogs, ADR status lines, and tables; "July 8, 2025" in prose; "9:30 AM" for times unless matching UI or code. |
| Alt text length | Google: at most 155 characters. Others silent. | 155 characters. |

## Limits

The following table lists the conflicts about numeric ceilings:

| Topic | Positions | Skill default |
|---|---|---|
| Sentence length | Google: under 26 words. Microsoft and FPLG: short, no number. Google Technical Writing: one idea. | 26 words is the hard ceiling the linter enforces; about 20 is the warning line; one idea per sentence is the judge's test. |
| Paragraph length | Google: 5 to 6 sentences. Microsoft: 3 to 7 lines. FPLG: 150 words, 3 to 8 sentences, never over 250. Google Technical Writing: 3 to 5 sentences. | 6 sentences or 150 words, whichever comes first; 250 words is an error. |
| Heading depth | FPLG: at most three levels. Google: never skip a level, no number given. | Three levels (H1 to H3) in a single page; a needed H4 means the page splits. |

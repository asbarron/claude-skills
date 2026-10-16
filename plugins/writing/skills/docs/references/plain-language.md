# Plain language

The numeric limits and requirement verbs from the Federal Plain Language Guidelines, and the sentence, paragraph, and word rules from Google Technical Writing One. The house style already fixes sentence and paragraph ceilings; this page gives the finer limits and the techniques.

## Numeric limits

The following table lists the limits the guidelines state as numbers:

| Rule | Do / Don't | Source |
|---|---|---|
| At most three heading levels | H1, H2, H3; promote an H4 to its own page | fplg:organize#headings |
| Abbreviations per document: no more than three, preferably two | Spell the term out instead of coining a fourth | fplg:words#abbreviations |
| Paragraphs: at most 150 words in three to eight sentences, never longer than 250 | | fplg:paragraphs#short |
| Cross-references: at most one per section | Define on the page instead of sending the reader away | fplg:other#cross-references |
| Web readers read about 18% of a page; to get them to read half your words, hold the page to 110 words or fewer | Put the answer first; everything after it is optional reading | fplg:web#scan |
| Readers decide in about five seconds whether a page helps them | The first sentence states what the page is for | fplg:web#scan |
| One idea per sentence | The guideline's own example trims a sentence to 22 words | fplg:sentences#short |
| Address one person, not a group | Do: "You must file the form." Don't: `Applicants must file the form.` | fplg:organize#one-person |

## Requirement verbs

Replace `shall`, which is "officious and obsolete" and ambiguous between obligation and prediction. The following table lists the verbs and their meanings:

| Verb | Meaning | Source |
|---|---|---|
| `must` | An obligation: the reader has to do it | fplg:words#must |
| `must not` | A prohibition | fplg:words#must |
| `may` | A discretionary action: the reader is allowed to | fplg:words#must |
| `should` | A recommendation | fplg:words#must |
| `shall` | Never; the US Courts are replacing it with `must` | fplg:words#must |

In ordinary prose the house style avoids `should` and `may` as ambiguous. In requirement statements, runbooks, and specifications, use the four verbs with the meanings in the table and say so once near the top of the document.

## Sentences

The following table lists the sentence techniques from Technical Writing One:

| Rule | Do / Don't | Source |
|---|---|---|
| Strong, specific verbs instead of be, occur, happen | Do: "Dividing by zero raises the exception." Don't: `The exception occurs when dividing by zero.` | google:tech-writing/one/clear-sentences |
| Delete `there is` and `there are`; move the real subject forward | Do: "The buffer holds 64 entries." Don't: `There is a buffer that holds 64 entries.` | google:tech-writing/one/clear-sentences |
| Minimize subjective adjectives and adverbs; replace them with numbers | Do: "handles 2,000 requests per second" Don't: `blazingly fast` | google:tech-writing/one/clear-sentences |
| Convert a sentence that contains "or" or an embedded list into a list | | google:tech-writing/one/short-sentences |
| Cut wordy phrases | Do: "now", "find", "can", "although", "produces" Don't: `at this point in time`, `determine the location of`, `is able to`, `in spite of the fact that`, `causes the production of` | google:tech-writing/one/short-sentences |
| Split a subordinate clause that branches to a new idea: which, that, because, whose, until, unless, since | One sentence per idea | google:tech-writing/one/short-sentences |
| "That" is essential and takes no comma; "which" is nonessential and takes a comma; test with a pause | Do: "The file that you edited is saved." "The file, which is small, is saved." | google:tech-writing/one/short-sentences |
| Define new terms; use terms consistently; spell out acronyms; replace ambiguous pronouns | Do: "the config file" Don't: `it` after two nouns | google:tech-writing/one/words |
| Keep subject, verb, and object close together; avoid double negatives and exceptions to exceptions; put the main idea before exceptions and conditions | | fplg:sentences |
| Avoid hidden verbs and nouns made from verbs | Do: "decide" Don't: `make a decision` | fplg:words#hidden-verbs |
| Don't use slashes between alternatives | Do: "a user or a group" Don't: `user/group` | fplg:words#slashes |

## Paragraphs

The following table lists the paragraph rules from Technical Writing One and the guidelines:

| Rule | Do / Don't | Source |
|---|---|---|
| The opening sentence states the point; the paragraph answers what, why, and how | | google:tech-writing/one/paragraphs |
| One topic per paragraph; three to five sentences; split at about seven | | google:tech-writing/one/paragraphs |
| Avoid runs of one-sentence paragraphs | Merge or restructure as a list | google:tech-writing/one/paragraphs |
| Every paragraph has a topic sentence; use transition words between paragraphs | Do: "However", "As a result", "In contrast" at the start of the next paragraph | fplg:paragraphs |
| A document states scope, audience, and key points up front, then breaks into sections | | google:tech-writing/one/documents |
| Use examples, lists, tables, and emphasis as reading aids; design for scanning | | fplg:other-aids |

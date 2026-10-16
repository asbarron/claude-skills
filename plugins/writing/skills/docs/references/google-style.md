# Google developer documentation style

Google's rules beyond the house style in `shared/voice.md`: tone, structure, procedures, UI, links, accessibility, translation, timeless phrasing, mechanics, and the word list. Source slugs name pages under the Google developer documentation style guide.

## Contents

- [Tone](#tone)
- [Person, voice, and tense](#person-voice-and-tense)
- [Sentences and paragraphs](#sentences-and-paragraphs)
- [Headings](#headings)
- [Procedures](#procedures)
- [Lists](#lists)
- [Tables](#tables)
- [UI elements](#ui-elements)
- [Links and notices](#links-and-notices)
- [Accessibility](#accessibility)
- [Global audience](#global-audience)
- [Inclusive language](#inclusive-language)
- [Timeless writing](#timeless-writing)
- [Mechanics](#mechanics)
- [Word list](#word-list)

## Tone

Write like a knowledgeable friend who respects the reader's time. The following table lists the tone rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Conversational and friendly without being frivolous; not a textbook, not a salesperson | Do: "To get the user's phone number, call `user.phoneNumber.get`." Don't: a pop-culture joke about the call | google:tone |
| Don't write exactly as you speak; speech is wordier | Read the sentence aloud, then cut what you'd never type | google:tone |
| No humor, slang, cuteness, or internet abbreviations | Don't: `tl;dr`, `ymmv` | google:tone#humor |
| No `please` in instructions or cross-references | Do: "To view the document, click **View**." Don't: `please click View` | google:tone#politeness |
| Avoid exclamation marks | Do: "The build passed." | google:tone |
| Avoid buzzwords, jargon, and inflated wording | Do: "call the `get` method" Don't: `via the simple expedient of using` | google:jargon |
| Delete ease words in procedures: `simply`, `easy`, `quickly` | The meaning survives without them | google:inclusive-documentation |
| No placeholder phrases | Don't: `please note`, `at this time` | google:tone |
| No `let's` | Do: "Consider adding a description to your table." Don't: `Let's add a description to our table.` | google:person |
| Avoid figurative language, metaphors, idioms, and ableist language | Do: "the affected area" Don't: `blast radius` | google:inclusive-documentation |
| Vary sentence openings | Don't start every sentence with "You can" or "To do" | google:tone |
| Don't overuse "However" and "Nonetheless" | Reorder or merge the sentences instead | google:tone |

## Person, voice, and tense

The house style sets second person, active voice, and present tense. The following table lists the carve-outs and edge cases:

| Rule | Do / Don't | Source |
|---|---|---|
| "We" only for the authoring organization, with a clear antecedent | Do: "Example Organization provides A, but we don't provide C." | google:person |
| Third person for what software or end users do; "you" for what the reader does | Do: "The server sends an acknowledgment. You can inspect it in the log." | google:person |
| State the audience near the beginning and stay consistent | Do: "This guide is for developers who deploy to Kubernetes." | google:person |
| Imperative mood in procedures, and in running text once the addressee is established | Do: "Click **Submit**." | google:person |
| Passive is acceptable to emphasize the object, de-emphasize the actor, or when the actor is irrelevant | Do: "The file is saved." "Over 50 conflicts were found in the file." "The database was purged in January." | google:voice#exceptions |
| Future tense only for actions that happen later, such as scheduled or asynchronous work | Do: "The file is archived the next time the backup runs." Don't: `The server will send` for general behavior | google:tense |
| Never future tense for future releases | Don't: `Version 3 will add` | google:future |
| Avoid the hypothetical `would` | Do: "If you send X, the server removes you." Don't: `The server would then remove you.` | google:tense |

## Sentences and paragraphs

Length limits live in the house style. The following table lists the structural rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Condition, circumstance, or goal before the instruction | Do: "For more information, see X." Don't: `See X for more information.` | google:sentence-structure |
| Most important information in the first sentence of the paragraph | Lead with the fact, follow with the reason | google:paragraph-structure |
| One-sentence paragraphs are acceptable; more than 5 or 6 sentences is a warning sign | Split at the second idea | google:paragraph-structure |
| Avoid double negatives | Do: "The flag is optional." Don't: `The flag is not required to be absent.` | google:accessibility |

## Headings

Sentence case and no end punctuation are house rules. The following table lists the rest:

| Rule | Do / Don't | Source |
|---|---|---|
| Task-based headings start with a bare infinitive | Do: "Create an instance" Don't: `Creating an instance` | google:headings |
| Conceptual headings are noun phrases | Do: "Migration to Google Cloud" Don't: `Migrating to Google Cloud` | google:headings |
| Avoid starting any heading with an -ing word; "Billing" or "Pricing" is acceptable when nothing else fits | Do: "Transfer data sets" | google:headings |
| Optional sections start with "Optional:" | Do: "Optional: Customize your alias" | google:headings |
| One h1 per page; never skip a level; no empty headings; never pick a level for its look | | google:headings |
| Don't number headings | Don't: `Step 1: Install` | google:headings |
| Avoid code, links, abbreviations, and heavy punctuation in headings; if code is unavoidable, pair it with a descriptive noun | Do: "The `gcloud` command" | google:headings |
| Introduce subsections with "the following sections", not "this section" | | google:headings |
| Every heading is unique and descriptive; a short sentence sits under each one; never an h3 directly under an h2 | | google:accessibility |

## Procedures

A procedure is a numbered sequence of steps with one action each. The following table lists the rules for writing one:

| Rule | Do / Don't | Source |
|---|---|---|
| The intro sentence adds context beyond the heading and is imperative or complete; colon if the steps follow directly, period if a note intervenes | Do: "To customize the buttons, follow these steps:" or "Customize the buttons:" Don't: `To customize the buttons:` | google:procedures#introductory |
| "Do the following" is an accepted intro phrase | Do: "To set up billing, do the following:" | google:whats-new |
| One action per step; each instruction is its own list item; split long steps | | google:procedures |
| A single-step procedure is one sentence in a bulleted list, not a numbered list | Do: "- To clear the log, click **Clear log**." | google:procedures#single-step |
| Sub-steps use lowercase letters, then lowercase roman numerals | a, b, c; then i, ii, iii | google:procedures |
| Within a complex step: action, command, placeholder explanation, detail, output, then the result in its own paragraph | | google:procedures#order |
| Menu sequences collapse with ">" in bold | Do: "Click **File > New > Document**." | google:procedures |
| Document one method: the shortest, keyboard-only, best-known one; alternatives go on separate pages or tabs | | google:procedures#multiple-ways |
| Don't repeat a procedure; refer to it | Do: "Create a user as you did in the previous step." | google:procedures |
| Optional steps start with "Optional:" and a colon, never "(Optional)" | Do: "Optional: Add a label." | google:procedures |
| Location before action | Do: "In Google Docs, click **File > New**." Don't: `Click File > New in Google Docs.` | google:procedures |
| Goal before action with "To ..."; if that makes a required step look optional, use the colon form instead | Do: "To start a new document, click **File > New**." | google:procedures |
| Result and justification come after the action, in the same paragraph | Do: "Click **Run**. The query results appear." | google:procedures |
| Each step starts with an imperative verb, is a complete sentence, and matches the verb form of its neighbors | | google:procedures |
| Include the Enter press in the step; leave out keyboard shortcuts | Do: "Enter `custom function`, and then press **Enter**." | google:procedures |
| No `please`; no `above` or `below`; no "run the following command" as the whole intro, say what the command does | Do: "Create the bucket:" | google:procedures |
| Prerequisites come before the procedure, never in a note mid-procedure | | google:procedures |

## Lists

Numbered for sequences and bulleted otherwise is a house rule. The following table lists the formatting rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Description list for term and definition pairs; a table when each item has 3 or more properties | | google:lists |
| A single item is not a list | Write it as a sentence, or as one bulleted step in a procedure | google:lists |
| The intro is a full sentence, not a fragment the items complete; colon if the list follows directly | Do: "Use the **Submit** button for any of the following purposes:" Don't: `Use the Submit button to:` | google:lists#introducing |
| Capitalize each item; end punctuation unless the item is a single word, has no verb, is all code, or is all link text; never mix within one list | | google:lists#punctuation |
| Run-in headings: bold term, then a period or colon applied consistently; after a colon the description starts lowercase; no dashes between term and description | Do: "**Crow**: the other best kind of bird" | google:lists#run-in |
| In prose, never end a list with `etc.` or `and so on`; signal a partial list up front with "such as" | Do: "formats such as JSON and YAML" | google:lists#prose |

## Tables

A table holds items that each carry several facts. The following table lists the rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Use a table when each item has 3 or more pieces of data; a list for 1; a description list for 2 | | google:tables |
| Never for layout, code, splitting a long list into columns, a single column, a single row, or inside a procedure | | google:tables |
| Introduce every table with a complete sentence; colon if the table follows directly | Do: "The following table lists the supported regions:" | google:tables |
| Caption only when several tables sit close together: "**Table 1.** Prehistoric birds", sentence case, no period; refer to it as "table 1" | | google:tables#captions |
| Header cells only in the first row or column, with a scope attribute; no merged cells | | google:accessibility |
| Column headings: sentence case, concise, no end punctuation | | google:tables |
| Don't link to a table; refer to it by number; footnotes go directly after the table | | google:tables |

## UI elements

Bold for visible labels is a house rule. The following table lists how to describe interaction:

| Rule | Do / Don't | Source |
|---|---|---|
| Write in terms of the task, not the widget, when possible | Do: "Refresh the page." over "Click **Refresh**." | google:ui-elements |
| Bold buttons, menus, dialog boxes, tabs, and fields; don't bold product or feature names | Do: "In the **New project** window, select the **New activity** checkbox, and then click **Next**." | google:ui-elements |
| Match on-screen capitalization; if the label is all caps, use sentence case | Do: "Click **Refresh**." Don't: `Click REFRESH.` | google:ui-elements |
| Refer to a button by its label alone: no "the", no "button", no trailing ellipsis | Do: "Click **OK**." Don't: `Click the "OK" button.` or `Browse...` | google:ui-elements |
| Never use a label as a verb or noun | Do: "In the **Name** field, enter a name." Don't: `Name the account.` | google:ui-elements |
| Icons: use the name from the icon's hover text, icon before the name; never describe the picture | Do: "Click **Notifications**." Don't: `Click the bell icon.`, `the hamburger`, `the zippy` | google:ui-elements |
| Outside a procedure, mention a UI element with its location | Do: "in the **Current jobs** section of the service console" | google:ui-elements |
| Verbs: click (buttons and links; "tap" on touch devices), select (UI items, checkboxes, lists), choose (generic), enter (text, over "type"), press (keys), hold the pointer over, drag, go to, turn on or off, clear (checkbox) | Do: "Select the **Enable** checkbox." "Press Control+C (or Command+C on macOS)." | google:ui-elements |
| "click", never `click on`; hyphenate right-click and double-click | | google:word-list#click |
| Don't use "toggle" as a verb | Do: "Click the **Wi-Fi** toggle to the on position." | google:ui-elements |
| "in" for dialog boxes, fields, lists, menus, panes, and windows; "on" for pages, tabs, and toolbars | Do: "On the **Settings** tab, in the **Name** field, enter a name." | google:ui-elements |
| Keys in a `kbd` element, in MODIFIER+KEY form with spelled-out modifiers | Do: "Control+V" Don't: `Ctrl+V` | google:ui-elements |
| Never directional language for UI positions; add context or a screenshot instead | Do: "In the preceding diagram" Don't: `In the diagram above` | google:accessibility |

## Links and notices

Descriptive link text is a house rule. The following table lists the rules for notices, link text, and cross-references:

| Rule | Do / Don't | Source |
|---|---|---|
| Notice types: Note (aside), Caution (proceed carefully), Warning (irreversible, data loss), Success (dynamic content only) | | google:notices |
| Use a note only for information the reader can skip; never for prerequisites, steps, must-know facts, cross-references, or results | | google:notices |
| Minimize notices; never two in a row; never nested; write the text as a paragraph first and promote it only if needed | | google:notices |
| Markdown notice markup is a bold label | Do: "**Caution**: This action deletes the bucket." | google:notices |
| Link text is the exact page title or a short phrase with the key words first; never a sentence, a URL, or a vague phrase | Do: "see [Load balancing and scaling](https://example.com/lb)" Don't: `click here`, `this document` | google:link-text |
| Include the abbreviation and the code element's noun inside the link | Do: "[Google Kubernetes Engine (GKE)](https://example.com/gke)", "the [`--hostname` flag](https://example.com/flags)" | google:link-text |
| One link text, one target; avoid duplicate links to one target except section links on long pages | | google:cross-references |
| Cross-reference pattern: "For more information, see X" or "For more information about Y, see X"; "about", never "on"; "see", never "refer to" or "check out" | | google:cross-references |
| Each link is cognitive load; define briefly on the page instead of linking when you can | | google:cross-references |
| Punctuation outside the link; no quotation marks around link text; unlinked titles in quotes for sections and italics for books | Do: "see [Test your code](https://example.com/test)." | google:link-text |
| Say in text when a link downloads a file, opens a new tab, or leaves the site; never force a new tab | Do: "the [schema (JSON)](https://example.com/schema.json)" | google:link-text |

## Accessibility

Alt text and no information only in images are house rules. The following table lists the rest:

| Rule | Do / Don't | Source |
|---|---|---|
| Usable by keyboard alone; semantic HTML; em only for emphasis | | google:accessibility |
| Avoid camel case and all caps in prose; avoid exclamation marks, question marks, and semicolons, which some screen readers skip | | google:accessibility |
| "and", not "&", except in UI labels, tight table headers, and code | | google:accessibility |
| Alt text: a full sentence or noun phrase with punctuation; no "Image of"; decorative images get an empty alt; the same alt for a repeated icon; a caption is not alt text | Do: `alt="Login screen with email and password fields."` Don't: `alt="Image of a login screen"` | google:images#alt |
| SVG over PNG; MP4 over animated GIF; no image maps | | google:images |
| Screenshots: crop to the relevant area; mask personal data with a fully opaque overlay, not a blur; no explanatory text inside the image; consistent OS and style | | google:images#screenshots |
| Figure captions are complete sentences: "**Figure 1.** Description."; refer to "figure 1", never `the image above` | | google:images#captions |
| Buttons by label; icon-only controls get an aria-label | Do: "Click **Notifications**." | google:accessibility |
| Never convey state by color or icon alone; no interactions that need a pointer | | google:accessibility |
| Test without sound, images, color, and the mouse, and with magnification | | google:accessibility |

## Global audience

Text gets translated by people and machines. The following table lists the rules that keep it translatable:

| Rule | Do / Don't | Source |
|---|---|---|
| Prefer plain words | Do: "start", "so", "use", "some" Don't: `commence`, `consequently`, `utilize`, `a number of` | google:translation |
| Subject, verb, object, with the main subject and verb near the start | | google:translation |
| Avoid phrasal verbs when one verb works; "set up", "log in", and "sign in" are exceptions | Do: "remove" Don't: `take out` | google:translation |
| At most two noun modifiers before a noun | Do: "A cloud-native DevSecOps pipeline in a hybrid environment" Don't: `A hybrid cloud-native DevSecOps pipeline` | google:translation |
| Put "only" directly before the word it modifies | Do: "Request no more than one token." Don't: `Only request one token.` | google:translation |
| Avoid gerunds | Do: "describes how to set up replication" Don't: `describes setting up replication` | google:translation |
| Use each word in its primary sense; don't use one word as both noun and verb nearby | | google:translation |
| Keep helper words: "that", "then", "of"; never drop relative pronouns | Do: "the rules that you previously defined", "all of the datasets" | google:translation |
| Replace ambiguous pronouns with the noun; put a noun after "this" or "that" | Do: "make sure that the ad is targeted", "this setting" | google:translation |
| Say what readers can do, not what they can't | Do: "Enter up to 20 characters." Don't: `Don't enter more than 20 characters.` | google:translation |
| Same term, same capitalization, same phrasing for the same thing everywhere | | google:translation |
| No idioms, slang, humor, holidays, sports, seasons, or culture-bound references | Don't: `ballpark figure`, `back burner`, `summer release` | google:translation |

## Inclusive language

The house style covers allowlist, primary and replica, singular "they", and the ease words. The following table lists the other replacements; the left term is the one to avoid:

| Rule | Do / Don't | Source |
|---|---|---|
| `dummy variable` | placeholder | google:word-list |
| `man-hours`, `mankind` | person-hours, humanity | google:inclusive-documentation |
| `crazy`, `insane`, `dumb`, `blind to`, `cripple` | baffling, or the precise effect: "slows down the service" | google:inclusive-documentation |
| `hangs` | doesn't respond | google:word-list |
| `hover over`, `hit` | hold the pointer over, point to; click | google:word-list#hover |
| `native`, `non-native`, `first-class citizen` | built-in, supported, or the specific property | google:inclusive-documentation |
| `blast radius`, `ingest`, `off-the-shelf`, `STONITH`, `pets vs cattle` | affected area; import or load; ready-made; "fence failed nodes"; describe the model | google:inclusive-documentation |
| `the elderly`, `the disabled`, `wheelchair-bound`, `suffering from` | older adults; people with disabilities; uses a wheelchair; living with | google:inclusive-documentation |
| `normal` or `healthy` for people without disabilities; euphemisms such as `differently abled` | "people without disabilities" | google:inclusive-documentation |
| Roles tied to a gender or ethnicity in examples | Rotate names (Alex, Dana, Kai, Quinn, Sasha, Yuri) and roles; use "they" | google:inclusive-documentation |
| Subjective words that assume the reader's experience: `careful`, `thorough`, `proper`, and the ease words | Delete, or state the fact: "takes about two minutes" | google:inclusive-documentation |
| Jargon, including vague words such as `solution`, `support`, `workload` | Write around it, or define on first use in parentheses or with a link | google:jargon |
| A code term that is also discouraged jargon | Show the term in code font once and say what it means: "add a user to the allowlist (`whitelist`)" | google:inclusive-documentation |
| First mention of a renamed term can give the old one | Do: "allowlist (sometimes called a `whitelist`)" | google:inclusive-documentation |

## Timeless writing

Document the current state; avoid words that date the page. The following table lists the rules and the exceptions:

| Rule | Do / Don't | Source |
|---|---|---|
| Banned in product docs: `as of this writing`, `currently`, `does not yet`, `eventually`, `existing`, `future`, `latest`, `new`, `now`, `old`, `presently`, `soon` | Do: "The emulator supports the following filters:" Don't: `now supports` | google:timeless-documentation |
| "New" or "old" needs a reference point: a date or a version | Do: "The January 14, 2021 release of BigQuery includes a new resource panel." Don't: `the new resource panel` | google:timeless-documentation |
| Time words are fine in release notes, blog posts, and procedure results | Do: `The VM goes offline soon after.` as the result of a step | google:timeless-documentation#exceptions |
| Never document unreleased features, even casually; pre-announcing needs legal approval | Don't: `A later release adds` | google:future |

## Mechanics

The following table lists the rules for numbers, dates, abbreviations, capitalization, contractions, commas, and formatting:

| Rule | Do / Don't | Source |
|---|---|---|
| Spell out zero through nine; numerals from 10; numerals always for versions, technical quantities, step and page numbers, prices, percentages, dimensions, decimals, ranges, and when mixed with 10 or more in one sentence | Do: "three options", "24 hours", "version 3", "6 queries per second", "12 projects, but 4 are archived" | google:numbers |
| Ordinals spelled out; no roman numerals except sub-steps; don't start a sentence with a numeral | Do: "first", "forty-third" | google:numbers |
| Percent: numeral and "%" with no space; ranges with a hyphen and no spaces; commas in numbers of four or more digits; leading zero in decimals; dimensions with "x" | Do: "40%", "2012-2016", "2,000 vertices", "0.3 inches", "192x192" | google:numbers |
| Cite step numbers as numerals | Do: "Repeat step 3." | google:numbers |
| Dates: "July 8, 2025", weekday first when relevant, comma after the year mid-sentence; ISO 8601 when numeric, with a day greater than 12 in invented examples | Do: "2025-07-18" Don't: `07/08/2025` | google:dates-times |
| Times: 12-hour with a space and capital AM or PM, no ":00"; 24-hour only to match UI or code; spell out time zones with a UTC offset, and only when needed | Do: "9:30 AM", "5 PM", "Japan Standard Time (UTC+9)" | google:dates-times |
| No seasons; use months or quarters | Do: "in Q3" Don't: `in the fall` | google:dates-times |
| Spell out an abbreviation on first use with the short form in parentheses, both in italics; skip the long form when it doesn't help (PDF) or the term is universal (API, HTML, URL, RAM); no `approx.` or `10x`; choose the article by sound; never use an acronym as a verb | Do: "a SQL query", "an SAP system", "connect by using SSH" Don't: `ssh into` | google:abbreviations |
| Sentence case in headings, table cells, captions, list items, and glossaries; lowercase after a colon unless a proper noun, heading, or label follows; never caps or camel case to signal meaning; describe a casing style with an example, don't name it | | google:capitalization |
| Contractions: common two-word ones (you're, don't, isn't); prefer negative contractions because readers miss "not"; never a noun contraction (`browser's` for "browser is") or a triple contraction | | google:contractions |
| Commas: after an introductory phrase; before a conjunction that joins independent clauses, unless both are very short; before nonrestrictive "which"; a semicolon or period before "however", "otherwise", and "therefore", and a comma after; usually no comma before "because" | Do: "The variable must have a value; otherwise, the server returns an error." | google:commas |
| Bold only for UI elements, run-in headings, and notice labels; italics for new terms, words as words, light emphasis, full titles, and variables in version numbers; underline only for links; in Markdown use `**` and `_`, never `__` or `*` | Do: `version 1.4._x_` | google:text-formatting |
| No "&" for "and"; no font, size, or color overrides; no quotation marks or end punctuation inside link text | | google:text-formatting |

## Word list

The following table lists the most-violated word list entries. Every row's source is `google:word-list` unless the row names another page:

| Term | Guidance | Source |
|---|---|---|
| `above`, `below` | Not for versions (use later, earlier), document positions (preceding, following), or UI positions | google:word-list |
| `abort`, `kill`, `terminate` | stop, exit, cancel, end; "kill" is fine in command-line contexts, "terminate" in telephony and networking | google:word-list |
| `a.k.a.`, `aka` | "also known as", or parentheses | google:word-list |
| `allows you to` | "lets you" | google:word-list |
| `and/or` | Don't, except in space-limited tables | google:word-list |
| `app` vs `application` | "app" for end-user programs; "application" in enterprise contexts and set phrases | google:word-list |
| `approx.`, `10x` | "approximately"; "10 times" | google:abbreviations |
| `as` (meaning because) | "because" | google:word-list |
| `can`, `may`, `might`, `must`, `should`, `will`, `would` | `can` = ability or permission; `might` = possibility; `may` = policy or legal only; `must` = requirement ("you need" also works); avoid `should`, `will`, and `would` in prose | google:word-list |
| `cell phone`, `mobile` (noun) | "mobile phone", "mobile device", or "phone" | google:word-list |
| `check`, `uncheck`, `deselect` | "select", "clear" | google:word-list |
| `choose` vs `select` | "select" for UI elements; "choose" for generic decisions | google:word-list |
| `click on`, `tap`, `touch` | "click" for mouse targets; "tap" on Android and touch devices; "touch & hold" is fine, bare "touch" is not | google:word-list#click |
| `deprecate` | Means recommend against, not removed, deleted, or shut down | google:word-list |
| `desire`, `desired`, `wish` | "want" or "need" | google:word-list |
| `dummy` | "placeholder" | google:word-list |
| `easy`, `easily`, `simple`, `simply`, `quick`, `quickly` | Remove; the meaning survives | google:word-list |
| `e.g.`, `i.e.`, `etc.` | "for example" or "such as"; "that is"; avoid `etc.` and never `and so on` | google:word-list |
| `e-mail` | "email"; not a verb ("send email") | google:word-list |
| `enable` vs `turn on` | Pick one per document for features; "lets you" for making possible, not `enables you to` | google:word-list |
| `enter` vs `type` | "enter" covers paste and voice; say "press Enter" explicitly when needed | google:word-list |
| `ephemeral IP` | Don't | google:word-list |
| `file name` | "filename", one word | google:word-list |
| `hangs` | "doesn't respond" | google:word-list |
| `hit` | "click" or "press" | google:word-list |
| `hover` | "hold the pointer over"; "point to" | google:word-list#hover |
| `in order to` | "to" | google:word-list |
| `just` | Fine only when one approach is simpler than another; never as a softener | google:word-list |
| `learnings` | "knowledge", "things that you learned" | google:word-list |
| `let's` | Don't | google:word-list |
| `leverage`, `utilize` | "use", "build on", "take advantage of"; `utilize` is fine for resource utilization quantities | google:word-list |
| `login`, `log in`, `sign in` | Noun "login"; verb "sign in"; "sign in to", not `sign into`; "sign-on" only in "single sign-on" | google:word-list |
| `once` (meaning after) | "after" | google:word-list |
| `please` | Never in instructions; only to ask permission or forgiveness | google:tone#politeness |
| `press` | Keys, key combinations, and mechanical buttons only | google:word-list |
| `read-only` | Hyphenated | google:word-list |
| `refer to`, `check out` | "see" | google:cross-references |
| `repo` | "repository" | google:word-list |
| `sanity check` | `quick check`, "confidence check", "preliminary check", "coherence check" | google:word-list |
| `screenshot` | One word; "take a screenshot" | google:word-list |
| `setup` vs `set up` | Noun or adjective "setup"; verb "set up" | google:word-list |
| `since` (meaning because) | "because" | google:word-list |
| `slave`, `master`, `whitelist`, `blacklist` | "replica", "primary", "allowlist", "denylist"; see [Inclusive language](#inclusive-language) | google:word-list |
| `SSH` (verb) | "connect by using SSH" | google:word-list |
| `this`, `that` (bare) | Add a noun after it | google:word-list |
| `toggle` (verb) | "click the toggle to the on position"; "turn on" | google:ui-elements |
| `user` vs `you` | "you" for the reader; "user" only for the reader's own users | google:word-list |
| `via` | "through", "by using", or restructure | google:word-list |
| `walk-through` | `walkthrough`, one word | google:word-list |
| `we` | Not for the reader; fine for the authoring organization with a clear antecedent | google:word-list |
| `zip`, `unzip` | "extract"; not `unarchive`, `uncompress`, or `untar` | google:word-list |

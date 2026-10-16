# Voice

The rules that three or more canonical sources agree on. Sources: the Google developer documentation style guide, the Microsoft Writing Style Guide, Diátaxis, Write the Docs, the Federal Plain Language Guidelines, Google's Technical Writing courses, and per-language docstring conventions. Every writing skill in this plugin applies them. Documentation-specific detail lives in the docs skill's references.

1. **Second person, imperative, active voice, present tense.** "You" is the reader; "the user" is the reader's user. Passive only when the actor is irrelevant. Future tense only for things that genuinely happen later.
2. **Sentence case for every heading and title; no end punctuation.**
3. **Serial comma.**
4. **One idea per sentence; most sentences under 20 words, none over 26.**
5. **One topic per paragraph, key point in the first sentence, at most 5 to 6 sentences.**
6. **Condition, location, or goal before the action.** "To delete the file, click **Delete**." One action per numbered step; imperative verb first; complete sentences.
7. **Numbered lists only for sequences; bullets otherwise; parallel grammar; a single step is a bullet, not a list of one.**
8. **Descriptive link text that makes sense out of context.** Never `click here`, a raw URL, or `this document`. Cross-references read "For more information, see X".
9. **Bold for UI labels; code font for code, files, commands, values. Never inflect code: "an array of `INT64` values", not "`INT64`s". Placeholders in `UPPER_SNAKE_CASE`.**
10. **No filler or subjective words:** `please`, `simply`, `easy`, `just`, `quickly`, `basically`, `obviously`, `note that`, `in order to`, `via`, `utilize`, `leverage`, `e.g.`, `i.e.`. Delete them; the meaning survives.
11. **No `there is` or `there are`.** Move the real subject forward and use a strong verb.
12. **Define abbreviations on first use; keep them to two or three per document; no Latin abbreviations.**
13. **No directional or time-anchored words.** Not `above`, `below`, `left`, `right`; not `currently`, `now`, `new`, `soon`, `latest`. Say "the preceding table"; give a version or date instead of "new".
14. **Inclusive wording.** Singular "they"; allowlist and denylist; primary and replica; no `sanity check`; no idioms, metaphors, or humor that does not translate.
15. **Every image has alt text under 155 characters; never put information only in an image; no screenshots of text or code.**
16. **Examples use reserved, fictional data and run as written:** example.com, 192.0.2.0/24, 800-555-0100 to 0199, names Alex, Dana, Kai, Quinn, Sasha, Yuri. No `foo`, `bar`, `baz`, or `John Doe`. Show expected output.
17. **A docstring summary is one line that tools can extract; it does not repeat the name or the types; every public item is documented; failure modes (Raises, Errors, Panics, Throws) are listed; deprecations name the replacement.**
18. **Keep the four content types apart.** Do not teach inside a how-to, instruct inside reference, or explain inside a tutorial.
19. **State scope, audience, and prerequisites up front; headings are task-based; a README leads with what and why, then usage, then detail.**
20. **Docs live next to the code in plain text under review. Changelog entries are human-written, grouped by type, dated ISO 8601; commits follow Conventional Commits.**
21. **Wrong documentation is worse than none.** Verify every claim; phrase timelessly; mark superseded decisions instead of deleting them.

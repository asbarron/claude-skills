# Document types

Section lists, shapes, and skeletons for each document type the docs skill writes. The required headings and orders here match `doc-types.json`, which the structure check enforces.

## Contents

- [README](#readme)
- [API reference](#api-reference)
- [How-to](#how-to)
- [Tutorial](#tutorial)
- [Explanation](#explanation)
- [ADR](#adr)
- [Changelog](#changelog)
- [Commits](#commits)
- [Runbook](#runbook)

## README

The README is a consumer's first and maybe only look at the project. Its job, in order: tell them what it is, show it in action, show how to use it, then give the remaining details. The following table lists the sections in order; the structure check requires install, usage, and license, in that order, with usage before any API section:

| Section | Content | Source |
|---|---|---|
| Name and one-liner | The H1 is the name. The first sentence says what the project does and who it is for, in plain words, no adjectives | art-of-readme:name, writethedocs:beginners-guide |
| Description | The problem it solves, context links, and how it differs from alternatives | makeareadme:description |
| Install | The basic case in a couple of lines, taken from the manifest; a Requirements subsection when versions matter; links to detail | writethedocs:beginners-guide, makeareadme:installation |
| Usage | The smallest useful example with its expected output; keep it as a runnable file in the repository | art-of-readme:usage, makeareadme:usage |
| API or detail | Signatures, return types, callbacks, events, and caveats; only what a reader needs after the usage example | art-of-readme:api |
| Support and contributing | Where to ask, where to file issues, how to set up for development, how to lint and test | writethedocs:beginners-guide, makeareadme:contributing |
| License | One standard license; move a non-permissive license to the top | writethedocs:beginners-guide, art-of-readme:license |

The following table lists the rules that decide what goes in and what moves out:

| Rule | Do / Don't | Source |
|---|---|---|
| Cognitive funneling: broadest, most pertinent details first, narrowing to what only the deeply interested read | A slightly familiar reader refreshes their memory without paging down | art-of-readme:cognitive-funneling |
| As short as it can be without being any shorter; detail moves to separate pages rather than being cut | Do: link to `docs/` or `CONTRIBUTING.md` Don't: delete the content | art-of-readme:brevity, makeareadme:length |
| Documentation is complete when someone can use the module without reading its code | Every public entry point appears in usage or API | art-of-readme:no-abstraction |
| Link aggressively; state types where they are not obvious; be judicious with badges | | art-of-readme:bonus |
| No FAQ as the primary documentation | FAQs rot and rarely come from real questions | writethedocs:beginners-guide |

The following skeleton passes the structure check:

```markdown
# PROJECT_NAME

One sentence: what it does and who it is for.

## Install

    pip install PROJECT_NAME

Requires Python 3.11 or later.

## Usage

    PROJECT_NAME run config.yaml

The command prints one line per processed record.

## API

## Contributing

## License

MIT. See `LICENSE`.
```

## API reference

An API reference page describes one operation or one resource, with the request before the parameters and the response before the prose. The following table lists the page structure that the Stripe and `Twilio` references converge on:

| Rule | Do / Don't | Source |
|---|---|---|
| One page per operation, or one page per resource with operations as sections; the HTTP method and path lead each section | Do: "POST /v1/customers" as the first line under the heading | stripe:api, twilio:message-resource |
| A runnable request example precedes the parameter list, followed immediately by the full response | One fictional dataset (Dana, `dana@example.com`) reused across every example | stripe:api |
| Every parameter: name in code font, type, required or optional inline, constraints as plain facts, default | Do: `balance` (integer, optional). The maximum length is 150 characters. Defaults to 1. | stripe:api, twilio:message-resource |
| The label is one of required, optional, conditional, or recommended, with the condition stated | Do: `address` (object, required if calculating taxes) | stripe:api |
| Enums list every value in code font | Do: `status` is one of `active`, `paused`, or `deleted` | stripe:api |
| Mutually exclusive parameters are declared explicitly | Do: "Set `from` or `messaging_service_sid`, not both." | twilio:message-resource |
| Nested objects are collapsible and still addressable by link | | stripe:api |
| A Returns section states the success object and when errors occur; errors are documented once on a single page and linked | | stripe:api |
| Label examples by use case, not by number | Do: "Send an SMS message" Don't: `Example 1` | twilio:message-resource |
| Credentials come from environment variables, with a comment pointing to setup | Do: `api_key = os.environ["API_KEY"]` | twilio:message-resource |
| A 5 to 20 line code sample at the top of each page | | google:api-reference-comments |

The following table lists the phrasing for parameter, field, and error descriptions:

| Situation | Opening | Source |
|---|---|---|
| Non-boolean parameter | "The ID of the task to retrieve." Capitalized, ends with a period | google:api-reference-comments |
| Boolean action flag | "If true, validates the certificate before connecting. If false, skips validation." | google:api-reference-comments |
| Boolean state flag or boolean return | "True if the task is complete; false otherwise." True and false not in code font | google:api-reference-comments |
| Default | Explain each value, then "Default: 30." | google:api-reference-comments |
| Exception | "If no key is assigned." when the generator adds "Throws"; otherwise "Thrown when no key is assigned." | google:api-reference-comments |
| Deprecation | "Deprecated. Use `CameraPose` instead." Name the replacement and the version; most important information first | google:api-reference-comments |
| String literal | Code font inside double quotes: "`"enabled"`" | google:api-reference-comments |
| Class name | Never pluralized in code font: "`Intent` objects"; match the spelling exactly | google:api-reference-comments |

## How-to

A how-to guide takes a competent reader through one real task. The structure check requires an H1 that starts with "How to" or a bare infinitive, and a numbered list. It forbids the phrases `in this tutorial` and `let's`. The following table lists the shape:

| Rule | Do / Don't | Source |
|---|---|---|
| Title names the task exactly | Do: "How to rotate the signing key" or "Rotate the signing key" Don't: `Rotating the signing key` | diataxis:how-to-guides |
| One sentence of context, then prerequisites, then the numbered steps | | diataxis:how-to-guides, google:procedures |
| Steps are conditional imperatives where the reader's situation varies | Do: "If the key is in use, set `grace_period` first." | diataxis:how-to-guides |
| No teaching, no background; link to the explanation and the reference instead | | diataxis:how-to-guides |
| A verification step closes the guide | Do: "Run `keyctl list`. The new key appears first." | google:procedures |

```markdown
# How to rotate the signing key

Rotate the key when it expires or after a suspected leak. You need admin access.

1. Generate the new key:

       keyctl generate --name signing-2

2. Set the grace period so in-flight requests keep working:

       keyctl grace signing-1 --hours 24

3. Promote the new key. Run `keyctl promote signing-2`. The output ends with `active`.
```

## Tutorial

A tutorial is a lesson that produces a working result. The structure check requires a numbered list with at least three steps and forbids "you can also" and "alternatively". The following table lists the shape:

| Rule | Do / Don't | Source |
|---|---|---|
| Open by saying what the reader builds, not what they learn | Do: "In this tutorial, we build a bot that answers on port 8000." | diataxis:tutorials |
| State the prerequisites and the time it takes | Do: "You need Python 3.11. The tutorial takes about 20 minutes." | diataxis:tutorials |
| Each step ends with a visible result and a sentence about what to notice | Do: "The server prints `Listening on 8000`." | diataxis:tutorials |
| One path only: no options, no alternatives, no explanation beyond a clause and a link | | diataxis:tutorials |
| "We" voice throughout; close with what was built and where to go next | | diataxis:tutorials |

## Explanation

An explanation page answers a "why" question. The structure check forbids numbered lists on it. The following table lists the shape:

| Rule | Do / Don't | Source |
|---|---|---|
| Title is a noun phrase with an implied "About", or the question itself | Do: "Retry policy" or "Why the client retries" | diataxis:explanation |
| Open with the question and the short answer, then the forces behind it | | diataxis:explanation |
| Discuss alternatives and their costs; opinion is allowed when labeled | Do: "We chose exponential back-off; a fixed delay has less code but overloads a recovering server." | diataxis:explanation |
| No steps, no parameter tables; link to the how-to and the reference | | diataxis:explanation |
| Close with the boundaries: what the page does not cover | | diataxis:explanation, eppo:specific-purpose |

## ADR

An architecture decision record captures one decision for a future developer. The structure check requires the filename `adr-NNN.md` or `NNN-slug.md` and the sections Context, Decision, Status, and Consequences in that order. The following table lists the rules:

| Rule | Do / Don't | Source |
|---|---|---|
| File `doc/arch/adr-NNN.md`; sequential numbers, never reused; one or two pages | | nygard:adr |
| Title is a short noun phrase with the number | Do: "ADR 9: LDAP for multi-tenant integration" | nygard:adr |
| Context states the forces in tension, neutrally and value-free | Do: "Three services need a shared directory. Two already speak LDAP." | nygard:adr |
| Decision is full sentences in active voice, "We will ..." | Do: "We will use LDAP as the directory for all tenants." | nygard:adr |
| Status is one of Proposed, Accepted, Deprecated, or Superseded, with a reference to the superseding ADR | Do: "Superseded by ADR 14" | nygard:adr |
| Consequences lists every outcome: positive, negative, and neutral | | nygard:adr |
| Paragraphs of full sentences; bullets only for layout; never delete a reversed decision, mark it superseded | | nygard:adr |

```markdown
# ADR 9: LDAP for multi-tenant integration

## Context

Three services need a shared directory. Two already speak LDAP.

## Decision

We will use LDAP as the directory for all tenants.

## Status

Accepted

## Consequences

Every service gains one network dependency. Tenant onboarding drops from two steps to one.
```

## Changelog

"Changelogs are for humans, not machines." The structure check requires the filename `CHANGELOG.md` and an `[Unreleased]` section first. Version headings take the form `## [1.2.0] - 2026-10-16`, and only the six section names are allowed. The following table lists the rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Every version has an entry, newest first, each dated in ISO 8601 | Do: `## [1.2.0] - 2026-10-16` Don't: `## 1.2.0 (16/10/2026)` | keepachangelog:1.1.0 |
| Group changes by type: Added, Changed, Deprecated, Removed, Fixed, Security | | keepachangelog:1.1.0 |
| One bullet per change, describing user-visible impact | Do: "Retries now honor `Retry-After`." Don't: `Merge pull request #41` | keepachangelog:1.1.0 |
| State whether the project follows Semantic Versioning; link each version heading to a compare URL at the bottom | | keepachangelog:1.1.0 |
| Mark a pulled release `[YANKED]` | Do: `## [0.0.5] - 2014-12-13 [YANKED]` | keepachangelog:1.1.0 |
| Never dump the commit log, skip deprecations, or leave gaps; "an incomplete changelog is nearly as harmful as none" | | keepachangelog:1.1.0 |

```markdown
# Changelog

All notable changes to this project are listed here. The format follows Keep a Changelog, and the project follows Semantic Versioning.

## [Unreleased]

### Added

- Retries honor the `Retry-After` header.

## [1.2.0] - 2026-10-16

### Fixed

- The CLI exits with code 2 on a malformed config file.
```

## Commits

Commit messages follow Conventional Commits 1.0.0. The structure check applies the pattern `^(feat|fix|build|chore|ci|docs|style|refactor|perf|test|revert)(\([a-z0-9-]+\))?!?: .+` to the first line. The following table lists the rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Shape: type, optional scope in parentheses, colon, space, description; blank line; body; blank line; footers | Do: `feat(parser): add ability to parse arrays` | conventionalcommits:1.0.0 |
| `fix` is a patch release, `feat` a minor release; `!` before the colon or a `BREAKING CHANGE:` footer is a major release, on any type | Do: `feat(api)!: drop the v1 endpoints` | conventionalcommits:1.0.0 |
| Other types: build, chore, ci, docs, style, refactor, perf, test, revert | | conventionalcommits:1.0.0 |
| Scope is a noun naming the affected area, lowercase | Do: `fix(auth): reject expired tokens` | conventionalcommits:1.0.0 |
| Footers are `Token: value` or `Token #value` with hyphenated tokens; `BREAKING CHANGE` is the one exception and stays uppercase | Do: `Reviewed-by: Dana` and `Refs #123` | conventionalcommits:1.0.0 |
| Description is imperative, lowercase, no end period; the body says why, not what | Do: `docs(readme): state the Python floor` | conventionalcommits:1.0.0 |

## Runbook

A runbook is a how-to for an operator under time pressure. The structure check requires three sections and a numbered list. The trigger section is named When to use, Trigger, or Symptoms; the steps section Steps, Procedure, or Resolution; the verification section Verify, Verification, or Check. The following table lists the rules:

| Rule | Do / Don't | Source |
|---|---|---|
| The trigger section names the alert or symptom and the first thing to check | Do: "Alert `api-5xx-rate` over 2% for 5 minutes." | google:tech-writing/two/large-docs |
| Prerequisites, access, and rollback come before the steps, never in a note mid-procedure | | google:procedures |
| One action per step, location before action, expected result after the action in the same paragraph | Do: "On the **Deployments** page, click **Roll back**. The status changes to Rolling back." | google:procedures |
| Document one method; put the alternative on another page | | google:procedures#multiple-ways |
| Requirement words carry their plain-language meanings: `must` for an obligation, `must not` for a prohibition, `may` for a discretionary action, `should` for a recommendation; never `shall` | Do: "You must drain the node before step 3." | fplg:must |
| The verification section states the signal that proves recovery and what to do if it does not appear | Do: "The 5xx rate drops under 0.5% within two minutes. If it does not, escalate to the on-call lead." | google:procedures |
| Timing and time-anchored words are allowed in step results | Do: "The pod restarts within 30 seconds." | google:timeless-documentation#exceptions |

```markdown
# Roll back a bad deployment

## When to use

Alert `api-5xx-rate` fires and the last deployment was under one hour ago.

## Steps

1. On the **Deployments** page, select the previous release.
2. Click **Roll back**. The status changes to Rolling back.
3. Watch the error-rate panel for two minutes.

## Verify

The 5xx rate drops under 0.5%. If it does not, escalate to the on-call lead.
```

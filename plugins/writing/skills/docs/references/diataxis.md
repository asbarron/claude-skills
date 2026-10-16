# Diátaxis

The four documentation types, the compass that assigns content to one of them, and the rules for each. The last section adds the entry-point rules from Every Page is Page One and Google Technical Writing Two.

## Contents

- [The map](#the-map)
- [The compass](#the-compass)
- [Tutorial](#tutorial)
- [How-to](#how-to)
- [Reference](#reference)
- [Explanation](#explanation)
- [Adopting the map](#adopting-the-map)
- [Every page is page one](#every-page-is-page-one)

## The map

Two axes divide documentation: action versus cognition (practical steps versus theory) and acquisition versus application (study versus work). The following table lists the four quadrants:

| Quadrant | Orientation | Purpose | Form | The page must | Source |
|---|---|---|---|---|---|
| Tutorial | Learning | Provide a learning experience | A lesson | Introduce, educate, lead | diataxis:tutorials |
| How-to guide | Goal | Help achieve a particular goal | A series of steps | Guide | diataxis:how-to-guides |
| Reference | Information | Describe the machinery | Dry description | State, describe, inform | diataxis:reference |
| Explanation | Understanding | Illuminate a topic | Discursive explanation | Explain, clarify, discuss | diataxis:explanation |

When the distinctions blur, the kinds "bleed into each other." The worst case is a tutorial and a how-to guide collapsing into one page. Such a page serves neither a learner nor a worker. Neighbors on the map have natural affinity and are the ones that blur: tutorial with how-to, how-to with reference, reference with explanation, explanation with tutorial. Readers cycle through the quadrants: learn, do goal-oriented work, consult reference for missing facts, reflect through explanation. They enter anywhere.

## The compass

Apply the compass to a whole document, a section, or a single sentence whenever you suspect the text is doing one thing while you intend another. The following table is the compass:

| If the content | And it serves the reader's | Then it belongs to | Source |
|---|---|---|---|
| Informs action | Acquisition of skill | A tutorial | diataxis:compass |
| Informs action | Application of skill | A how-to guide | diataxis:compass |
| Informs cognition | Application of skill | Reference | diataxis:compass |
| Informs cognition | Acquisition of skill | Explanation | diataxis:compass |

## Tutorial

A tutorial is a lesson the reader follows to acquire a skill. The following table lists its rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Show where the lesson is going at the start; never promise what the reader "learns" | Do: "In this tutorial, we build a service that answers on port 8000." Don't: `You will learn about services.` | diataxis:tutorials |
| Visible results early and often | Every two or three steps, something runs or renders | diataxis:tutorials |
| Narrate what to expect and what to notice | Do: "The install prints about thirty lines. Notice the last one, which names the port." | diataxis:tutorials |
| Allow repetition; avoid irreversible steps | Do: "Run the command again." Don't: a step that deletes a resource with no way back | diataxis:tutorials |
| Minimize explanation: one clause and a link | Do: "The port is 8000 because that is the default; the reference page lists the alternatives." | diataxis:tutorials |
| Concrete, not abstract; ignore options and alternatives | Do: "Use port 8000." Don't: `You can use any free port, or alternatively a socket.` | diataxis:tutorials |
| "We" voice: tutor and learner together | Do: "Next, we add a route." | diataxis:tutorials |
| Aspire to perfect reliability; test in a clean environment before publishing | Run it from a fresh checkout | diataxis:tutorials |

## How-to

A how-to guide helps a competent reader reach one real goal. The following table lists its rules:

| Rule | Do / Don't | Source |
|---|---|---|
| One real task from user need, not tool operation | Do: "How to use fixtures in `pytest`" Don't: `How to build a web application` | diataxis:how-to-guides |
| Assume competence; "a recipe is not a cooking lesson" | Skip what a working developer already knows | diataxis:how-to-guides |
| Only action; link out for explanation and reference | Do: "For the full option list, see the reference page." | diataxis:how-to-guides |
| Adaptable through conditional imperatives | Do: "If you want retries, set `max_attempts`." | diataxis:how-to-guides |
| Usefulness over completeness; logical, not necessarily linear; seek flow | Cover the path readers take, not every branch | diataxis:how-to-guides |
| The title says exactly what the page shows | Do: "How to integrate application performance monitoring" Don't: `Integrating application performance monitoring` (ambiguous) or `Application performance monitoring` (worst) | diataxis:how-to-guides |

## Reference

Reference describes the machinery and nothing else. The following table lists its rules:

| Rule | Do / Don't | Source |
|---|---|---|
| "Describe and only describe"; austere and authoritative | No persuasion, no teaching | diataxis:reference |
| Standard patterns so readers find things where they expect them | Same section order on every page of the same kind | diataxis:reference |
| Structure mirrors the machinery | One page per module, resource, or command, in the code's own hierarchy | diataxis:reference |
| Brief examples are fine; instruction is not | Do: a two-line call and its output Don't: numbered steps | diataxis:reference |
| Warnings as plain constraints | Do: "You must not apply `b` unless `c` is set." | diataxis:reference |
| List everything: commands, options, flags, limits, errors | A missing flag is a bug | diataxis:reference |
| Generated docs don't replace hand-written reference | Generation supplies the skeleton; a person supplies the descriptions | diataxis:reference |

## Explanation

Explanation gives context and reasons. The following table lists its rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Make connections; give context and reasons: design decisions, history, constraints | Do: "The cache is write-through because the service tolerates stale reads for under a second." | diataxis:explanation |
| Titles read with an implied "About" | Do: "About user authentication" or "User authentication" | diataxis:explanation |
| Admit opinion; weigh alternatives | Do: "An event log also works; it costs more storage and buys the ability to replay." | diataxis:explanation |
| Keep it tightly bounded: no instructions, no reference tables | Link to the how-to and the reference instead | diataxis:explanation |
| Scope the page with a "why" question | Do: "Why does the client retry?" | diataxis:explanation |
| Section label can be Discussion, Background, Concepts, or Topics | Pick one and keep it across the site | diataxis:explanation |

## Adopting the map

Diátaxis changes documentation from the inside, one page at a time. The following table lists the adoption rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Work one step at a time; every step in the right direction is worth publishing | Don't: wait for the big picture | diataxis:how-to-use-diataxis |
| Don't impose a top-level structure first | Don't: create empty tutorial, how-to, reference, and explanation sections ("Don't do that. It's horrible.") | diataxis:how-to-use-diataxis |
| Functional quality is measurable: accuracy, completeness, consistency, usefulness, precision | Check these with a review | diataxis:quality |
| Deep quality is judged: flow, fit to human needs, anticipating the reader | "Documentation can be accurate and complete and consistent without being truly excellent." | diataxis:quality |

## Every page is page one

Readers arrive from search or a link, so every page works as an entry point. The following table lists the traits of such a page, with the large-document rules from Google Technical Writing Two:

| Rule | Do / Don't | Source |
|---|---|---|
| Self-contained: designed to function alone, not merely to stand alone | Name the tool and the symbol in the text, not "it" | eppo:self-contained |
| Specific and limited purpose; conforms to a type that the purpose defines | One quadrant, one job per page | eppo:specific-purpose |
| Establishes context, because the reader can arrive from anywhere | Do: "This page describes the retry policy of the Python client." | eppo:establish-context |
| Assumes the reader is qualified and points others to prerequisites | Do: "Before you start, install the CLI." | eppo:assume-qualified |
| Stays on one level; never drifts between conceptual, procedural, and detailed | Let the reader decide when to change levels by following a link | eppo:stay-on-one-level |
| Links richly along lines of subject affinity | Link the concept, the how-to, and the reference to each other | eppo:link-richly |
| Outline first; one concept or task per outline step; alternate concepts with hands-on sections | | google:tech-writing/two/large-docs |
| The introduction states scope, prerequisites, and exclusions | Do: "This guide covers deployment to a single region. Multi-region setups are out of scope." | google:tech-writing/two/large-docs |
| Task-based headings in the reader's language; a short intro sentence under every heading | Do: "Rotate the signing key" | google:tech-writing/two/large-docs |
| Table of contents and a next-steps section on long pages | | google:tech-writing/two/large-docs |
| Progressive disclosure: define terms near the steps that need them; the smallest example first | | google:tech-writing/two/large-docs |

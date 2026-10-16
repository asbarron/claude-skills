# Code samples

Rules for code in running text, sample blocks, command syntax, placeholders, and the reserved example data, plus the sample-quality standard from Google Technical Writing Two.

## Code in text

Code font and bold for UI are house rules. The following table lists what gets code font and how to write around it:

| Rule | Do / Don't | Source |
|---|---|---|
| Code font for attributes, classes, methods, command names, command output, data types, database elements, keywords, constants, enums, environment variables, filenames and paths, HTTP verbs and status codes, content types, query parameters, IAM roles, package names, port numbers, IP addresses, element names without brackets, text the reader types, URLs inside code, and placeholders | Do: "Open the `pg_hba.conf` file in the `/etc/postgresql/13/main` directory." | google:code-in-text |
| Not code font: product and organization names, plain domain references, URLs the reader visits (link those) | | google:code-in-text |
| Booleans: code font when naming the value, plain when describing a condition | Do: "set `enabled` to `true`"; "if the flag is enabled" | google:code-in-text |
| A UI element that is also code gets bold and code font | Do: "select **`us-east1`**" | google:code-in-text |
| Omit the class name from a method reference unless it is ambiguous | Do: "the `get` method" Don't: `the animal.get method` | google:code-in-text |
| Status codes are "status code", never "response code" or "error code"; give the number and the name; ranges as `4xx` | Do: "a `404 Not Found` status code" | google:code-in-text |
| Pair every code keyword with a qualifying noun | Do: "the `example.yaml` file" Don't: `open example.yaml` | google:translation |
| Never inflect code: add a noun and inflect that | Do: "an array of `INT64` values", "send a `POST` request" Don't: `Returns INT64s`, `POST the data` | google:code-in-text#grammar |

## Sample blocks

The following table lists the rules for a fenced code sample:

| Rule | Do / Don't | Source |
|---|---|---|
| An intro sentence precedes every sample; colon if the sample follows directly, period if a note intervenes | Do: "The following code sample shows how to use the `get` method:" | google:code-samples |
| Two-space indent unless the language guide says otherwise; wrap at 80 characters | | google:code-samples |
| Omitted code is a comment in the sample's language, never three dots; a block with omissions is not click-to-copy | Do: `# Several lines of code are omitted here.` | google:code-samples |
| Input and output go in separate blocks; show output only when it adds value, introduced with "The output is similar to the following:" | Omitted output lines are a line of three dots on their own | google:code-syntax |
| Comments are short and sit on non-obvious lines only; an explanation that must travel with copied code goes in a comment | "Why" comments for experts, not "what" comments | google:tech-writing/two/sample-code |

## Command syntax

The following table lists the rules for command lines:

| Rule | Do / Don't | Source |
|---|---|---|
| Show the `$` prompt only when a block has several commands or the document mixes input and output; change the prompt when the context changes | | google:code-syntax |
| Optional arguments in square brackets, each on its own; mutually exclusive arguments as `{A\|B}`; repeatable arguments with three dots | Do: `gcloud dns GROUP [GLOBAL_FLAG ...]` | google:code-syntax |
| A click-to-copy block contains no brackets, braces, pipes, or three dots | Move syntax notation to a separate non-copyable block | google:code-syntax |
| Break long commands before a `-`, `--`, `_`, or quote; 4-space continuation indent; a trailing backslash on Linux and a trailing caret on Windows | | google:code-syntax |
| Never "run the following command" as the whole intro; say what the command does | Do: "Create the bucket:" | google:procedures |

## Placeholders

The following table lists the placeholder rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Descriptive UPPER_SNAKE_CASE, no possessive prefix | Do: `API_NAME` Don't: a `MY_` prefix, `api-name`, `apiName`, or angle brackets | google:placeholders |
| Markup: HTML wraps the placeholder in `code` and `var` elements; Markdown puts asterisks outside the backticks | Do: ``*`API_NAME`*`` | google:placeholders |
| Explain each placeholder on first use | Do: "Replace `BUILD_ID` with the ID from the previous step." | google:placeholders |
| Two or more placeholders: "Replace the following:" and a list where each item is the placeholder in code font, a colon, and a lowercase description | Do: "- `PROJECT_ID`: the project that owns the bucket" | google:placeholders |

## Reserved example data

Never put real names, domains, emails, phone numbers, IP addresses, or card numbers in an example. The following table lists the pools to draw from:

| Rule | Do / Don't | Source |
|---|---|---|
| Domains: example.com, example.org, example.net; organization: "Example Organization" | Do: `dana@example.com` | google:examples |
| People: Alex, Dana, Kai, Quinn, Sasha, Yuri; Alice and Bob only when documenting a specification that uses them | | google:examples |
| Phone numbers: 800-555-0100 through 800-555-0199 | | google:examples |
| IPv4 from RFC 5737: 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24; IPv6 from RFC 3849: 2001:db8::/32 | Do: `192.0.2.10` | google:examples |
| Project and resource names are meaningful words with numbered suffixes, never `foo`, `bar`, `baz` | Do: `production-1`, `production-2` | google:examples |
| Dates in invented examples use a day greater than 12 so the format is unambiguous | Do: `2026-10-16` | google:dates-times |

## Sample quality

The only goal of a sample program is to educate. The following table lists the quality standard:

| Rule | Do / Don't | Source |
|---|---|---|
| Correct: builds, runs, production-ready, no security holes, follows the language's conventions | | google:tech-writing/two/sample-code |
| Tested and maintained like code; never a reused unit test | | google:tech-writing/two/sample-code |
| Concise, but "always prefer correctness over conciseness" | | google:tech-writing/two/sample-code |
| Descriptive names; no tricks or deep nesting; named parameters for API newcomers | | google:tech-writing/two/sample-code |
| Show the expected output; state prerequisites | | google:tech-writing/two/sample-code |
| An anti-example is fine for strict syntax, labeled as wrong | Do: a block headed "Don't do this:" | google:tech-writing/two/sample-code |
| A sample set ramps from Hello World to moderate to complex | | google:tech-writing/two/sample-code |

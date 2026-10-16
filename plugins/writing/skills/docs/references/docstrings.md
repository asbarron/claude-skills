# Docstrings

Per-language conventions for code-level documentation, each with the canonical skeleton, and the cross-language phrasing patterns for first sentences. The house rule that a summary is one extractable line that does not repeat the name or the types applies everywhere.

## Contents

- [Python](#python)
- [Go](#go)
- [Rust](#rust)
- [TypeScript and JavaScript](#typescript-and-javascript)
- [Phrasing patterns](#phrasing-patterns)

## Python

Python follows the Google Python style guide, section 3.8. The following table lists the rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Triple double quotes always; the summary is one physical line of at most 80 characters ending in a period, question mark, or exclamation mark; a blank line follows it; the rest aligns with the opening quote | | pyguide:3.8.1 |
| Module docstring: one-line summary, blank line, description, optional usage examples; license boilerplate goes before it | Test modules can skip the docstring; never repeat the module name | pyguide:3.8.2 |
| Every public, nontrivial, or non-obvious function has a docstring that says how to call it and what it does, not how it works | Note side effects such as mutated arguments | pyguide:3.8.3 |
| Descriptive ("Fetches rows") or imperative ("Fetch rows"), consistent within a file | Properties use attribute style, not "Returns" | pyguide:3.8.3 |
| Sections end with a colon and use a 2- or 4-space hanging indent: `Args:`, `Returns:` or `Yields:`, `Raises:` | | pyguide:3.8.3 |
| `Args:` lists each name and description; types only when the signature is unannotated; `*args` and `**kwargs` written as in the signature | | pyguide:3.8.3 |
| `Returns:` is omitted when the function returns None or the summary already says; describe tuples as "A tuple (a, b), where ..." | | pyguide:3.8.3 |
| `Raises:` lists exceptions relevant to the interface, not ones raised on contract violation | Do: `IOError: An error occurred accessing the table.` | pyguide:3.8.3 |
| Decorated functions describe post-decoration behavior; overriding methods get no docstring unless they refine the contract | | pyguide:3.8.3 |
| Class summary says what an instance represents; never say "class"; `Attributes:` lists public non-property attributes; exception classes describe what they represent, not when they are raised | | pyguide:3.8.4 |
| Comments explain the reasoning behind tricky code, not each line; inline comments start two or more spaces after the code; `TODO:` carries a link or bug and an explanation, never a person's name | Do: `# TODO: b/192837465: Remove after the migration.` | pyguide:3.8.5 |

```python
def fetch_smalltable_rows(table_handle, keys, require_all_keys=False):
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will be
          returned.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. ...

    Raises:
        IOError: An error occurred accessing the smalltable.
    """

class SampleClass:
    """Summary of class here.

    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
```

## Go

Go doc comments sit on the lines that precede a top-level declaration, with no blank line between. The following table lists the rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Every exported name gets a doc comment of complete sentences | | go:doc-comment |
| Package comment begins "Package name ..." and lives in one file per package; a command's comment starts with the capitalized program name | Do: `Gofmt formats Go programs.` | go:doc-comment#package |
| Type comment is a full sentence naming the symbol; state concurrency guarantees when they are stronger than single-goroutine; document the zero value and exported fields | Do: "A Buffer is a variable-sized buffer of bytes." | go:doc-comment#type |
| A function comment starts with the function name and says what it returns or does; refer to parameters by bare name, not in code font | Do: "HasPrefix reports whether the string s begins with prefix." | go:doc-comment#func |
| A function that returns a `bool` "reports whether", never "or not" | Don't: `returns true if s begins with prefix or not` | go:doc-comment#func |
| List special cases; don't describe the implementation; give asymptotic bounds only when callers need them | | go:doc-comment#func |
| A `const` or `var` group can share one comment with end-of-line comments per item; an item outside a group needs a full sentence | | go:doc-comment#const |
| Syntax: paragraphs without indentation; `# Heading` lines set off by blank lines; `[Name]`, `[pkg.Name]`, and `[*bytes.Buffer]` doc links; `[Text]: URL` link definitions; lists with `-` or `N.`; no nested lists, HTML, or font changes | | go:doc-comment#syntax |
| Any indented line is a code block, so indent continuation lines of list items and never indent wrapped paragraph lines | | go:doc-comment#syntax |
| `Deprecated:` starts its own paragraph, explains why, and names the alternative; notes use `MARKER(uid): body` with two or more uppercase letters | | go:doc-comment#notes |

```go
// Package path implements utility routines for manipulating slash-separated
// paths.
package path

// A Regexp is the representation of a compiled regular expression.
// A Regexp is safe for concurrent use by multiple goroutines,
// except for configuration methods, such as Longest.
type Regexp struct {
    // Fields are omitted here.
}

// HasPrefix reports whether the string s begins with prefix.
func HasPrefix(s, prefix string) bool

// Reset zeros the key data and makes the Cipher unusable.
//
// Deprecated: Reset can't guarantee that the key will be entirely removed from
// the process's memory.
func (c *Cipher) Reset()
```

## Rust

Rust follows the rustdoc book and the Rust API guidelines. The following table lists the rules:

| Rule | Do / Don't | Source |
|---|---|---|
| `//!` documents the crate or module front page; `///` documents items; every public item is documented | | rustdoc:how-to-write-documentation |
| The crate front page opens with a sentence that places the crate in the ecosystem, then one copy-pasteable real-world example, then a features list | | rustdoc:how-to-write-documentation |
| Item structure: short sentence, blank line, detailed explanation, blank line, at least one copy-paste example, then advanced notes; everything before the first blank line is the summary, so keep it one line | | rustdoc:how-to-write-documentation |
| Don't repeat type information; the signature is already linked | | rustdoc:how-to-write-documentation |
| `# Errors` lists every error condition, including on trait methods; `# Panics` lists every panic condition, documenting more when unsure; `# Safety` lists every invariant the caller upholds on an `unsafe` function; `# Examples` holds the samples | | api-guidelines:C-FAILURE |
| Examples show why to use the item, not only how | | api-guidelines:C-EXAMPLE |
| Examples use `?`, never `unwrap` or `try!`; hide boilerplate lines with a leading a `#` and a space | Unwrapping an error is a conscious decision, not an example default | api-guidelines:C-QUESTION-MARK |
| Link every type with `` [`Type`] `` and reference definitions; method anchors are `#method.name` | | api-guidelines:C-LINK |
| `#[doc(hidden)]` for implementation details users never need | | api-guidelines:C-HIDDEN |
| Release notes link from the crate docs, flag breaking changes, and match annotated git tags; `Cargo.toml` carries authors, description, license, repository, keywords, and categories | | api-guidelines:C-RELNOTES, api-guidelines:C-METADATA |
| Markdown is CommonMark plus `strikethrough`, footnotes, tables, task lists, and smart punctuation; warnings use a `div` with class `warning` | | rustdoc:how-to-write-documentation |

```rust
/// Returns the arguments which this program was started with (normally passed
/// via the command line).
///
/// The first element is traditionally the path of the executable, ...
///
/// # Panics
///
/// The returned iterator will panic during iteration if any argument to the
/// process is not valid unicode. If this is not desired,
/// use the [`args_os`] function instead.
///
/// # Examples
///
/// ```
/// use std::env;
/// for argument in env::args() {
///     println!("{argument}");
/// }
/// ```
///
/// [`args_os`]: ./fn.args_os.html
```

## TypeScript and JavaScript

TypeScript uses TSDoc; JavaScript uses JSDoc. Both parse only comments that open with `/**`. The following table lists the rules:

| Rule | Do / Don't | Source |
|---|---|---|
| Only `/** */` is parsed; `/*` and `/***` are ignored; the comment sits immediately before the code | | JSDoc:about-getting-started |
| JSDoc tags: `@param {type} name - description`, `@returns`, `@throws`, `@example`, `@deprecated`, `@typedef`, `@see`, `@since`, `@async`, `@class`, `@private`, `@public`, `@default`, `@readonly`, `@yields`; inline `{@link}` | Types go in braces because JavaScript has none | JSDoc:tags |
| TSDoc never repeats types; TypeScript has them | Don't: `@param {string} name` | TSDoc:spec |
| Text before the first block tag is the summary; long prose goes under `@remarks` | | TSDoc:tags#remarks |
| Block tags: `@param`, `@returns`, `@remarks`, `@example`, `@throws`, `@deprecated`, `@typeParam`, `@defaultValue`, `@see`, `@privateRemarks` | | TSDoc:tags |
| Modifier tags sit one per line at the bottom: release tags `@public`, `@beta`, `@alpha`, `@internal`; also `@readonly`, `@override`, `@sealed`, `@virtual`, `@packageDocumentation` | | TSDoc:tags |
| Inline tags: `{@link}`, `{@inheritDoc}`, `{@label}` | | TSDoc:tags |
| `@param name - description` uses a hyphen separator | Do: `@param x - The first input number` | TSDoc:tags#param |
| `@throws` names each error type and when it occurs; `@deprecated` names the replacement | | JSDoc:tags, TSDoc:tags#deprecated |

```ts
/**
 * Returns the average of two numbers.
 *
 * @remarks
 * This method is part of the {@link core-library#Statistics | Statistics subsystem}.
 *
 * @param x - The first input number
 * @param y - The second input number
 * @returns The arithmetic mean of `x` and `y`
 *
 * @beta
 */
```

## Phrasing patterns

The first sentence of any API comment states the action in present tense and is short and unique, because tools extract it. A class summary gives the purpose beyond what the name says, never starts "This class will", and never contains `e.g.` because the period ends the summary. The following table lists the opening for each situation:

| Situation | Opening | Source |
|---|---|---|
| Method that returns data | A verb: "Adds a new task to the queue and returns its ID." | google:api-reference-comments |
| Boolean getter | "Checks whether ..." (Go: "reports whether") | google:api-reference-comments, go:doc-comment#func |
| Non-boolean getter | "Gets the ..." | google:api-reference-comments |
| Setter, updater, remover, registrar | "Sets the ...", "Updates the ...", "Deletes the ...", "Registers ..." | google:api-reference-comments |
| Callback | "Called by ..." then "Subclasses implement this method to ..." | google:api-reference-comments |
| Convenience constructor | "Creates a ..." | google:api-reference-comments |
| Non-boolean parameter | "The ID of the task to retrieve." Capitalized, ends with a period | google:api-reference-comments |
| Boolean action flag | "If true, validates the certificate before connecting. If false, skips validation." | google:api-reference-comments |
| Boolean state flag or boolean return | "True if ...; false otherwise." True and false not in code font | google:api-reference-comments |
| Default | Explain each value, then "Default: ..." | google:api-reference-comments |
| Exception | "If no key is assigned." when the generator adds "Throws"; otherwise "Thrown when ..." | google:api-reference-comments |
| Deprecation | "Deprecated. Use `CameraPose` instead." Name the replacement and the version; most important information first | google:api-reference-comments |
| String literal | Code font inside double quotes | google:api-reference-comments |
| Class name in prose | Never pluralized in code font: "`Intent` objects"; spelling matches the declaration | google:api-reference-comments |
| Python summary | Descriptive or imperative, consistent per file; the skill default is descriptive third person to match the other languages | pyguide:3.8.3 |

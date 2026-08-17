# Coding standard topics

The topic list for the coding standard. Every row is written; the **Entry**
column links it to its file in [docs/standard/](../standard/).

The split: a standard topic is one the project decides once and every file
follows, checkable by a tool or at a glance. A policy is a decision procedure an
author applies case by case. Correct the split and this list changes. The rule
that keeps a policy from restating an entry is in
[the corpus format](README.md#the-coding-standard-boundary).

The **Material** column says where the content came from. Most of these claim
rows in [CG-WORKLIST.md](CG-WORKLIST.md) or
[CONVENTIONS-ADDITIONS.md](CONVENTIONS-ADDITIONS.md) rather than adding anything
new, so a row landing here came out of there.

## Files and layout

| Topic | What it fixes | Material | Entry |
|-------|---------------|----------|-------|
| File extensions | `.hpp` for headers, `.cpp` for sources | diverges [Use a `.cpp` suffix for code files and `.h` for interface files if your project doesn't already follow another convention](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-file-suffix) (SF.1), [Use a `.cpp` suffix for code files and `.h` for interface files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-file-suffix) (NL.27); additions | [STD-0001](../standard/STD-0001-file-extensions.md) |
| File naming | `snake_case` filenames | conventions.md Naming | [STD-0002](../standard/STD-0002-file-naming.md) |
| Directory and namespace layout | `include/proj/layer/`, namespaces nested by layer, `snake_case` | [Use `namespace`s to express logical structure](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-namespace) (SF.20); conventions.md Module Boundary | [STD-0003](../standard/STD-0003-directory-and-namespace-layout.md) |
| Include guards | `#ifndef PROJECT_COMPONENT_FILE_HPP`, no `#pragma once` | [Use `#include` guards for all header files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-guards) (SF.8); additions | [STD-0004](../standard/STD-0004-include-guards.md) |
| Include order and form | Own header first, quoted for local and angle for external, self-contained headers, no reliance on implicit includes | [Include header files before other declarations in a file](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-include-order) (SF.4), [A `.cpp` file must include the header file(s) that defines its interface](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-consistency) (SF.5), [Avoid dependencies on implicitly `#include`d names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-implicit) (SF.10), [Header files should be self-contained](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-contained) (SF.11), [Prefer the quoted form of `#include` for files relative to the including file and the angle bracket form everywhere else](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-incform) (SF.12), [Use portable header identifiers in `#include` statements](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-portable-header-id) (SF.13) | [STD-0005](../standard/STD-0005-include-order-and-form.md) |
| `using namespace` placement | Never at header scope, local scope only | [Use `using namespace` directives for transition, for foundation libraries (such as `std`), or within a local scope (only)](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-using) (SF.6), [Don't write `using namespace` at global scope in a header file](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-using-directive) (SF.7) | [STD-0006](../standard/STD-0006-using-namespace-placement.md) |
| Anonymous namespace | Internal entities in the `.cpp`, never in a header | [Don't use an unnamed (anonymous) namespace in a header](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-unnamed) (SF.21), [Use an unnamed (anonymous) namespace for all internal/non-exported entities](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-unnamed2) (SF.22) | [STD-0007](../standard/STD-0007-anonymous-namespace.md) |
| Test file location and naming | Where a test lives relative to what it tests | conventions.md Testing | [STD-0008](../standard/STD-0008-test-file-location.md) |

## Names

| Topic | What it fixes | Material | Entry |
|-------|---------------|----------|-------|
| Case table | `snake_case` functions and variables, trailing-underscore private members, `PascalCase` types and enumerators, `kPascalCase` constants, project-prefixed `ALL_CAPS` macros | diverges [Prefer `underscore_style` names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-camel) (NL.10); [Avoid encoding type information in names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name-type) (NL.5), [Use a consistent naming style](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name) (NL.8), [Use `ALL_CAPS` for macro names only](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-all-caps) (NL.9); additions | [STD-0009](../standard/STD-0009-case-table.md) |
| Operation verb vocabulary | `parse_`, `format_`, `resolve_`, `validate_`, `build_`, `load_`, `write_`, `render_`, `expand_`, `plan_` | additions | [STD-0010](../standard/STD-0010-operation-verb-vocabulary.md) |
| Return-contract prefixes | `is_`/`has_`, `try_`, `get_`, `find_`, `make_` | additions | [STD-0011](../standard/STD-0011-return-contract-prefixes.md) |
| Unit suffixes | `width_mm`, `feed_mm_per_min`, `angle_deg` at every interface | [Make interfaces precisely and strongly typed](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-typed) (I.4), [Avoid names that are easily misread](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-misread) (NL.19) | [STD-0012](../standard/STD-0012-unit-suffixes.md) |
| Name length against scope | Short names in short scopes, longer as scope widens | [Make the length of a name roughly proportional to the length of its scope](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name-length) (NL.7) | [STD-0013](../standard/STD-0013-name-length-against-scope.md) |

## Layout of the line

| Topic | What it fixes | Material | Entry |
|-------|---------------|----------|-------|
| Indentation and brace style | K&R-derived, indent 4, column limit 100 | [Maintain a consistent indentation style](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-indent) (NL.4), [Use K&R-derived layout](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-knr) (NL.17); conventions.md Tooling | [STD-0014](../standard/STD-0014-indentation-and-brace-style.md) |
| Declarator layout | `int* p`, not `int *p` | [Use C++-style declarator layout](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-ptr) (NL.18) | [STD-0015](../standard/STD-0015-declarator-layout.md) |
| `const` notation | Which side of the type `const` sits on | [Use conventional `const` notation](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-const) (NL.26) | [STD-0016](../standard/STD-0016-const-notation.md) |
| One thing per line | One statement per line, one name per declaration | [Don't place two statements on the same line](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-stmt) (NL.20), [Declare one name (only) per declaration](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name-one) (NL.21) | [STD-0017](../standard/STD-0017-one-thing-per-line.md) |
| Whitespace | Where spaces earn their place | [Use spaces sparingly](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-space) (NL.15) | [STD-0018](../standard/STD-0018-whitespace.md) |
| Literal readability | Digit separators, suffixes, no bare unreadable constants | [Make literals readable](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-literals) (NL.11) | [STD-0019](../standard/STD-0019-literal-readability.md) |
| Class member declaration order | Public, then protected, then private | [Use a conventional class member declaration order](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-order) (NL.16) | [STD-0020](../standard/STD-0020-member-declaration-order.md) |
| Empty argument lists | `f()`, never `f(void)` | [Don't use `void` as an argument type](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-void) (NL.25) | [STD-0021](../standard/STD-0021-empty-argument-lists.md) |

## Comments

| Topic | What it fixes | Material | Entry |
|-------|---------------|----------|-------|
| What a comment carries | Intent, not restatement of the code; crisp | [Don't say in comments what can be clearly stated in code](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-comments) (NL.1), [State intent in comments](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-comments-intent) (NL.2), [Keep comments crisp](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-comments-crisp) (NL.3) | [STD-0022](../standard/STD-0022-what-a-comment-carries.md) |

## Toolchain

| Topic | What it fixes | Material | Entry |
|-------|---------------|----------|-------|
| Language standard declaration | Declared once in the top-level build config | additions | [STD-0023](../standard/STD-0023-language-standard-declaration.md) |
| Warning set | `-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror` | additions | [STD-0024](../standard/STD-0024-warning-set.md) |
| Sanitizer configuration | UBSan and ASan always, TSan once concurrency exists | additions | [STD-0025](../standard/STD-0025-sanitizer-configuration.md) |
| Static analysis check families | `bugprone-*`, `cert-*`, `cppcoreguidelines-*`, `performance-*`, `readability-*` | additions | [STD-0026](../standard/STD-0026-static-analysis-check-families.md) |
| Formatter configuration | clang-format, Google baseline, indent 4, column 100 | additions | [STD-0027](../standard/STD-0027-formatter-configuration.md) |
| Build system | CMake by default | additions | [STD-0028](../standard/STD-0028-build-system.md) |
| Test framework | Catch2, GoogleTest, or doctest, one per project | conventions.md Testing | [STD-0029](../standard/STD-0029-test-framework.md) |

## Settled

- **Universal, with the axis available.** No entry carries an `applicability`
  mark today; every topic above holds regardless of C++ version, including the
  standard declaration, which fixes *where* the standard is declared rather than
  which one. The axes exist for the first entry that genuinely varies.
- **Toolchain stays in the corpus and renders separately.** It is one format and
  one loader; `group` decides that the seven toolchain entries land in
  `project-setup.md` and the other twenty-two in `standard.md`. A second artifact
  type would have doubled the machinery to express one grouping.

# Coding standard topics

Temporary. Candidate topics for the coding standard, the document that is
generated once and held as canon.

Working split, and my read rather than yours: a standard topic is one the
project decides once and every file follows, checkable by a tool or at a glance.
A policy is a decision procedure an author applies case by case. Correct the
split and this list changes.

The **Material** column says where the content already sits. Most of these claim
rows in [CG-WORKLIST.md](CG-WORKLIST.md) or
[CONVENTIONS-ADDITIONS.md](CONVENTIONS-ADDITIONS.md) rather than adding
anything new, so a row landing here comes out of there.

## Files and layout

| Topic | What it fixes | Material |
|-------|---------------|----------|
| File extensions | `.hpp` for headers, `.cpp` for sources | diverges [Use a `.cpp` suffix for code files and `.h` for interface files if your project doesn't already follow another convention](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-file-suffix) (SF.1), [Use a `.cpp` suffix for code files and `.h` for interface files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-file-suffix) (NL.27); additions |
| File naming | `snake_case` filenames | conventions.md Naming |
| Directory and namespace layout | `include/proj/layer/`, namespaces nested by layer, `snake_case` | [Use `namespace`s to express logical structure](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-namespace) (SF.20); conventions.md Module Boundary |
| Include guards | `#ifndef PROJECT_COMPONENT_FILE_HPP`, no `#pragma once` | [Use `#include` guards for all header files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-guards) (SF.8); additions |
| Include order and form | Own header first, quoted for local and angle for external, self-contained headers, no reliance on implicit includes | [Include header files before other declarations in a file](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-include-order) (SF.4), [A `.cpp` file must include the header file(s) that defines its interface](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-consistency) (SF.5), [Avoid dependencies on implicitly `#include`d names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-implicit) (SF.10), [Header files should be self-contained](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-contained) (SF.11), [Prefer the quoted form of `#include` for files relative to the including file and the angle bracket form everywhere else](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-incform) (SF.12), [Use portable header identifiers in `#include` statements](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-portable-header-id) (SF.13) |
| `using namespace` placement | Never at header scope, local scope only | [Use `using namespace` directives for transition, for foundation libraries (such as `std`), or within a local scope (only)](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-using) (SF.6), [Don't write `using namespace` at global scope in a header file](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-using-directive) (SF.7) |
| Anonymous namespace | Internal entities in the `.cpp`, never in a header | [Don't use an unnamed (anonymous) namespace in a header](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-unnamed) (SF.21), [Use an unnamed (anonymous) namespace for all internal/non-exported entities](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-unnamed2) (SF.22) |
| Test file location and naming | Where a test lives relative to what it tests | conventions.md Testing |

## Names

| Topic | What it fixes | Material |
|-------|---------------|----------|
| Case table | `snake_case` functions and variables, trailing-underscore private members, `PascalCase` types and enumerators, `kPascalCase` constants, project-prefixed `ALL_CAPS` macros | diverges [Prefer `underscore_style` names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-camel) (NL.10); [Avoid encoding type information in names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name-type) (NL.5), [Use a consistent naming style](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name) (NL.8), [Use `ALL_CAPS` for macro names only](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-all-caps) (NL.9); additions |
| Operation verb vocabulary | `parse_`, `format_`, `resolve_`, `validate_`, `build_`, `load_`, `write_`, `render_`, `expand_`, `plan_` | additions |
| Return-contract prefixes | `is_`/`has_`, `try_`, `get_`, `find_`, `make_` | additions |
| Unit suffixes | `width_mm`, `feed_mm_per_min`, `angle_deg` at every interface | [Make interfaces precisely and strongly typed](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-typed) (I.4), [Avoid names that are easily misread](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-misread) (NL.19) |
| Name length against scope | Short names in short scopes, longer as scope widens | [Make the length of a name roughly proportional to the length of its scope](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name-length) (NL.7) |

## Layout of the line

| Topic | What it fixes | Material |
|-------|---------------|----------|
| Indentation and brace style | K&R-derived, indent 4, column limit 100 | [Maintain a consistent indentation style](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-indent) (NL.4), [Use K&R-derived layout](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-knr) (NL.17); conventions.md Tooling |
| Declarator layout | `int* p`, not `int *p` | [Use C++-style declarator layout](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-ptr) (NL.18) |
| `const` notation | Which side of the type `const` sits on | [Use conventional `const` notation](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-const) (NL.26) |
| One thing per line | One statement per line, one name per declaration | [Don't place two statements on the same line](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-stmt) (NL.20), [Declare one name (only) per declaration](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name-one) (NL.21) |
| Whitespace | Where spaces earn their place | [Use spaces sparingly](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-space) (NL.15) |
| Literal readability | Digit separators, suffixes, no bare unreadable constants | [Make literals readable](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-literals) (NL.11) |
| Class member declaration order | Public, then protected, then private | [Use a conventional class member declaration order](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-order) (NL.16) |
| Empty argument lists | `f()`, never `f(void)` | [Don't use `void` as an argument type](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-void) (NL.25) |

## Comments

| Topic | What it fixes | Material |
|-------|---------------|----------|
| What a comment carries | Intent, not restatement of the code; crisp | [Don't say in comments what can be clearly stated in code](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-comments) (NL.1), [State intent in comments](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-comments-intent) (NL.2), [Keep comments crisp](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-comments-crisp) (NL.3) |

## Toolchain

| Topic | What it fixes | Material |
|-------|---------------|----------|
| Language standard declaration | Declared once in the top-level build config | additions |
| Warning set | `-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror` | additions |
| Sanitizer configuration | UBSan and ASan always, TSan once concurrency exists | additions |
| Static analysis check families | `bugprone-*`, `cert-*`, `cppcoreguidelines-*`, `performance-*`, `readability-*` | additions |
| Formatter configuration | clang-format, Google baseline, indent 4, column 100 | additions |
| Build system | CMake by default | additions |
| Test framework | Catch2, GoogleTest, or doctest, one per project | conventions.md Testing |

## Open

- Whether the standard is per-configuration or universal. Every topic above
  holds regardless of C++ version except the standard declaration itself, which
  argues for universal.
- Whether the toolchain group belongs in the standard at all, or in a separate
  project-setup document. It is the only group that describes the build rather
  than the source.

---
id: POL-0091
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments: static analysis"
---

# Static analysis runs a fixed set of check families

`clang-tidy` runs with `bugprone-*`, `cert-*`, `cppcoreguidelines-*`,
`performance-*`, and `readability-*`.

Disables are project-level, live in `.clang-tidy`, and carry one comment per
disable stating why. A disable list with no comments is a record of what was
inconvenient, not of what was decided.

Per-site `NOLINT` is for the case the check cannot see, and it names the check
it suppresses rather than suppressing everything at that line.

Static analysis is the layer between the compiler and a reader: it finds the
patterns that are well-formed, so no warning applies, and wrong often enough to
be worth naming. Most of what it reports here is already a policy in this
corpus, which is the reason the families are fixed — the check set is the
mechanical half of guidance that otherwise has to be remembered. Choosing the
families per project would let the set drift away from the policies it is
supposed to enforce, and nothing would report that it had.

The tool is due diligence and not how quality is produced. A codebase that
needs its linter in order to be well designed is not well designed; the linter
catches what slipped.

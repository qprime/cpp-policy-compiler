---
id: POL-0090
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments: sanitizers"
enforcement:
  sanitizers: ["undefined", "address"]
---

# The tests run under sanitizers in at least one configuration

UBSan and ASan are enabled in at least one build configuration, and the test
suite runs under it. TSan is added in its own configuration once the project
introduces concurrency.

A sanitizer finding is a defect, and it is a defect of the code rather than of
the configuration. Suppressions are for known issues in third-party code, listed
in a file, each with a reason.

TSan is separate rather than combined because it does not compose with ASan, and
running it before there is concurrency to find reports nothing while costing
every run.

Undefined behaviour is forbidden (POL-0019), and the compiler cannot report most
of it: the whole point of the category is that the standard imposes no
requirement, so a conforming implementation may produce code that appears to
work. That leaves a rule with no mechanism behind it, which is what the
sanitizers supply. They are also the only check here that finds a defect the
author did not think to look for, since they observe what the program actually
did rather than what it was expected to do.

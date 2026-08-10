---
id: POL-0007
kind: principle
precedence: 7
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #7"
---

# Determinism is the default

Same input, same output, on every platform and every run. No dependence on
unordered-container iteration order, on address values, on uninitialized memory,
on wall-clock time, or on platform-dependent floating-point in output that is
compared.

If two runs over the same input can differ, that is a defect even when both
outputs are individually correct.

Non-determinism does not produce a wrong answer. It produces an answer that
cannot be checked. A result that differs between runs cannot be diffed against a
known-good one, so golden tests, reproducible builds, and any claim that a
change was safe all stop working at once.

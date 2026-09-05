---
id: POL-0246
kind: standard
trigger: "write code that produces structured output"
review_trigger: "structured output changes without a complete golden comparison"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# Deterministic structured output has a representative golden test

Toolpaths, plans, schedules, traces, generated code — each deterministic format has
a small representative checked-in golden. Normalize or separately assert volatile
fields such as timestamps and random identifiers. No golden diff is evidence that
the covered output stayed stable, not proof that every behavior is unchanged; a
deliberate regeneration has a reviewed diff and explanation.

```
tests/goldens/pocket_100mm.gcode        # checked in, diffed on every run
```

Adding an alternative to the output is versioned: define it, expose it across the
FFI, document it, regenerate — in that order.

Structured output is where a refactor's unintended effects hide, because the code
still compiles and focused unit tests can pass. A golden is a cheap, reviewable check
that the covered bytes did not move, while semantic assertions cover properties for
which textual identity is too strict.

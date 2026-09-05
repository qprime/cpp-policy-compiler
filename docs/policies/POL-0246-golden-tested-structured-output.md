---
id: POL-0246
kind: standard
trigger: "write code that produces structured output"
review_trigger: "structured output changes without a complete golden comparison"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# Anything producing structured output is golden-tested

Toolpaths, plans, schedules, traces, generated code — each has a checked-in golden.
Every change is one of two things: no golden diff, which proves the change was a
refactor, or a deliberate regeneration whose diff the commit message explains.

```
tests/goldens/pocket_100mm.gcode        # checked in, diffed on every run
```

Adding an alternative to the output is versioned: define it, expose it across the
FFI, document it, regenerate — in that order.

Structured output is where a refactor's unintended effects hide, because the code
still compiles and the unit tests still pass. The golden is the only cheap check that
the bytes did not move, and the commit message is what tells a future reader whether
a diff was intended.

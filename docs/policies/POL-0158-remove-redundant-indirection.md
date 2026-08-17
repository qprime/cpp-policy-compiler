---
id: POL-0158
kind: guideline
attribution:
  - source: standard-practice
    locator: "redundant indirection"
    upstream: ["CG Per.12", "CG Per.13"]
---

# Delete an alias or an indirection that adds nothing

A reference or pointer that only renames something already in scope, and a wrapper
that only forwards, are both noise. Where indirection buys polymorphism or
ownership, keep it.

```cpp
const Tool& tool = job.tool();
use(tool.diameter_mm());

const Tool& tool = job.tool();
const Tool& t = tool;                              // renames for nothing
const double d = t.diameter_mm();
```

The reader has to prove each alias refers to what they think it does, and the
compiler has to prove the same thing before it can keep the value in a register.
Both costs disappear when the alias does.

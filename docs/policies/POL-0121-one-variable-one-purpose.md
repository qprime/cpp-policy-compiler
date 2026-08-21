---
id: POL-0121
kind: standard
trigger: "reuse a name, or a variable, for a second purpose"
attribution:
  - source: standard-practice
    locator: "variable reuse"
    upstream: ["CG ES.12", "CG ES.26"]
---

# One variable, one purpose, and no name reused in a nested scope

Introduce a second name rather than reusing the first for an unrelated value, and
never shadow an outer name with an inner one.

```cpp
const double rough_step_mm = tool.diameter_mm() * 0.6;
const double finish_step_mm = tool.diameter_mm() * 0.15;

double step_mm = tool.diameter_mm() * 0.6;
...
step_mm = tool.diameter_mm() * 0.15;      // same name, different meaning
```

A reused variable makes its name mean different things in different halves of the
function, so a reader must track where the meaning switched. A shadowed name makes
an edit in the inner scope silently stop affecting the outer one.

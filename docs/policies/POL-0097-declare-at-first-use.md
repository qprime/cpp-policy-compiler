---
id: POL-0097
kind: guideline
attribution:
  - source: standard-practice
    locator: "declaration scope"
    upstream: ["CG ES.21", "CG ES.22"]
---

# A variable is declared where it is first used

```cpp
// Avoid. Three names live and meaningless for most of the function.
Plan plan;
double total;
std::string label;
// ... forty lines that do not touch them ...

// Prefer.
const auto plan = build_plan(input);
const auto total = plan.total_mm();
```

Where a value must outlive a branch that computes it, prefer an immediately
invoked helper or a function that returns it over declaring it early and
assigning it later, so it can still be `const` (POL-0020).

A variable declared before it means anything has a region of the function in
which it is live and carries nothing. That region is where a stale read
happens, and it grows every time the function does. Declaring at first use
makes the scope match the meaning, which is also what lets the declaration be
`const` and what makes an unused value visible rather than merely inert.

---
id: POL-0002
kind: principle
precedence: 2
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #2"
    upstream: ["CG P.6", "CG P.7"]
---

# Expected failure modes are visible

A failure the caller is expected to branch on is represented in the function's
return type. Other failures are documented and propagate to a layer that can
act; C++ function types do not generally enumerate the exceptions an operation
may throw. Nothing is swallowed, and no failure is returned as a value that
reads as success.

```cpp
std::optional<Tool> find_tool(const ToolTable& table, int slot);
double lookup_diameter_mm(const ToolTable& table, int slot);  // returns NaN when absent
```

The second signature makes the caller's omission invisible: the NaN propagates
into arithmetic and surfaces as bad geometry somewhere else. In a system whose
output drives a physical machine, a silent wrong answer is the worst available
failure.

---
id: POL-0056
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: named operation"
    upstream: ["CG F.56"]
---

# Reject early; do not nest the happy path

Handle each failure or trivial case as it arises and return. What remains after
the guards is the operation the function is named for, at one level of
indentation.

```cpp
std::optional<Paths> plan(const Job& job) {
    if (job.faces.empty()) { return std::nullopt; }
    if (!job.tool.has_value()) { return std::nullopt; }
    return plan_faces(job.faces, *job.tool);
}
```

Nesting the body inside the success conditions puts the interesting code furthest
from the left margin and separates each `if` from its `else` by the whole
function. Guards keep the precondition next to the reason it exists.

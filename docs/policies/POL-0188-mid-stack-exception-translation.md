---
id: POL-0188
kind: anti-pattern
trigger: "catch and rethrow a different type"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: mid-stack exception translation"
    upstream: ["CG E.17", "CG E.18"]
replacement: ["POL-0187"]
---

# Catching at every layer to rethrow a different type

```cpp
Paths plan(const Job& job) {
    try {
        return plan_faces(job);
    } catch (const GeometryError& e) {
        throw PlanError(std::string("plan failed: ") + e.what());   // no
    }
}
```

Each layer adds a wrapper, and by the time the exception reaches a handler that can
act, the original type is gone and the message is a chain of prefixes. The noise
also buries the one layer that does real handling.

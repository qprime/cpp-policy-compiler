---
id: POL-0116
kind: anti-pattern
trigger: "reach for a shared_ptr"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: reflexive shared_ptr"
    upstream: ["CG R.21"]
replacement: ["POL-0044"]
---

# `std::shared_ptr` as the default for anything heap-allocated

Reaching for `shared_ptr` because the ownership question is unresolved hides the
question and buys an atomic refcount the design does not need.

```cpp
std::shared_ptr<Toolpath> path = std::make_shared<Toolpath>(...);   // one owner
std::shared_ptr<MachineConfig> config_;                            // never shared
```

Shared ownership means several owners with no primary and independent lifetimes.
Where that is not the case, `shared_ptr` adds shared control-block bookkeeping,
makes the lifetime harder to determine by inspection, and permits ownership
cycles that do not release themselves. Exact synchronization costs are an
implementation detail and depend on the operation.

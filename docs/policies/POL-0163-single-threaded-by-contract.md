---
id: POL-0163
kind: standard
trigger: "write a type that will be reached from more than one thread"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.1"]
---

# A type is single-threaded by contract until its header says otherwise

Write no synchronization by default. Concurrent access is the caller's problem
until the type states a threading model, and where a module has one, it says so in
one or two sentences at the top of its header.

```cpp
// plan_2d.hpp
// Threading: Planner is not thread-safe. One instance per thread, or serialize
// calls externally. ToolTable is immutable after construction and may be shared.
```

```cpp
class Toolpath {
    std::mutex mutex_;              // guarding what, against whom?
};
```

A mutex on a class with no documented threading model is cosplay: it does not make
compound operations atomic, it does not stop a caller from holding a reference
across the lock, and it costs an uncontended lock on every call. Stating the model
is what lets a caller reason; adding a mutex only looks like it does.

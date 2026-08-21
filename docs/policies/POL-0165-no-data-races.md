---
id: POL-0165
kind: standard
trigger: "reach shared mutable state"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.2", "CG CP.3"]
---

# Shared mutable state is reached under a lock or through an atomic, and there is as little of it as possible

Prefer to share nothing: give each thread its own data, pass values between them,
and keep shared state immutable after construction. What remains shared and mutable
is guarded.

```cpp
const ToolTable table = load_tool_table(path);      // immutable: shared freely
std::atomic<bool> stop_requested{false};            // one word: atomic
```

Two threads touching the same non-atomic object, at least one of them writing, is
undefined behaviour — not a torn read, but a program the compiler may transform on
the assumption it never happens. Reducing the shared set is the only fix that
scales; guarding it is what you do with the remainder.

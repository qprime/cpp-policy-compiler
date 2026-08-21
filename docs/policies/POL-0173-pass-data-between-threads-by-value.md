---
id: POL-0173
kind: standard
trigger: "pass data to another thread"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.31", "CG CP.32"]
---

# Small data crosses a thread boundary by value; shared ownership crosses as `shared_ptr`

Copy the value into the task. Where the object is large and genuinely shared
between threads with no primary owner, hand over a `std::shared_ptr`.

```cpp
auto plan = std::async(std::launch::async, plan_face, face, params);   // copies

auto table = std::make_shared<const ToolTable>(load_tool_table(path));
auto a = std::async(std::launch::async, plan_with, table, face_a);     // shared, const
```

A reference or pointer into the spawning frame dangles as soon as that frame
returns, and nothing diagnoses it. `shared_ptr` makes the lifetime independent of
either thread's stack, which is the only reason to reach for it here.

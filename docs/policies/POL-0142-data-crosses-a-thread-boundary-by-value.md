---
id: POL-0142
kind: standard
attribution:
  - source: standard-practice
    locator: "concurrency, passing data between threads"
    upstream: ["CG CP.31", "CG CP.32"]
---

# Small data crosses a thread boundary by value; shared ownership is `shared_ptr`

```cpp
// Never. The caller's frame may be gone before the task reads it.
std::jthread worker([&request] { handle(request); });

// Right. The task owns its input.
std::jthread worker([request] { handle(request); });

// Right, where two unrelated threads genuinely both own it.
auto table = std::make_shared<const ToolTable>(load_tools(path));
std::jthread worker([table] { plan_with(*table); });
```

By value is the default: a copy removes the lifetime question and the
synchronization question at once, and for small data it costs less than the lock
that would otherwise be needed.

Where the data is large or genuinely shared between threads with no clear
primary owner, `std::shared_ptr` is the mechanism — this is the case POL-0048
holds it open for. Prefer `shared_ptr<const T>`, so sharing does not also mean
shared mutation.

A reference passed to another thread is a lifetime claim that no signature
states and no compiler checks: the referent must outlive a thread whose end the
caller may not wait for. When it does not, the read is undefined and lands
wherever that memory has been reused, which is the failure POL-0002 ranks worst
because nothing downstream can tell it from a correct value.

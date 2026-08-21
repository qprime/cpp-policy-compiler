---
id: POL-0053
kind: standard
trigger: "write a lambda capture list"
attribution:
  - source: testimony/coding-rules-2026-07.md
    locator: "Lambdas #2"
    upstream: ["CG F.54"]
---

# Capture each variable explicitly; no `[=]`, no `[&]`

List what the lambda carries. This holds especially inside a member function,
where `[=]` captures `this` and so captures every member by reference under a
syntax that looks like copying.

```cpp
auto within = [tolerance_mm, &visited](const Move& move) { ... };

auto within = [=](const Move& move) { ... };        // what does it hold? this?
```

The capture list is the one part of a lambda with lifetime consequences, so it is
the part that must be readable at a glance. A default capture hides which state
the lambda depends on and turns a dangling capture into something you can only
find by reading the enclosing function.

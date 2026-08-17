---
id: POL-0114
kind: standard
attribution:
  - source: testimony/coding-rules-2026-07.md
    locator: "Lambdas 2"
  - source: standard-practice
    locator: "lambdas, capture list"
    upstream: ["CG F.54"]
---

# A lambda names every capture; `[=]` and `[&]` are not written

```cpp
// Never. What state does this carry? The list is the only place that says.
auto ready = [&] { return count >= limit && !cancelled; };

// Right.
auto ready = [&count, &limit, &cancelled] { return count >= limit && !cancelled; };
```

`[this]` counts as a default: it captures the whole object, so a lambda written
inside a member function reaches every member without naming one. Capture the
members it uses, by value.

The capture list is the only part of a lambda with lifetime consequences, and a
default capture hides exactly that. `[&]` binds whatever the body happens to
name, so adding one identifier to the body silently extends what the lambda
borrows, and nothing in the diff shows a lifetime changed. An explicit list
makes the ownership question answerable from the declaration, which is what
POL-0003 asks of every other construct.

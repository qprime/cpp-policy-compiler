---
id: POL-0019
kind: guideline
trigger: "write a precondition no type can carry"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Divergences: [CG I.6], [CG I.8]"
    upstream: ["CG I.6", "CG I.8"]
---

# A non-structural precondition is asserted, not declared with a macro

Where a precondition cannot be carried by a type, `assert` it at function entry
and say what it is. Do not take a GSL dependency for `Expects()` and `Ensures()`,
and do not hand-roll the macros unless one header defines them for the whole
project.

```cpp
double chip_load_mm(const Tool& tool, double feed_mm_per_min) {
    assert(feed_mm_per_min >= 0.0);
    ...
}
```

The concept is adopted; the dependency is not. A third-party library in an FFI
kernel is not worth two macros, and `std::span` — the GSL facility with real
value — is in C++20.

Frequent asserts of the same precondition are a missing wrapper type. If three
callers assert what the callee also asserts, the precondition wants to be a
type.

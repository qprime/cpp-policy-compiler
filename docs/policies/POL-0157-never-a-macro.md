---
id: POL-0157
kind: anti-pattern
replacement: [POL-0010, POL-0036]
attribution:
  - source: standard-practice
    locator: "macros"
    upstream: ["CG ES.30", "CG ES.31", "CG ES.33"]
---

# Never define a macro for a constant, a function, or program text

```cpp
// Never. No type, no scope, and MIN(i++, j) evaluates i++ twice.
#define MAX_TOOLS 64
#define MIN(a, b) ((a) < (b) ? (a) : (b))

// Right.
constexpr int kMaxTools = 64;
constexpr auto smaller = [](auto a, auto b) { return std::min(a, b); };
```

A constant is `constexpr` (POL-0010), a function is a function or a `constexpr`
function (POL-0036), and a compile-time choice is `if constexpr` rather than
`#if`.

The exceptions are an include guard (POL-0028) and the small set of macros a
platform or test framework requires. Those are `ALL_CAPS` and project-prefixed,
per POL-0084, precisely because they have no scope and a short name will collide.

A macro is a textual substitution performed before the compiler sees a type, so
it obeys no scope, appears in no diagnostic, and is invisible to the debugger.
An argument used twice in the body is evaluated twice, which turns any argument
with a side effect into a defect that the call site cannot see.

`ALL_CAPS` is reserved for macros for this reason: the name is the only warning a
reader gets that ordinary language rules do not apply on that line.

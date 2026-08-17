---
id: POL-0116
kind: guideline
attribution:
  - source: testimony/coding-rules-2026-07.md
    locator: "Lambdas 1"
  - source: standard-practice
    locator: "lambdas, when to reach for one"
    upstream: ["CG F.11", "CG F.50", "CG T.40", "CG T.141", "CG C.170", "CG ES.28"]
---

# A lambda is trivial glue at one call site; anything else is a named function

```cpp
// Prefer. One use, one line, reads better inline than as a jump to a name.
std::ranges::sort(moves, [](const Move& a, const Move& b) { return a.z < b.z; });

// Prefer a function. Two uses, and it wants a name to be understood.
bool is_finishing_pass(const Move& m);
```

A lambda also earns its place initializing a `const` value that needs several
statements to compute, which is the one case where the alternative is a
non-`const` variable assigned later (POL-0020).

Where a lambda would be overloaded on argument type, write one generic lambda
rather than a set.

A lambda buys locality, not brevity. It is justified when reading the body in
place beats jumping to a name, which is true for a comparator and false for
anything a reader would need to think about. Once it wants a name, wants a
comment, or acquires a second use, it is a function that has not been given its
name yet, and POL-0030 already says what to do about that.

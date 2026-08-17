---
id: POL-0068
kind: anti-pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: stringly-typed dispatch"
replacement: ["POL-0066"]
---

# A `kind` string with optional payload members

A struct carrying `std::string kind` plus a payload for each possible kind is a
tagged union with no checking whatsoever. An `enum class` paired with an
if/else-if chain is only half a fix: the enum is a real type, but nothing forces
the chain to handle every case.

```cpp
struct Move {                                  // no
    std::string kind;                          // "rapid", "cut", "comment"
    std::optional<double> x, y, z, feed;
    std::string text;
};
```

Every consumer re-parses the string, a typo is a runtime miss rather than a
compile error, and the valid combinations of payload members live in nobody's
head.

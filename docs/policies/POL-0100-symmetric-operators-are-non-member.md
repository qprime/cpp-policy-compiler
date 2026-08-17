---
id: POL-0100
kind: standard
attribution:
  - source: standard-practice
    locator: "operator placement"
    upstream: ["CG C.161", "CG C.168"]
---

# A symmetric operator is a non-member in the namespace of its operands

Write it as a hidden friend, or as a free function beside the type. Member form is
for the asymmetric ones — assignment, `[]`, `->`, `()`.

```cpp
struct Feed {
    double mm_per_min = 0.0;
    friend bool operator<(Feed a, Feed b) { return a.mm_per_min < b.mm_per_min; }
};
```

A member operator applies conversions only to its right operand, so
`1200.0 < feed` and `feed < 1200.0` do not both compile. Defining it in the
operands' namespace is what lets argument-dependent lookup find it from generic
code that never named the namespace.

---
id: POL-0154
kind: standard
attribution:
  - source: standard-practice
    locator: "boolean conditions"
    upstream: ["CG ES.87"]
---

# A condition that is already `bool` is not compared to one

```cpp
if (is_closed(poly)) { ... }
if (!moves.empty()) { ... }

if (is_closed(poly) == true) { ... }
if (moves.empty() != true) { ... }
```

The comparison adds a token and a negation for the reader to unwind and says
nothing the expression did not already say. Where the value is not a `bool` —  a
pointer, an integer — the explicit comparison is the right form and states which
test is meant.

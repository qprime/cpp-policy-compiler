---
id: POL-0112
kind: standard
attribution:
  - source: standard-practice
    locator: "comments"
    upstream: ["CG NL.1"]
---

# A comment states what the code cannot

```cpp
// Right: an identity the reader cannot derive from the expression.
// Shoelace formula; sign of the result gives the winding direction.
const auto area2 = cross(a, b) + cross(b, c) + cross(c, a);

// Right: a load-bearing assumption the types do not carry.
// Caller holds scan_mutex_; this runs inside the scan window.
void append_trace(const Fault& f);
```

The three cases are a non-obvious identity or derivation, an assumption the
code depends on and the types do not express, and the reason for a choice that
otherwise reads as arbitrary.

No docstring block on every function, and no running prose narrating the next
few lines. Volume trains the reader to skip comments, which costs the few that
carry something.

Everything else the name carries instead, which is POL-0006 applied to the
comment case. A comment is the fallback for what naming cannot reach, so its
value depends entirely on being rare: a reader who has learned that comments
here are load-bearing will read them, and a reader who has learned they restate
the code will skip the one that mattered.

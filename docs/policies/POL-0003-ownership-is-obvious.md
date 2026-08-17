---
id: POL-0003
kind: principle
precedence: 3
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #3"
    upstream: ["CG P.8"]
---

# Ownership is obvious from the declaration

Anyone reading a declaration answers *who owns this* in under five seconds. If
they cannot, the declaration is wrong, not the reader.

```cpp
std::unique_ptr<Spindle> spindle_;   // this object owns it
const Spindle& spindle_;             // someone else owns it, outlives us
Spindle* spindle_;                   // someone else owns it, may be absent
```

RAII by default means the answer is always in the type. A resource whose owner
has to be reconstructed from call sites has no owner, only habits.

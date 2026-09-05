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

Anyone reading a declaration can distinguish ownership from borrowing. If a
borrow is retained, its required lifetime is part of the surrounding interface
contract rather than an assumption reconstructed from call sites.

```cpp
std::unique_ptr<Spindle> spindle_;   // this object owns it
const Spindle& spindle_;             // someone else owns it, outlives us
Spindle* spindle_;                   // someone else owns it, may be absent
```

RAII makes resource ownership visible in the owning type. A reference or pointer
states that it does not own; the API that retains one must also make the actual
owner and lifetime relationship clear.

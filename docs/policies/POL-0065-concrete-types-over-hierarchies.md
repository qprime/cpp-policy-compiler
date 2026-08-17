---
id: POL-0065
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: is inheritance right"
    upstream: ["CG C.10", "CG C.120", "CG C.129", "CG C.132"]
---

# Prefer a concrete type; inherit only for an open set of behaviours

Work down the list.

| Question | Answer |
|----------|--------|
| Is this a fixed set of alternatives? | Not inheritance — closed-set variation |
| Is it an open set of behaviours injected by a caller? | An abstract interface with no data |
| Is it code reuse? | Not inheritance — composition, or a free function |
| Do I have at least two concrete cases in hand? | If not, write the function. Decide on the second |

```cpp
class Move { public: virtual ~Move() = default; };   // Rapid, Cut derive: no
using Move = std::variant<Comment, SetRpm, Rapid, Cut>;   // instead
```

Inheritance shares implementation and is not how variation is represented. A
hierarchy costs an allocation, a pointer chase, and the compiler's ability to tell
you a case is missing — and it does that whether or not the set is actually open.

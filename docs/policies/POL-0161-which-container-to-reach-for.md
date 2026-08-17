---
id: POL-0161
kind: guideline
attribution:
  - source: standard-practice
    locator: "containers"
    upstream: ["CG SL.con.2"]
---

# `std::vector` unless something else is required

| Need | Container |
|------|-----------|
| A sequence | `std::vector` |
| A fixed size known at compile time | `std::array` |
| Keyed lookup | `std::unordered_map`, or `std::map` where iteration order must be deterministic |
| Membership | `std::unordered_set`, or `std::set` on the same condition |
| Stable addresses across insertion | `std::deque`, or `std::vector` of `std::unique_ptr` |

`std::list` is not a default. It is the answer only where splicing is the
operation and it has been measured.

Iteration order over an unordered container is unspecified, so anything derived
from it that reaches output must be sorted first, or the container must be an
ordered one. That is POL-0007 directly: the output differs between runs and
between standard library versions, and the golden test that would have caught it
is the thing that breaks.

`std::vector` is the default because contiguous storage is what current hardware
is fastest at traversing, and because it is the container every reader already
understands (POL-0004). Departing from it is a decision with a reason, and the
reason belongs in the code as a comment where it is not obvious (POL-0112).

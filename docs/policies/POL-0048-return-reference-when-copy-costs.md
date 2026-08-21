---
id: POL-0048
kind: guideline
trigger: "return a reference"
attribution:
  - source: standard-practice
    locator: "reference returns"
    upstream: ["CG F.44"]
---

# Return `T&` when a copy is wasteful and *no object* is not a possible answer

Return a reference from an accessor onto storage the object owns and outlives the
call. If the answer might be *nothing*, return `std::optional` or a pointer
instead.

```cpp
const std::vector<Move>& moves() const { return moves_; }   // borrow, no copy
Vec2 origin_mm() const { return origin_mm_; }               // small: return by value
```

A reference return commits the caller to the object staying alive, which is
correct for an accessor and wrong for anything computed. Small values are cheaper
copied than indirected, so the reference buys nothing there.

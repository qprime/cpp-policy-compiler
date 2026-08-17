---
id: POL-0080
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "8. Special members and value semantics"
    upstream: ["CG C.66"]
---

# Move operations are `noexcept`

Write `noexcept` on the move constructor and move assignment. If a member's move
can throw, hold it by `std::unique_ptr` so the move becomes a pointer swap.

```cpp
Toolpath(Toolpath&&) noexcept = default;
Toolpath& operator=(Toolpath&&) noexcept = default;
```

`std::vector` reallocation uses moves only when they are `noexcept`; otherwise it
copies every element to keep its exception guarantee. Without the annotation a
type looks movable and behaves like a copy at every growth point.

---
id: POL-0084
kind: guideline
trigger: "write a swap"
attribution:
  - source: standard-practice
    locator: "swap"
    upstream: ["CG C.83", "CG C.84", "CG C.85"]
---

# Where a type needs `swap`, it is `noexcept` and cannot fail

Most types need no `swap` — the generated move operations make `std::swap`
correct. Where a member `swap` earns its place, it exchanges members and is
declared `noexcept`.

```cpp
void Toolpath::swap(Toolpath& other) noexcept {
    moves_.swap(other.moves_);
    std::swap(length_mm_, other.length_mm_);
}
```

`swap` is the primitive that copy assignment, `std::sort`, and every rollback path
are built on, so a throwing `swap` leaves both objects in an unknown state with
no way to recover either. Exchanging members is inherently non-throwing;
allocating inside `swap` is what breaks the guarantee.

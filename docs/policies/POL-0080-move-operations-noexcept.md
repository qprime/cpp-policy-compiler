---
id: POL-0080
kind: standard
trigger: "declare a move constructor or move assignment operator"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "8. Special members and value semantics"
    upstream: ["CG C.66"]
---

# A move operation is `noexcept` exactly when moving every member is non-throwing

Default the move operations where possible and let their exception specifications
follow their members. For a user-written move, state `noexcept` only when every
operation it performs is non-throwing. Do not change value semantics or add an
allocation merely to manufacture that guarantee.

```cpp
Toolpath(Toolpath&&) noexcept = default;
Toolpath& operator=(Toolpath&&) noexcept = default;
```

Containers can prefer copying during reallocation when a throwing move would
prevent their exception guarantee. That is a reason to preserve a truthful
non-throwing move when the representation provides one, never to write a false
specification: throwing through it calls `std::terminate`.

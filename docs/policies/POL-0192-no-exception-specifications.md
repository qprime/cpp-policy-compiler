---
id: POL-0192
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "13. Standard-specific bans"
    upstream: ["CG E.30"]
---

# The only exception specification is `noexcept`

```cpp
void write(std::span<const std::byte> bytes);
Toolpath(Toolpath&&) noexcept;

void write(std::span<const std::byte> bytes) throw(IoError);   // removed from the language
```

Dynamic exception specifications were deprecated in C++11 and removed in C++17, and
where they still compile they check at run time by calling `std::unexpected` rather
than at compile time. `noexcept` is the one form the language kept, and it means
*nothing escapes*, not *these things escape*.

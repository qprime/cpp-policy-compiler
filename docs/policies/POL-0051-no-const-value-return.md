---
id: POL-0051
kind: standard
attribution:
  - source: standard-practice
    locator: "const-qualified returns"
    upstream: ["CG F.49"]
---

# Do not return `const T` by value

Return `T`. Keep `const` on reference and pointer returns, where it says the
caller may not write through the handle.

```cpp
Bounds bounds_of(const Polygon& poly);              // yes
const Bounds bounds_of(const Polygon& poly);        // no
const std::vector<Move>& moves() const;             // yes: const is doing work
```

On a by-value return the `const` cannot protect the caller — they own the object
— and it blocks moving out of the result, silently turning moves into copies at
every call site.

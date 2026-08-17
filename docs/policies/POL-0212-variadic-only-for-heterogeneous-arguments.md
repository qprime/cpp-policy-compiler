---
id: POL-0212
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "9. Generic code"
    upstream: ["CG T.102", "CG T.103"]
---

# A variadic template is for arguments of differing types; a sequence view is for the rest

Where the arguments are all the same type, take a `std::span`, a
`std::initializer_list`, or a container. Where they genuinely differ, expand the pack
with a fold expression or a `for` over an initializer list — not recursion.

```cpp
double total_length_mm(std::span<const Move> moves);          // homogeneous

template <class... Args>
std::string join(const Args&... parts) {
    std::string out;
    (out.append(to_string(parts)), ...);                       // fold, not recursion
    return out;
}
```

A variadic template over one type instantiates a separate function per argument
count, so twenty call sites produce twenty function bodies for one operation. Pack
recursion does the same thing per depth and produces error messages proportional to
the pack length.

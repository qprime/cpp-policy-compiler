---
id: STD-0024
group: toolchain
enforced_by: build
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
---

# Warnings are `-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror`

```cmake
add_compile_options(-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror)
```

`-Werror=switch` is load-bearing where exhaustive dispatch rests on the warning
system rather than on the type system.

Any per-site disable carries a comment saying what it permits and why.

```cpp
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wconversion"
// Clipper's API takes int64 coordinates; the scale factor bounds the range.
const auto scaled = static_cast<std::int64_t>(value_mm * kClipperScale);
#pragma GCC diagnostic pop
```

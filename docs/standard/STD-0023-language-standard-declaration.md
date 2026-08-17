---
id: STD-0023
group: toolchain
enforced_by: build
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
    upstream: ["CG P.2"]
---

# The language standard is declared once, in the top-level build configuration

```cmake
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
```

No per-target override, no per-file pragma. Reaching for a feature from a later
standard than the one declared is a bug, not an upgrade, and the mechanism matrix
is read against this declaration.

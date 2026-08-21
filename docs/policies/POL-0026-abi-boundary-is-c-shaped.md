---
id: POL-0026
kind: standard
trigger: "expose an interface across a compiler or language boundary"
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
    upstream: ["CG I.26"]
---

# A cross-compiler boundary is a C-shaped interface

Where a binary must be consumed by a toolchain you do not control, the exported
surface is `extern "C"`: trivially copyable types, explicit lengths, no
exceptions, no C++ types in signatures. Everything C++ lives behind it.

```cpp
extern "C" {
struct PathBuffer { double* xy; std::size_t count; };
int plan_pocket_c(const PathBuffer* face, double step_over_mm, PathBuffer* out);
}
```

C++ has no stable ABI across compilers or standard-library versions, so a
`std::string` or `std::vector` in an exported signature is a crash waiting for a
version skew. The C subset is the only shape both sides agree on.

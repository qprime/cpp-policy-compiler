---
id: POL-0216
kind: standard
trigger: "call C code from C++"
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
    upstream: ["CG CPL.1", "CG CPL.2", "CG CPL.3"]
---

# A C library remains C and is reached through one C++ wrapper

Prefer a C++ library. Where C is unavoidable, compile the C source with its supported
C compiler and link it through its declared C ABI. Give it one C++ wrapper that owns
resources and converts errors; ordinary C++ callers do not see the raw C API. Do not
assume valid C has the same meaning—or is valid at all—when compiled as C++.

```cpp
class ClipperPaths {                     // the only code that touches clipper_*
 public:
    explicit ClipperPaths(const Polygon& poly);
    ~ClipperPaths();
    Polygon offset(double delta_mm) const;   // throws on clipper_* failure
};
```

The C API has no destructors, so every caller that touches it directly owns a
cleanup obligation on every path out. One wrapper converts that into RAII once, and
converts the error codes into the module's failure mechanism at the same seam.

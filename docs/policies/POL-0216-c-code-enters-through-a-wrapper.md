---
id: POL-0216
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
    upstream: ["CG CPL.1", "CG CPL.2", "CG CPL.3"]
---

# C code is compiled as C++ and reached through a C++ wrapper

Prefer a C++ library. Where C is unavoidable, keep the C source in the common subset
of the two languages, compile it as C++, and give it one C++ wrapper that owns its
resources and converts its errors. Callers never see the C API.

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

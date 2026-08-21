---
id: POL-0211
kind: guideline
trigger: "expose a template across an ABI-stable interface"
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
    upstream: ["CG T.84"]
---

# Where an interface must be ABI-stable, the template is a thin layer over a non-template core

Put the work in a non-template function taking erased types, and let the template do
nothing but convert and call.

```cpp
namespace detail {
double area_mm2_impl(const double* xy, std::size_t count);      // the ABI
}

template <class Shape>
double area_mm2(const Shape& shape) {
    return detail::area_mm2_impl(shape.data(), shape.size());
}
```

A template has no ABI at all — it is code the consumer instantiates — so a change to
its body changes their binary and a mismatch between their instantiation and yours is
undefined behaviour. The non-template core is the only part that can carry a version
guarantee.

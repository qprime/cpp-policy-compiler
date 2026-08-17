---
id: POL-0207
kind: standard
attribution:
  - source: standard-practice
    locator: "template name lookup"
    upstream: ["CG T.60"]
---

# A template depends on its parameters and on nothing else in scope

Everything the body needs arrives through the template parameters, the function
parameters, or a qualified name. No unqualified calls except deliberate customization
points, and no reliance on names the instantiation context happens to provide.

```cpp
template <class Shape>
double margin_mm(const Shape& shape) {
    return proj::geom::area_mm2(shape) / proj::geom::perimeter_mm(shape);
}
```

Unqualified names in a template are resolved partly at instantiation, so the same
template can mean different things in two translation units. Qualifying makes the
template's meaning a property of its definition.

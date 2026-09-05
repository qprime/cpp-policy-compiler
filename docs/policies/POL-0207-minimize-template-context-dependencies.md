---
id: POL-0207
kind: standard
trigger: "name something inside a template that its parameters do not carry"
attribution:
  - source: standard-practice
    locator: "template name lookup"
    upstream: ["CG T.60"]
---

# A template makes non-parameter dependencies explicit and stable

Everything the body needs arrives through template parameters, function parameters,
or a qualified stable dependency. Use an unqualified dependent call only for a
deliberate customization point; do not accidentally rely on names supplied by the
instantiation context.

```cpp
template <class Shape>
double margin_mm(const Shape& shape) {
    return proj::geom::area_mm2(shape) / proj::geom::perimeter_mm(shape);
}
```

Unqualified names in a template are resolved partly at instantiation, so the same
template can mean different things in two translation units. Qualifying makes the
template's meaning a property of its definition.

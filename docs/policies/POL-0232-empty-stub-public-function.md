---
id: POL-0232
kind: anti-pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: empty-stub public function"
replacement: ["POL-0231"]
---

# A public function returning `{}` because it is not written yet

```cpp
std::optional<Span> find_sliver_span(const Polygon& poly, double tool_diameter_mm) {
    return {};                     // TODO
}
```

`{}` is what this function returns when it legitimately finds nothing, so no caller
can tell the difference and no test can catch it. The `TODO` is visible only to
someone already reading the body — which is the one place the defect does not
matter.

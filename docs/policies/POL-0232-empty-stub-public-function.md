---
id: POL-0232
kind: anti-pattern
trigger: "return an empty value from a function you have not written yet"
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
can tell the difference from the return value alone and ordinary empty-result tests
can accidentally bless it. A test expecting non-empty output may catch this case,
but the `TODO` remains invisible to callers and bindings; absence or a loud failure
makes the unfinished contract unambiguous.

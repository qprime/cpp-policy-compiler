---
id: STD-0009
group: names
enforced_by: clang-tidy
attribution:
  - source: cpp-convention/conventions.md
    locator: "Naming"
    upstream: ["CG NL.5", "CG NL.8", "CG NL.9", "CG NL.10", "CG ES.9", "CG Enum.5", "CG ES.32", "CG ES.33"]
---

# Case is fixed by kind

| Kind | Case | Example |
|------|------|---------|
| Functions, variables, parameters, members | `snake_case` | `plan_pocket`, `step_over_mm` |
| Private data members | `snake_case_` trailing underscore | `diameter_mm_` |
| Types — class, struct, enum, alias | `PascalCase` | `ConvexPolygon`, `PocketParams` |
| Enumerators | `PascalCase` | `PocketStrategy::Spiral` |
| Constants — `constexpr`, `const` at namespace scope | `kPascalCase` | `kMinMarginMm` |
| Macros | `ALL_CAPS`, project-prefixed | `PROJ_ASSERT` |
| Namespaces | `snake_case`, nested by layer | `proj::algo` |

`ALL_CAPS` is only ever a macro. No type information is encoded in a name — no
`p_tool`, no `str_name`, no `m_count`.

```cpp
namespace proj::algo {

constexpr double kMinMarginMm = 10.0;

class ConvexPolygon {
 public:
    double area_mm2() const;

 private:
    Polygon points_;
};

}  // namespace proj::algo
```

The table is mandated machine-wide rather than chosen per project because names
must cross the FFI boundary unchanged, and that is unachievable if either side
picks its own case.

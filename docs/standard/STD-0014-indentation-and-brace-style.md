---
id: STD-0014
group: layout-of-the-line
enforced_by: clang-format
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
    upstream: ["CG NL.4", "CG NL.17"]
---

# Indentation is four spaces; the column limit is 100; braces are K&R-derived

Opening braces stay on the same line as the declaration or statement that owns
them, following the Google baseline. Access specifiers indent one space. No tabs.

```cpp
namespace proj::algo {

Paths plan_pocket(const PlanarFace& face, const Tool& tool,
                  const PocketParams& params) {
    if (face.empty()) {
        return {};
    }
    return plan_rings(build_inset_rings(face, params.step_over_mm));
}

}  // namespace proj::algo
```

```cpp
class Tool {
 public:
    double diameter_mm() const;

 private:
    double diameter_mm_;
};
```

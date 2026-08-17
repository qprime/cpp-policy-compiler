---
id: POL-0225
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Logging"
    upstream: ["CG SL.io.3"]
---

# Library code emits through the logger; streams belong to entry points

`std::cout`, `std::cerr`, and `printf` appear in `main` and in CLI code. Everywhere
else, diagnostics go to the structured logger and results come back as return values.

```cpp
// planner/plan_2d.cpp
Paths plan_pocket(const PlanarFace& face, const PocketParams& params) {
    if (params.step_over_mm > face.width_mm()) {
        log_warning("plan_pocket: step_over_mm {} exceeds face width {}",
                    params.step_over_mm, face.width_mm());
    }
    ...
}
```

One stream write left in a deep helper spams every run thereafter, cannot be
filtered by level, and interleaves unpredictably when anything runs concurrently. It
also makes the function unusable from a library consumer who has their own output
discipline.

Where formatted output is genuinely needed at an entry point, `std::format` is the
mechanism; `printf` is not type-checked and `ostringstream` in new code on C++20 is a
defect.

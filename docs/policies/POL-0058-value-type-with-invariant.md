---
id: POL-0058
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: value type with invariant"
    upstream: ["CG C.2", "CG C.8", "CG C.40", "CG C.41", "CG C.42", "CG E.5"]
---

# A type with an invariant establishes it in its constructor

Ask whether the members can vary independently. If they can, write an aggregate
`struct`. If some combination must never exist, write a `class` whose constructor
is the only way in and which throws when the input is invalid.

```cpp
struct Vec2 {
    double x = 0.0;
    double y = 0.0;
};
```

```cpp
class Tool {
 public:
    Tool(double diameter_mm, double rpm);

    double diameter_mm() const { return diameter_mm_; }
    double radius_mm() const { return 0.5 * diameter_mm_; }
    double rpm() const { return rpm_; }

 private:
    double diameter_mm_;
    double rpm_;
};

Tool::Tool(double diameter_mm, double rpm)
    : diameter_mm_(diameter_mm), rpm_(rpm) {
    if (diameter_mm <= 0.0) {
        throw std::invalid_argument("Tool: diameter_mm must be > 0, got " +
                                    std::to_string(diameter_mm));
    }
    if (rpm < 0.0) {
        throw std::invalid_argument("Tool: rpm must be >= 0, got " +
                                    std::to_string(rpm));
    }
}
```

Where a caller wants to test rather than catch, add a static `try_from` beside
the constructor that delegates to it rather than duplicating the checks.

Without the invariant, every consumer defends itself, and two consumers pick two
different fallbacks. That divergence is silent and shows up in the output, not at
the call site.

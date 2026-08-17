---
id: STD-0019
group: layout-of-the-line
enforced_by: review
attribution:
  - source: standard-practice
    locator: "numeric literals"
    upstream: ["CG NL.11"]
---

# Literals are written to be read

Digit separators above four digits. An explicit suffix where the type matters. A
leading zero on a fraction. Lowercase `0x`, uppercase hex digits.

```cpp
constexpr int kMaxSteps = 1'000'000;
constexpr double kMinMarginMm = 0.5;
constexpr auto kMask = 0xFF00u;
constexpr float kEpsilon = 1.0e-6f;

constexpr int kMaxSteps = 1000000;
constexpr double kMinMarginMm = .5;
```

A name is still required for any literal that carries meaning; readability applies
to the literals that survive that rule.

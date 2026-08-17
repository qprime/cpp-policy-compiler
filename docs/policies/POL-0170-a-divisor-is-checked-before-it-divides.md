---
id: POL-0170
kind: standard
attribution:
  - source: standard-practice
    locator: "arithmetic preconditions"
    upstream: ["CG ES.105"]
---

# A divisor is established non-zero before the division, not after

```cpp
// Never. Integer division by zero is undefined behaviour, not an exception.
const auto per_pass = total_depth_mm / pass_count;

// Right, at a boundary: reject it (POL-0005).
if (pass_count <= 0) {
    return std::unexpected(PlanError::NoPasses);   // POL-0011 message at the throw site
}

// Right, inside: the type already established it.
const auto per_pass = total_depth_mm / passes.count();   // PassCount cannot be zero
```

Where the same division happens in several places, the check belongs in a type
that establishes the precondition once (POL-0027), not at each call site
(POL-0045).

Integer division by zero is undefined behaviour, so it does not reliably trap —
the compiler may assume it cannot happen and remove the branch that would have
detected it, and the observable result depends on the target.

Floating-point division by zero is defined and produces infinity or NaN, which
is worse for this corpus: the value propagates silently through every subsequent
computation and reaches output as a number-shaped thing that is not a number.
POL-0013 already rejects NaN as a value with meaning; this is where it most often
enters.

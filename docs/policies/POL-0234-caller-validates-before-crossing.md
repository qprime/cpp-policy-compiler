---
id: POL-0234
kind: standard
trigger: "validate around an FFI call"
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
---

# The calling side validates before crossing; the callee asserts and trusts

Whoever holds the untrusted input checks it before the call. The callee may `assert`
cheaply for a contract it cannot state in the signature, and does not re-validate
defensively.

```cpp
extern "C" int plan_pocket_c(const double* xy, std::size_t count, double step_over_mm) {
    assert(xy != nullptr);
    assert(step_over_mm > 0.0);           // cheap, and states the contract
    ...
}
```

```python
def plan_pocket(points: list[Vec2], step_over_mm: float) -> Paths:
    if step_over_mm <= 0.0:               # the caller owns the check
        raise ValueError(f"plan_pocket: step_over_mm must be > 0, got {step_over_mm}")
    return _proj.plan_pocket(points, step_over_mm)
```

Validating on both sides means two implementations of one rule, and the day they
disagree the boundary rejects input the caller believes it cleared. Putting the check
where the untrusted value arrives keeps one answer to *what is valid*.

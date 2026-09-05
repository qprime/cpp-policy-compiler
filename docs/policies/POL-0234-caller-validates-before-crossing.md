---
id: POL-0234
kind: standard
trigger: "validate around an FFI call"
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
---

# An FFI entry point validates unless a single trusted wrapper established the contract

The side where untrusted input enters validates it before constructing trusted domain
values. A public C ABI entry point cannot assume every foreign caller used the
preferred wrapper, so it validates before dereferencing or converting. Only an
internal seam with one enforced, trusted caller may assert an already-established
contract instead of implementing the same validation twice.

```cpp
extern "C" int plan_pocket_c(const double* xy, std::size_t count, double step_over_mm) {
    if (xy == nullptr || step_over_mm <= 0.0) {
        return kInvalidArgument;
    }
    ...
}
```

```python
def plan_pocket(points: list[Vec2], step_over_mm: float) -> Paths:
    if step_over_mm <= 0.0:               # the caller owns the check
        raise ValueError(f"plan_pocket: step_over_mm must be > 0, got {step_over_mm}")
    return _proj.plan_pocket(points, step_over_mm)
```

Avoid two independent definitions of validity: put the rule in a shared schema or
one boundary constructor where possible. Validation is still required at every
independently callable trust boundary; an assertion compiled out of a C entry point
is not input validation.

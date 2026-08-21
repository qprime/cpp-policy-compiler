---
id: POL-0239
kind: standard
trigger: "choose the layer a wrapper type lives in"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Dependency Direction"
---

# A wrapper type lives at the layer that owns its precondition

Put the type where the check can actually be made — the layer that first sees the
data and can reject it — not the layer that wants to assume the guarantee.

```
parser/     ConvexPolygon::try_from  — validates here, where the points arrive
planner/    inset(const ConvexPolygon&, double)  — assumes, cannot construct
```

Defining it at the consuming layer inverts the dependency: the parser would have to
include the planner's header to hand over a validated value. It also puts the
validation where the raw input is no longer in view, so the error message loses the
context that would have identified which input was bad.

---
id: POL-0136
kind: standard
attribution:
  - source: standard-practice
    locator: "arithmetic conversions"
    upstream: ["CG ES.46"]
---

# A narrowing conversion is written out or it is a defect

The build's warning set makes an implicit narrowing conversion a diagnostic. Where
one is genuinely intended, write the `static_cast` and, if the value could exceed
the target, check first.

```cpp
const auto count = static_cast<int>(moves.size());   // deliberate, and bounded

int count = moves.size();                            // silent narrowing
float x = position_mm;                               // silent precision loss
```

An implicit narrowing conversion loses the high bits or the low digits without any
report, so the wrong value propagates and surfaces as bad output somewhere else.
The explicit cast is a claim the reviewer can check.

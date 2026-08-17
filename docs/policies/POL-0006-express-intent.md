---
id: POL-0006
kind: principle
precedence: 6
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #6"
    upstream: ["CG P.1", "CG P.3"]
---

# Express intent, not mechanism

The reader should see *what* the code means before *how* it works. Name the
operation; let the mechanism be an implementation detail of the name.

```cpp
const double margin_mm = clearance_mm(stock, part);

const double margin_mm =
    std::sqrt(std::pow(sx - px, 2.0) + std::pow(sy - py, 2.0)) - tool_r_mm;
```

Both lines compute the same number. Only the first tells the reader what the
number is for, which is the fact they came to the line to learn.

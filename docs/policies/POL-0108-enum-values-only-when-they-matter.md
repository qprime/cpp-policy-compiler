---
id: POL-0108
kind: guideline
attribution:
  - source: standard-practice
    locator: "enumeration representation"
    upstream: ["CG Enum.7", "CG Enum.8"]
---

# Specify an underlying type or explicit enumerator values only when something depends on them

Write the bare enumeration by default. Add an underlying type when the values
cross a boundary that fixes their width, and write explicit values when an external
protocol or file format assigns them.

```cpp
enum class PocketStrategy { Raster, Spiral, Trochoidal };

enum class GCodeMotion : std::uint8_t {    // the wire format fixes both
    Rapid = 0,
    Linear = 1,
    ArcCw = 2,
    ArcCcw = 3,
};
```

Specified values are a promise to external readers, so specifying them without an
external reader creates a constraint nobody needs and invites a caller to depend
on the numbers. Where the values are a contract, writing them makes that contract
visible at the definition.

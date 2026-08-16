---
id: POL-0104
kind: guideline
attribution:
  - source: standard-practice
    locator: "enumerations, underlying type and values"
    upstream: ["CG Enum.7", "CG Enum.8"]
---

# An underlying type or an explicit enumerator value appears only when it is the contract

```cpp
// Prefer. Nothing is claimed about representation.
enum class CompactMode { Full, Incremental };

// State both when the numbers cross a boundary and must not move.
enum class WireOpcode : std::uint8_t { Rapid = 0x01, Cut = 0x02, Dwell = 0x03 };
```

The contract cases are serialization, an FFI crossing (POL-0063), and a fixed
width a device or protocol requires. Absent one of those, the default
underlying type is correct and no enumerator carries a number.

A stated underlying type reads as a claim that the representation matters, and
a reader who finds one will preserve it through changes that did not need it.
Explicit values invite a gap or a duplicate, and a duplicate is the worse
failure: two enumerators that compare equal make a `switch` over them
unreachable in one arm, which defeats the exhaustiveness POL-0033 relies on
without producing a diagnostic.

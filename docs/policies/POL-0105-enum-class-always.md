---
id: POL-0105
kind: standard
trigger: "declare an enumeration"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "12. Enumerations"
    upstream: ["CG Enum.2", "CG Enum.3"]
---

# An enumeration is an `enum class`

Every set of related named alternatives is an `enum class`. An unscoped `enum`
appears only to match a C API.

```cpp
enum class PocketStrategy { Raster, Spiral, Trochoidal };

PocketStrategy strategy = PocketStrategy::Spiral;
int n = strategy;                        // ill-formed, which is the point
```

An unscoped enum converts to `int` implicitly, so its enumerators enter the
surrounding scope, collide with each other's names, and compare equal to unrelated
enumerations and to raw integers. `enum class` makes the enumeration a type,
which is what lets exhaustive dispatch over it mean anything.

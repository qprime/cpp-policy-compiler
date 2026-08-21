---
id: POL-0106
kind: guideline
trigger: "add an operation to an enumeration"
attribution:
  - source: standard-practice
    locator: "enumeration interfaces"
    upstream: ["CG Enum.4"]
---

# Operations on an enumeration are named functions beside it

Where callers need to name, parse, order, or iterate an enumeration, write free
functions in the same namespace rather than making them reach for the underlying
integer.

```cpp
enum class PocketStrategy { Raster, Spiral, Trochoidal };

std::string_view name_of(PocketStrategy strategy);
std::optional<PocketStrategy> parse_strategy(std::string_view text);
```

Without them every caller writes its own `switch` or, worse, casts to `int` and
indexes an array whose order has to stay in step by hand. One named function per
operation keeps the enumeration's meaning next to its definition.

Do not define arithmetic operators on an enumeration that is a set of
alternatives; those belong only on a genuine flag set.

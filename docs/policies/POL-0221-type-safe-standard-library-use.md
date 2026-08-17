---
id: POL-0221
kind: guideline
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "11. Strings and formatting"
    upstream: ["CG SL.4"]
---

# Use the standard library through its typed interfaces

Prefer the range algorithms to iterator pairs you assemble by hand, `at()` or an
iterator to a raw index where the bound is not obvious, and `std::format` or a
stream helper to `printf`.

```cpp
std::ranges::sort(moves, by_x);
const std::string line = std::format("F{:.1f}", feed_mm_per_min);

std::sort(moves.begin(), other.end(), by_x);          // mismatched ranges: UB
std::printf("F%.1f\n", feed_mm_per_min);              // no type checking
```

Mismatched iterators, out-of-range indices, and `printf` format mismatches are all
undefined behaviour the compiler cannot see. The range and format interfaces put the
same operations behind signatures that check.

---
id: POL-0010
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #7"
    upstream: ["CG ES.45"]
  - source: cpp-convention/conventions.md
    locator: "Trap: magic number"
enforcement:
  clang_tidy: ["readability-magic-numbers"]
---

# No magic constants

An inline literal that carries meaning gets a name. `constexpr` at file scope
for a value one translation unit owns; a shared constants header for a value
several modules must agree on.

```cpp
constexpr double kMinSpacingMm = 10.0;
if (spacing_mm < kMinSpacingMm) { ... }
```

The test is whether the number would ever be changed on its own. If it would, it
has a name. Trivially obvious literals do not: `0`, `1`, `0.5` for a midpoint,
array indices, and identity values in arithmetic.

Unnamed literals in limit checks, timing, and dimensional arithmetic drift and
diverge. The same threshold gets written at three sites, one is updated, and the
disagreement is invisible because nothing connects the three. The name is also
what states the unit and the intent, which the literal cannot.

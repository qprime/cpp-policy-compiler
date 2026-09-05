---
id: POL-0007
kind: principle
precedence: 7
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #7"
---

# Determinism is the default

Within the product's stated platform and reproducibility contract, the same
input produces the same observable output on every run. Do not leak undefined
behavior, unordered-container iteration, uninitialized reads, locale, or
uncontrolled floating-point variation into serialized or golden output.

```cpp
std::map<std::string, Layer> layers;             // ordered: safe to emit in order
std::unordered_map<std::string, Layer> layers;   // iteration order is not a contract
```

Nondeterminism turns reproducible defects into intermittent ones and makes
golden tests noisy. When output must compare across different implementations
or platforms, define normalization or tolerances instead of promising byte
identity the underlying operations do not provide.

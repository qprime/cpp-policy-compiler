---
id: POL-0007
kind: principle
precedence: 7
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #7"
---

# Determinism is the default

Same input, same output, on every platform and every run. No undefined
behaviour, no unordered-container iteration order in output, no uninitialized
reads, no platform-dependent floating point in golden output.

```cpp
std::map<std::string, Layer> layers;             // ordered: safe to emit in order
std::unordered_map<std::string, Layer> layers;   // iteration order is not a contract
```

Nondeterminism turns a reproducible defect into an intermittent one, and an
intermittent defect costs an order of magnitude more to find. It also destroys
golden testing, which is the only cheap check on structured output.

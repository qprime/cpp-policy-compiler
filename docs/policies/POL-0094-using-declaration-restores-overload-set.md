---
id: POL-0094
kind: standard
trigger: "overload an inherited name in a derived class"
attribution:
  - source: standard-practice
    locator: "name hiding"
    upstream: ["CG C.138"]
---

# A derived class that overloads an inherited name re-exposes the base overloads with `using`

Declaring any function with the same name in a derived class hides every base
overload of that name. Bring them back explicitly.

```cpp
class GrblPost final : public PostProcessor {
 public:
    using PostProcessor::emit;                  // keeps the base overloads visible
    std::string emit(const Rapid& rapid) const;
};
```

Without the `using`, a call that previously resolved to a base overload either
picks the derived one through a conversion or fails to compile — and which of the
two happens depends on the argument types at each call site.

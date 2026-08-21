---
id: POL-0092
kind: standard
trigger: "declare a virtual function or an override"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: is inheritance right"
    upstream: ["CG C.128"]
---

# A virtual function specifies exactly one of `virtual`, `override`, or `final`

`virtual` on the base declaration, `override` on an overrider, `final` on an
overrider nobody may replace. Never two of them on one declaration.

```cpp
class PostProcessor {
 public:
    virtual std::string emit(const Move& move) const = 0;
};

class GrblPost final : public PostProcessor {
 public:
    std::string emit(const Move& move) const override;
};
```

`override` is what turns a signature mismatch — a missing `const`, a widened
parameter — from a silently non-overriding new function into a compile error.
Repeating `virtual` alongside it says nothing and hides which declaration
introduced the function.

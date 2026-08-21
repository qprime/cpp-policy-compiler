---
id: POL-0210
kind: guideline
trigger: "templatize a hierarchy, or store derived objects by value"
attribution:
  - source: standard-practice
    locator: "templates and inheritance"
    upstream: ["CG T.80", "CG T.81", "CG T.82", "CG T.83"]
---

# Do not templatize a hierarchy, and do not put derived objects in an array

Keep the interface non-template and templatize behind it, or drop the hierarchy and
use a variant. Never declare a member function template `virtual`. Where virtual
dispatch is unwanted, linearize: give each level a concrete type and compose.

```cpp
class PostProcessor {                              // non-template interface
 public:
    virtual ~PostProcessor() = default;
    virtual std::string emit(const Move& move) const = 0;
};

template <class Dialect>                           // template implementation
class DialectPost final : public PostProcessor { ... };
```

A templatized hierarchy multiplies into an unrelated hierarchy per instantiation, so
no base type covers them all and the polymorphism is gone. A member function
template cannot be virtual because the set of instantiations is unbounded and a
v-table is not. Arrays of derived objects accessed through a base pointer step by
the wrong size.

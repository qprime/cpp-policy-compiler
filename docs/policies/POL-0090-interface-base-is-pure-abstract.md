---
id: POL-0090
kind: standard
trigger: "write a base class that exists to be an interface"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: is inheritance right"
    upstream: ["CG C.3", "CG C.121", "CG C.122"]
---

# A base used as an interface is pure abstract

Every member function is pure virtual, there are no data members, and the
destructor is public and virtual. Implementations live in derived classes that
share no state with each other.

```cpp
class PostProcessor {
 public:
    virtual ~PostProcessor() = default;
    virtual std::string emit(const Move& move) const = 0;
    virtual std::string preamble() const = 0;
};
```

A non-pure member in the base is shared implementation, and it means changing that
member recompiles and re-tests every implementation. Pure abstract is what buys
the complete separation the interface was introduced for: consumers depend on the
header, not on the code behind it.

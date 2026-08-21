---
id: POL-0025
kind: standard
trigger: "put data on a base class used as an interface"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: is inheritance right"
    upstream: ["CG I.25"]
---

# An interface base class carries no data

When an open set of behaviours is injected by a caller, the base is pure virtual
with no members, and derived classes hold their own state.

```cpp
class PostProcessor {
 public:
    virtual ~PostProcessor() = default;
    virtual std::string emit(const Move& move) const = 0;
};

class GrblPost final : public PostProcessor {
 public:
    explicit GrblPost(GrblDialect dialect);
    std::string emit(const Move& move) const override;

 private:
    GrblDialect dialect_;
};
```

Data in the base makes every derived class pay for it and couples them through
it, which turns an interface into shared implementation and takes the freedom
that made it an interface.

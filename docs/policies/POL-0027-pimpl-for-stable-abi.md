---
id: POL-0027
kind: guideline
attribution:
  - source: standard-practice
    locator: "ABI stability"
    upstream: ["CG I.27"]
---

# Hide implementation behind a pointer only when the ABI must not move

Reach for Pimpl when a header ships to consumers who will not recompile.
Otherwise pay nothing: a private member is already private.

```cpp
class Planner {
 public:
    explicit Planner(const MachineConfig& config);
    ~Planner();
    Paths plan(const Job& job) const;

 private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};
```

Pimpl buys ABI stability and recompile isolation, and costs an allocation, an
indirection on every access, and out-of-line special members. Inside one build
tree that is a fee with no purchase.

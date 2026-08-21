---
id: POL-0189
kind: guideline
trigger: "write cleanup that must run on every path"
attribution:
  - source: standard-practice
    locator: "scope guards"
    upstream: ["CG E.19"]
---

# Where no resource handle fits, use a scope guard

Prefer a real RAII type. Where the cleanup is one-off — restoring a flag, rolling
back a partial edit — a small guard object running a callable in its destructor is
the alternative, never a `try`/`catch`.

```cpp
template <class F>
class FinalAction {
 public:
    explicit FinalAction(F action) : action_(std::move(action)) {}
    ~FinalAction() { action_(); }
    FinalAction(const FinalAction&) = delete;
    FinalAction& operator=(const FinalAction&) = delete;

 private:
    F action_;
};

const FinalAction restore([&] { machine.set_units(previous_units); });
```

The guard runs on every exit — return, break, throw — where a `catch` block runs
only on the throw and has to be paired with duplicate cleanup on the normal path.

A codebase reaching for guards repeatedly has a resource type it has not written
yet.

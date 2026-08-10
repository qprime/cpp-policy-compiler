---
id: POL-0027
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: wrapper type for preconditions"
    upstream: ["CG I.5"]
  - source: cpp-convention/conventions.md
    locator: "Divergences: CG I.6, I.8"
  - source: cpp-convention/mechanisms.md
    locator: "§7 Invariants and preconditions"
---

# Wrapper type for preconditions

A function with a *structural* precondition — sorted, non-empty, acyclic,
normalized, deduplicated — takes a type that proves it. The check runs once, at
the boundary, instead of inside every algorithm that wants to assume it.

```cpp
class SortedKeys {
 public:
    static std::optional<SortedKeys> try_from(std::vector<Key> keys);
    const std::vector<Key>& keys() const { return keys_; }

 private:
    explicit SortedKeys(std::vector<Key> keys);
    std::vector<Key> keys_;
};

std::optional<Key> lower_bound(const SortedKeys& keys, const Key& target);
```

`lower_bound`'s signature *proves* its precondition. An unsorted vector cannot
reach it without passing through `try_from`, so the function neither re-checks
nor trusts a comment.

Two bounds on the pattern:

- **Scalar preconditions get no wrapper.** A positive count belongs on the type
  that owns the count field (POL-0022). Reserve wrappers for structure.
- **Repeated `assert`s are a missing wrapper.** When a function asserts the
  same precondition its callers also assert, the precondition wants to be a
  type.

This is how "state preconditions" is satisfied without taking a library
dependency for two macros: the precondition is not stated, it is made
unrepresentable. Where structure does not admit a wrapper, the precondition is
`assert`ed and documented instead.

A stated precondition is checked by whoever remembers it, which is everyone at
first and nobody after the third caller. A precondition in the parameter type
is checked by the compiler at every call, including the calls written later by
someone who never read the function. That converts an open-ended obligation on
callers into one conversion site whose failure is visible.

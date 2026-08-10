---
id: POL-0029
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: free function by default"
    upstream: ["CG C.4", "CG C.5"]
---

# Free function by default

A function is a member only if it needs direct access to the representation.
Everything else is a free function in the same namespace.

```cpp
class SortedKeys { /* only what needs the representation */ };

// same namespace, not members — these need only the public interface
std::optional<Key> lower_bound(const SortedKeys& keys, const Key& target);
std::size_t count_in_range(const SortedKeys& keys, const Key& lo, const Key& hi);
SortedKeys merge(const SortedKeys& a, const SortedKeys& b);
```

The test is mechanical: write the function against the public interface first,
and make it a member only when that fails.

A type's interface should be as small as its invariant requires, because every
member is code that could break the invariant and therefore code that has to be
read before the type can be trusted. A free function cannot corrupt what it
cannot reach, so a defect in one is a defect in one place. The arrangement also
lets operations be added without touching the type, which means the set of
things that can be done with a value grows without the set of things that must
be audited growing with it.

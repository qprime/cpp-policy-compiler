---
id: POL-0086
kind: standard
attribution:
  - source: standard-practice
    locator: "hashing"
    upstream: ["CG C.89"]
---

# A `std::hash` specialization is `noexcept` and agrees with `operator==`

Combine the same members equality compares, and declare the call operator
`noexcept`.

```cpp
template <>
struct std::hash<ToolId> {
    std::size_t operator()(const ToolId& id) const noexcept {
        return std::hash<int>{}(id.slot);
    }
};
```

Unordered containers call the hash while rehashing, where a throw leaves the
container's buckets half-rebuilt. A hash that disagrees with equality puts equal
keys in different buckets, so lookups miss entries the container holds.

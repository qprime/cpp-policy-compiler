---
id: POL-0146
kind: standard
attribution:
  - source: standard-practice
    locator: "comparison and hash"
    upstream: ["CG C.86", "CG C.87", "CG C.89"]
---

# `==` is symmetric and `noexcept`, and a `hash` agrees with it

```cpp
class ToolId {
 public:
    friend bool operator==(ToolId, ToolId) noexcept = default;
    friend auto operator<=>(ToolId, ToolId) noexcept = default;
 private:
    std::uint32_t value_{0};
};

template <>
struct std::hash<ToolId> {
    std::size_t operator()(ToolId id) const noexcept { return std::hash<std::uint32_t>{}(id.value()); }
};
```

`==` takes both operands the same way, so it is a free function rather than a
member (POL-0123). On C++20 prefer `= default` with `operator<=>`, which derives
the whole set from the members and cannot disagree with itself.

A `std::hash` specialization is `noexcept` and is consistent with `==`: two
objects that compare equal hash equal. An unordered container silently misbehaves
otherwise, storing duplicates that no lookup finds.

Never define `==` on a polymorphic base. It compares the base subobject, so two
objects of different derived types compare equal on their shared half — the same
slicing defect POL-0121 names, arriving through a comparison instead of a copy.
Comparison belongs on value types.

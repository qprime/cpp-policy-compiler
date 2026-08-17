---
id: STD-0020
group: layout-of-the-line
enforced_by: review
attribution:
  - source: standard-practice
    locator: "class layout"
    upstream: ["CG NL.16"]
---

# A class declares public, then protected, then private; data last within each

Within an access section: nested types and aliases, then constructors and the
destructor, then member functions, then data.

```cpp
class Toolpath {
 public:
    using value_type = Move;

    explicit Toolpath(std::vector<Move> moves);

    double length_mm() const;
    std::size_t size() const;

 private:
    std::vector<Move> moves_;
    double length_mm_;
};
```

A reader opening a class wants its interface, so the interface comes first and the
representation comes last.

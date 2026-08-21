---
id: POL-0127
kind: standard
trigger: "declare a member function, or a parameter you only read"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "6. Immutability"
    upstream: ["CG Con.2", "CG Con.3"]
---

# A member function that does not mutate is `const`, and so is every parameter you only read

```cpp
class Tool {
 public:
    double radius_mm() const { return 0.5 * diameter_mm_; }
};

double area_mm2(const Polygon& poly);
void offset_in_place(Polygon& poly, double delta_mm);   // non-const: it writes
```

Without `const` on the member function it cannot be called on a `const Tool`, so
one missing qualifier forces callers to hold non-`const` handles all the way up.
On a parameter, `const&` is what tells the caller their object comes back
unchanged — the alternative is reading the body to find out.

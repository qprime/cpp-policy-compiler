---
id: POL-0127
kind: standard
trigger: "declare a non-mutating member function or a borrowed parameter you only read"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "6. Immutability"
    upstream: ["CG Con.2", "CG Con.3"]
---

# A non-mutating member function is `const`; a borrowed input is `const&`

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
On a borrowed parameter, `const&` prevents mutation through that interface. A
by-value parameter is already the callee's copy and need not be top-level `const`,
especially when the implementation may move from it.

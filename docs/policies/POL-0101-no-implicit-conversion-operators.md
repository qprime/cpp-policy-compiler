---
id: POL-0101
kind: standard
attribution:
  - source: standard-practice
    locator: "conversion operators"
    upstream: ["CG C.164", "CG C.166"]
---

# No implicit conversion operators, and no overloaded unary `&`

Where a conversion is genuinely wanted, make it `explicit` or give it a name.
Leave `operator&` alone outside a smart-pointer or reference-wrapper system.

```cpp
class Feed {
 public:
    explicit operator double() const { return mm_per_min_; }   // explicit, or:
    double mm_per_min() const { return mm_per_min_; }          // named — better
};
```

An implicit conversion operator makes the type participate in every overload
resolution and arithmetic promotion in the program, which is how a strong type
quietly becomes the primitive it was wrapping. Overloading unary `&` breaks
generic code, which reasonably assumes `&x` yields a pointer to `x`.

---
id: POL-0123
kind: standard
attribution:
  - source: standard-practice
    locator: "operator overloading, placement and form"
    upstream: ["CG C.161", "CG C.164", "CG C.165", "CG C.168"]
---

# A symmetric operator is a free function in its type's namespace, and conversions are `explicit`

```cpp
namespace proj::geom {

class Millis {
 public:
    explicit constexpr Millis(double count) : count_{count} {}
    explicit constexpr operator double() const { return count_; }
    constexpr double count() const { return count_; }
 private:
    double count_;
};

constexpr bool operator==(Millis a, Millis b) { return a.count() == b.count(); }

}
```

A symmetric operator is a free function so both operands convert alike; a member
`operator==` converts only its right-hand side, which makes `a == b` and `b == a`
behave differently. It lives in the same namespace as its type, so
argument-dependent lookup finds it without a `using` declaration.

A conversion operator is `explicit`, and a customization point is opted into
with a `using` declaration at the call site rather than by defining a function
in someone else's namespace.

An implicit conversion operator makes a type participate in overload resolutions
nobody wrote it for. The type then converts silently in a comparison, an
arithmetic expression, or an overload it was never meant to match, which is the
same defect POL-0038 avoids by making a distinct type a named escape rather than
a transparent one.

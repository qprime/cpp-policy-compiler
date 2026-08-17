---
id: POL-0213
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "9. Generic code"
    upstream: ["CG T.120", "CG T.121", "CG T.122", "CG T.124", "CG T.125"]
---

# Compute types with aliases and values with `constexpr` functions; nothing deeper

Reach for `std::type_identity_t`, `std::conditional_t`, and the rest of
`<type_traits>` before writing a trait. Compute values in `constexpr` functions, not
in template recursion. Where the standard library has the facility, use it; where it
does not and the need is real, use an established library rather than writing your
own.

```cpp
template <class T>
using ElementOf = std::conditional_t<std::is_const_v<T>, const Element, Element>;

constexpr int pass_count(double depth_mm, double step_mm) {
    return static_cast<int>(std::ceil(depth_mm / step_mm));
}
```

Template metaprogramming is a functional language with no debugger, no stack trace,
and error messages that quote instantiation chains. Concepts, `if constexpr`, and
`constexpr` functions cover almost everything it used to be needed for, in a form
that reads like the rest of the language.

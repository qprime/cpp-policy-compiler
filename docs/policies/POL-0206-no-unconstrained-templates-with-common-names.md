---
id: POL-0206
kind: standard
trigger: "give a widely visible template an unconstrained parameter"
attribution:
  - source: standard-practice
    locator: "overload set pollution"
    upstream: ["CG T.47"]
---

# A widely visible template has a constraint, or a name nobody else would choose

Constrain anything at namespace scope whose name is common — `size`, `begin`,
`format`, `to_string`, an operator. Keep unconstrained helpers in a `detail`
namespace or an anonymous namespace in the source file.

```cpp
template <Offsettable Shape>
double size(const Shape& shape);          // constrained: only matches shapes

template <class T>
double size(const T& value);              // matches everything, everywhere
```

An unconstrained template with a common name enters the overload set of every call
found by argument-dependent lookup, including calls in code that has never heard of
it. That either hijacks the call or makes it ambiguous, and the error appears in a
file whose author cannot see the cause.

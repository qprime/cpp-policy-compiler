---
id: POL-0209
kind: standard
trigger: "specialize or overload a template"
attribution:
  - source: standard-practice
    locator: "specialization"
    upstream: ["CG T.64", "CG T.65", "CG T.67", "CG T.144"]
---

# Specialize class templates; overload function templates

Write a partial or full specialization of a class template to provide an alternative
implementation. For functions, add an overload or constrain a second template. Never
write an explicit specialization of a function template.

```cpp
template <class T> struct Formatter { std::string operator()(const T&) const; };
template <> struct Formatter<Vec2> { std::string operator()(const Vec2&) const; };

std::string format(const Move& move);              // overload
template <Formattable T> std::string format(const T& value);
```

Explicit function template specialization does not participate in overload
resolution the way readers expect: an overload declared later can win over a
specialization of an earlier template, so which one runs depends on declaration
order. Class template specialization has no such rule, and where dispatch must
happen on a property rather than a type, a tag parameter selects an overload
predictably.

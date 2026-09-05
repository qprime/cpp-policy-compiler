---
id: POL-0201
kind: standard
trigger: "write a constraint and its negation as two overloads"
attribution:
  - source: standard-practice
    locator: "constraint design"
    upstream: ["CG T.25"]
---

# Do not write a constraint and its negation as two overloads

Write one function with `if constexpr`, or give the two cases distinct positive
concepts.

```cpp
template <class T>
void emit(const T& value) {
    if constexpr (Formattable<T>) { emit_formatted(value); }
    else { emit_raw(value); }
}
```

```cpp
template <Formattable T>  void emit(const T& value);
template <class T> requires (!Formattable<T>) void emit(const T& value);   // no
```

The negation is a real logical complement, but it scales poorly: adding a more
specific overload changes the ordering problem, and diagnostics describe the
negative implementation category rather than a positive semantic requirement.
`if constexpr` keeps a true binary implementation choice together; independently
meaningful cases get positive concepts.

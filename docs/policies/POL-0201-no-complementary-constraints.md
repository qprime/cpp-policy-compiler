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

The negated overload is not the complement the author intends: adding a third
overload, or a type that satisfies neither predicate, changes which one is selected
in ways that are hard to predict. `if constexpr` puts both branches in one function
where the reader can see the whole decision.

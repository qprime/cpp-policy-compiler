---
id: POL-0102
kind: guideline
trigger: "call a function a caller may substitute"
attribution:
  - source: standard-practice
    locator: "customization points"
    upstream: ["CG C.165", "CG T.69"]
---

# A customization point is an unqualified call, and every other call is qualified

When a template must let callers substitute an operation, bring the default into
scope with `using` and call the name unqualified. Everywhere else, qualify the
call so lookup cannot be redirected.

```cpp
template <class T>
void normalize_all(std::vector<T>& values) {
    using proj::normalize;                  // the customization point
    for (T& value : values) { normalize(value); }
}
```

An unqualified call inside a template is found by argument-dependent lookup at
instantiation, so any namespace the arguments live in can supply the function.
That is exactly right when it is intended and an unpredictable hijack when it is
not.

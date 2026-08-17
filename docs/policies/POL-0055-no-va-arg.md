---
id: POL-0055
kind: standard
attribution:
  - source: standard-practice
    locator: "variadic arguments"
    upstream: ["CG F.55", "CG T.100"]
---

# No `va_arg`; a variable argument list is a variadic template

Where a function genuinely takes a variable number of arguments of varying
types, write a variadic template. Where the arguments are all the same type, take
a sequence view.

```cpp
template <class... Args>
void log_warning(std::string_view pattern, const Args&... args);

void log_warning(const char* pattern, ...);        // no types, no checking
```

`va_arg` erases every type, so a mismatch between the format and the arguments is
undefined behaviour the compiler cannot see. The template keeps the types and
turns the same mistake into a compile error.

---
id: POL-0096
kind: standard
attribution:
  - source: standard-practice
    locator: "initialization"
    upstream: ["CG ES.20", "CG ES.23"]
---

# Every variable is initialized at its declaration, with braces

```cpp
// Never. Indeterminate between the two lines, and reading it there is UB.
int retries;
retries = policy.retries;

// Right. Braces also reject the narrowing conversion.
const int retries{policy.retries};
const double ratio{0.75};
```

Braces are the default because they refuse narrowing: `int n{3.7}` fails to
build where `int n(3.7)` silently truncates.

Use parentheses where braces would select a `std::initializer_list`
constructor you did not want. `std::vector<int> v{10}` holds one element and
`std::vector<int> v(10)` holds ten, which is the one case where the brace
default is a trap rather than a guard.

A variable declared without a value has a window in which it holds whatever was
on the stack, and reading it is undefined behaviour rather than a wrong value.
No warning catches it reliably, because the compiler cannot see across the
branch that was supposed to assign it. Initializing at the declaration removes
the window rather than narrowing it, and it forces the value's origin to be
visible on the line that introduces the name (POL-0026).

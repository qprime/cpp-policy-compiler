---
id: POL-0132
kind: standard
attribution:
  - source: standard-practice
    locator: "evaluation order"
    upstream: ["CG ES.43", "CG ES.44"]
---

# No expression depends on the order its subexpressions run in

Read or modify a given object once per expression, and never let one argument's
value depend on another argument's side effect.

```cpp
const int i = next_index();
values[i] = compute(i);

values[next_index()] = compute(next_index());     // which call ran first?
emit(consume(buffer), buffer.size());             // unspecified
```

The order of evaluation of function arguments is unspecified, and modifying an
object twice in one expression without an intervening sequence point is undefined.
Both compile silently and both can change behaviour between compilers,
optimization levels, or a refactor that reorders arguments.

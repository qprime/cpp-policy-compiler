---
id: POL-0197
kind: standard
trigger: "write an expression template, or a DSL out of operator overloads"
attribution:
  - source: standard-practice
    locator: "expression templates"
    upstream: ["CG T.4"]
---

# No expression templates and no embedded DSL built out of operator overloads

Where a computation needs to be represented before it is evaluated, build an
explicit data structure — a variant tree, a vector of operations — and write a
function that walks it.

```cpp
using Expr = std::variant<Constant, Add, Multiply>;   // explicit, debuggable
double evaluate(const Expr& expr, const Bindings& bindings);
```

An expression template makes every intermediate an unnamed type, so a diagnostic
names a template instantiation instead of the user's expression and a debugger shows
nothing recognizable. The explicit tree costs one allocation and is readable by
anyone.

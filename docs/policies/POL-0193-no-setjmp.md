---
id: POL-0193
kind: standard
attribution:
  - source: standard-practice
    locator: "non-local jumps"
    upstream: ["CG SL.C.1"]
---

# No `setjmp` or `longjmp`

Use exceptions, or a result type in a module that has none.

```cpp
if (auto result = parse_job(text); !result) { return result.error(); }
```

`longjmp` unwinds without running destructors, so every RAII object between the jump
and the landing site leaks its resource. In C++ that is undefined behaviour whenever
any such object exists, which in practice is always.

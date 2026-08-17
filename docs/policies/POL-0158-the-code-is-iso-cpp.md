---
id: POL-0158
kind: standard
attribution:
  - source: standard-practice
    locator: "portability"
    upstream: ["CG P.2", "CG CPL.1"]
---

# The code is ISO standard C++, not a dialect of it

```cpp
// Never. Compiler extensions, silently accepted, silently non-portable.
typeof(x) y = x;
int values[n];                      // variable-length array
__attribute__((packed)) struct Wire { ... };

// Right.
decltype(x) y = x;
std::vector<int> values(n);
```

`-Wpedantic` under POL-0089 is what reports an extension, and it is on for
exactly this reason. Where a platform genuinely requires one — an alignment
attribute, an intrinsic — it is isolated behind an interface that the rest of
the code sees as ordinary C++, which is the escape hatch POL-0064 describes for
the binding layer.

C constructs are not written where C++ has an equivalent, and this covers the
whole family: C casts (POL-0094), C arrays (POL-0155), macros (POL-0157),
`va_arg` and `setjmp` (POL-0154), `malloc` (POL-0127).

An extension compiles on the compiler it was written against and fails on the
next one, usually years later during a migration nobody budgeted for. It also
defeats POL-0093: the declared standard stops describing what the code needs,
so the build configuration no longer states the truth about the project.

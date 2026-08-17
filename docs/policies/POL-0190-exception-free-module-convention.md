---
id: POL-0190
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "5. Failure"
    upstream: ["CG E.25", "CG E.26", "CG E.27"]
---

# A module compiled without exceptions states one error convention in its top-level header

Pick one — a result type on every fallible function, or fail-fast on violation —
and say which in the header. Keep RAII: the destructors still run, so resource
handling does not change.

```cpp
// scan/scan.hpp
// Built with -fno-exceptions. Every fallible function returns Result<T, ScanError>;
// an invariant violation calls std::abort through PROJ_FATAL.
```

Two conventions in one module means every caller checks both ways and one of them
gets forgotten. Systematically is the operative word: the value of an error-code
discipline is entirely in its uniformity, since nothing in the language enforces
that a code is read.

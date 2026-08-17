---
id: POL-0133
kind: anti-pattern
replacement: [POL-0098]
attribution:
  - source: standard-practice
    locator: "pointer arithmetic"
    upstream: ["CG Bounds.1", "CG Bounds.2", "CG ES.62", "CG ES.65", "CG Lifetime.1"]
---

# Never compute with a pointer

```cpp
// Never. No bound, and the arithmetic is only valid within one array.
double sum(const double* first, const double* last) {
    double total = 0.0;
    for (const double* p = first; p != last; ++p) { total += *p; }
    return total;
}

// Right.
double sum(std::span<const double> values) {
    return std::accumulate(values.begin(), values.end(), 0.0);
}
```

Take a `std::span` and a standard algorithm (POL-0046, POL-0098). Index with a
constant expression or through an interface that carries the bound; a raw
subscript computed at runtime is the same defect in different syntax.

Comparing or subtracting pointers into different arrays is undefined even where
both are valid, so the comparison a bounds check depends on may not mean what it
says.

Pointer arithmetic is the one construction where the language provides neither a
check nor a diagnostic. Reading one element past the end is undefined behaviour
that usually succeeds, because the memory is mapped and holds something
plausible, so the failure surfaces as a wrong answer far from the loop
(POL-0002). A `std::span` carries the length the pointer form left in a comment,
and every standard algorithm over it derives its bound from the object rather
than from the caller remembering.

---
id: POL-0101
kind: standard
attribution:
  - source: standard-practice
    locator: "arithmetic"
    upstream: ["CG ES.102", "CG ES.103", "CG ES.106"]
---

# Arithmetic is done in a signed type

```cpp
// Never. If margin exceeds width, the result is enormous, not negative.
const std::size_t slack = sheet.width_mm() - margin_mm;

// Right.
const auto slack = static_cast<std::int64_t>(sheet.width_mm()) - margin_mm;
```

`std::size_t` holds a size or an index that came from the standard library, and
converts to a signed type once, at the point the arithmetic starts. Letting an
unsigned type spread outward from `size()` is how the wrap reaches code that
does no container work.

Never rely on signed overflow either. It is undefined, so the optimizer assumes
it cannot happen and deletes the check written to detect it.

Unsigned arithmetic wraps at zero, so a subtraction that should go negative
produces a very large positive number instead. The comparison written to catch
it then succeeds, which means the guard and the defect cancel out and the wrong
value flows on. Nothing reports it: the wrap is defined behaviour, so no
sanitizer fires and no warning applies. A signed type makes the same
subtraction produce a negative number, which every subsequent check treats as
the error it is (POL-0002).

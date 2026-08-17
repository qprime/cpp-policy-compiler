---
id: POL-0155
kind: anti-pattern
replacement: [POL-0161, POL-0133]
attribution:
  - source: standard-practice
    locator: "C arrays"
    upstream: ["CG Bounds.3", "CG ES.27"]
---

# Never declare a C array

```cpp
// Never. Decays to a pointer at the first call; the size is gone.
double offsets[16];
process(offsets);

// Right. Carries its size, and knows it at compile time.
std::array<double, 16> offsets{};
process(offsets);
```

A fixed size known at compile time is `std::array`; a size known at run time is
`std::vector`; a view over either is `std::span` (POL-0046).

At an `extern "C"` boundary the foreign signature dictates a pointer, and the
conversion to `std::span` happens on entry — the same escape POL-0046 grants and
no wider.

Array-to-pointer decay is silent and immediate: passing an array to anything
loses the length, so every function downstream depends on a bound the caller
knows and the type does not carry. That is the pointer-and-length pair with the
length omitted, and it is the substrate for the pointer arithmetic POL-0133
forbids.

`std::array` costs nothing at run time, is the same layout, and keeps `size()`
attached to the object rather than to the reader's memory.

---
id: POL-0041
kind: pattern
trigger: "pass a sequence of elements"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "4. Sequences"
    upstream: ["CG F.24", "CG R.14"]
---

# A sequence parameter carries its own bounds

Write the view type your standard provides: `std::span<const T>` to read and
`std::span<T>` to write on C++20, an iterator pair or `const std::vector<T>&`
earlier, `std::string_view` for strings from C++17.

```cpp
double path_length_mm(std::span<const Vec2> points);
void offset_in_place(std::span<Vec2> points, double delta_mm);
```

The bounds travel with the data, so the callee can iterate without trusting a
separately-passed count and the caller cannot pass a mismatched pair. Where the
standard has no view type the intent is unchanged: the parameter still carries
its extent.

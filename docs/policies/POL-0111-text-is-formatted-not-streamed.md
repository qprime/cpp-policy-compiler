---
id: POL-0111
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "§11 Strings and formatting"
---

# Text is formatted by a format call, not assembled on a stream

```cpp
// Never. Manipulators persist on the stream past the line that set them.
std::ostringstream out;
out << std::fixed << std::setprecision(2) << "width " << width_mm << "mm";

// Right, on C++20.
const auto text = std::format("width {:.2f}mm", width_mm);
```

Below C++20 the spelling is one contained helper holding an
`std::ostringstream`, or `snprintf` into a fixed buffer where a real-time loop
forbids allocation (POL-0012). On C++20 an `std::ostringstream` in new code is
a defect.

`printf`-family calls are not type-safe. They are permitted only where a
project has no `std::format` and a measured reason to avoid streams.

A stream carries formatting state, so `std::setprecision` set for one value
applies to every value written afterward, including from a different function
that shares the stream. The defect appears as a number formatted wrongly a long
way from the manipulator that caused it. A format string states the formatting
for each argument at the point of use and carries nothing between calls.

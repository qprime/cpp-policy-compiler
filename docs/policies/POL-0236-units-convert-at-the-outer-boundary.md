---
id: POL-0236
kind: standard
trigger: "convert units near the FFI seam"
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
---

# Unit conversion happens at the outer boundary, never at the FFI seam

Convert where the value enters the program — user input, file parsing — and let one
unit travel everywhere inside, including across the language boundary.

```cpp
// parser: the outer boundary, where inches become millimetres once
Tool parse_tool(const ToolRecord& record) {
    const double diameter_mm = record.units == Units::Inches
        ? record.diameter * kMmPerInch
        : record.diameter;
    return Tool(diameter_mm, record.rpm);
}
```

Converting at the seam means the two sides hold values in different units, so every
signature crossing the boundary needs its unit documented and every future call site
needs to know which side it is on. It also puts a conversion in the one place that
already has the most ways to go wrong.

---
id: POL-0099
kind: standard
attribution:
  - source: standard-practice
    locator: "iteration, range-for binding"
    upstream: ["CG ES.71"]
---

# A range-`for` binds `const auto&` to read and `auto&` to modify

```cpp
for (const auto& tool : tools) { total += tool.diameter_mm; }  // read
for (auto& tool : tools) { tool.wear += 1; }                   // modify
for (auto tool : tools) { tool.wear += 1; }                    // copies; the write is lost
```

A bare `auto` is written only where a copy is the point, and then the copy is
what the body is for.

`auto&&` is reserved for a generic context or a range whose yield is a proxy,
which is the same boundary POL-0050 draws around `auto` generally.

A bare `auto` copies every element, which is two defects at once. When the body
writes, the write lands on the copy and is discarded with no diagnostic, so the
loop runs and does nothing. When the body only reads, the copy is silent cost
proportional to the container. The binding is the only place the difference is
visible, so it has to state which of the three cases this loop is.

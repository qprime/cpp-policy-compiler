---
id: STD-0016
group: layout-of-the-line
enforced_by: review
attribution:
  - source: standard-practice
    locator: "const placement"
    upstream: ["CG NL.26"]
---

# `const` goes on the left of the type it qualifies

```cpp
const Tool& tool;
const double kMinMarginMm = 10.0;
const char* name;                    // pointer to const char
char* const name;                    // const pointer — const binds right, as it must

Tool const& tool;                    // no
double const kMinMarginMm = 10.0;    // no
```

Left-`const` is what nearly all C++ reads like, so it is what a reader parses
without stopping. The one place `const` appears on the right is a `const` pointer,
where the language leaves no choice.

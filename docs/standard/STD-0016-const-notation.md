---
id: STD-0016
group: layout-of-the-line
enforced_by: review
review_trigger: "a declaration places const inconsistently with the project notation"
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

Left-`const` is the repository's single consistent spelling for a const-qualified
base type. A top-level const pointer necessarily places its own `const` after the
`*`; this is grammar, not a competing base-type convention.

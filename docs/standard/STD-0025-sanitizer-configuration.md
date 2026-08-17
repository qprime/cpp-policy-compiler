---
id: STD-0025
group: toolchain
enforced_by: build
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
    upstream: ["CG CP.9"]
---

# UBSan and ASan run in at least one configuration; TSan once concurrency exists

```cmake
add_compile_options(-fsanitize=address,undefined -fno-omit-frame-pointer)
add_link_options(-fsanitize=address,undefined)
```

The test suite runs under the sanitized configuration in CI. A finding blocks
merge.

ASan and TSan are mutually exclusive, so TSan is a third configuration rather than
an addition to the second.

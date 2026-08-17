---
id: STD-0027
group: toolchain
enforced_by: build
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
---

# clang-format runs on every file, Google baseline, indent 4, column limit 100

```yaml
# .clang-format
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
PointerAlignment: Left
```

The values here are the ones [STD-0014](STD-0014-indentation-and-brace-style.md)
and [STD-0015](STD-0015-declarator-layout.md) state. Changing one means changing
both.

Formatting is decided once per project and not revisited. Details beyond this
baseline are the project's to set; the four keys above are not.

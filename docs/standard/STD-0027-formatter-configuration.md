---
id: STD-0027
group: toolchain
enforced_by: build
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
---

# clang-format runs on every project-owned C++ file, Google baseline, indent 4, column limit 100

```yaml
# .clang-format
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
PointerAlignment: Left
DerivePointerAlignment: false
AccessModifierOffset: -3
```

The values here are the ones [STD-0014](STD-0014-indentation-and-brace-style.md)
and [STD-0015](STD-0015-declarator-layout.md) state. Changing one means changing
both.

Formatting is decided once per project and not revisited. Details beyond this
baseline are the project's to set; the six keys above are not. Disabling derived
pointer alignment prevents existing source from overriding the selected spelling.
With four-space member indentation, the access modifier offset of -3 places
`public:` and `private:` one space inside the class, as STD-0014 requires.

Generated and vendored sources follow their owner's process and are excluded
rather than rewritten.

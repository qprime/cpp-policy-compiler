---
id: POL-0094
kind: standard
attribution:
  - source: standard-practice
    locator: "casts"
    upstream: ["CG ES.48", "CG ES.49", "CG Type.1"]
---

# A cast is named, and the named cast is nearly always `static_cast`

```cpp
// Never. Which conversion is this? The syntax does not say.
double ratio = (double)count / (double)total;
Widget* w = (Widget*)handle;

// Right.
const auto ratio = static_cast<double>(count) / static_cast<double>(total);
auto* w = static_cast<Widget*>(handle);
```

`const_cast`, `reinterpret_cast`, and `dynamic_cast` each defeat a guarantee
the reader is entitled to assume, so each carries a comment stating why.
`static_cast` needs none.

Before writing any cast, check whether the type upstream is wrong. A cast is an
assertion that the type system has it backwards, and most casts mark a
representation chosen badly rather than a conversion genuinely needed
(POL-0034).

A C-style cast selects from among `static_cast`, `const_cast`, and
`reinterpret_cast` by rules almost nobody has memorized. The same four
characters mean a checked numeric conversion on one line and a reinterpretation
of raw memory on the next, and nothing in the syntax distinguishes them. A
named cast says which one it is and can be searched for when the class of
conversion turns out to be the defect.

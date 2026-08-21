---
id: POL-0218
kind: standard
trigger: "add an include or a library dependency"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Dependency Direction"
    upstream: ["CG SF.9", "CG A.4"]
---

# Includes and library dependencies flow one way

Layers depend rightward and never leftward:

```
Input/CLI  →  Parser  →  IR/Model  →  Validation  →  Backend/Output
```

Where a lower layer needs a higher layer's type, introduce an adapter at the
boundary rather than pulling the higher layer's headers down. The check: delete the
higher-level module mentally — do the lower-level ones still compile?

```cpp
// ir/move.hpp — knows nothing about the parser or the backend
struct Move { Vec2 end_mm; double feed_mm_per_min; };
```

A cycle between two files means neither can be compiled, read, or tested without the
other, so the pair is really one module with a header in the middle. A cycle between
libraries means the same thing at a scale where nothing can be reused.

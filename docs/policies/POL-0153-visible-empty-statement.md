---
id: POL-0153
kind: guideline
attribution:
  - source: standard-practice
    locator: "empty statements"
    upstream: ["CG ES.85"]
---

# An intentionally empty statement is visible

Write `{}` on its own line, or a comment saying why nothing happens.

```cpp
while (advance(stream)) {
    // Skipping the header; nothing to emit.
}

while (advance(stream));                       // is the semicolon deliberate?
```

A bare semicolon at the end of a loop header is indistinguishable from a typo that
detached the intended body, and it is one of the few mistakes that compiles into a
different program silently.

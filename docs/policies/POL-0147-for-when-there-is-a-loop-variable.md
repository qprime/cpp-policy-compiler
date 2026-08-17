---
id: POL-0147
kind: guideline
attribution:
  - source: standard-practice
    locator: "loop selection"
    upstream: ["CG ES.72", "CG ES.73"]
---

# `for` when there is an obvious loop variable, `while` when there is not

```cpp
for (int pass = 0; pass < pass_count; ++pass) { ... }

while (!queue.empty()) { process(queue.pop()); }

int pass = 0;
while (pass < pass_count) { ... ++pass; }        // the three parts, scattered
```

A `for` header puts initialization, test, and advance in one place, so a reader
checks the loop's shape without scanning the body. When there is no such variable,
a `for` with empty slots is a `while` in an awkward spelling.

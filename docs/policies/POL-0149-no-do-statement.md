---
id: POL-0149
kind: guideline
trigger: "write a do-statement"
attribution:
  - source: standard-practice
    locator: "loop forms"
    upstream: ["CG ES.75"]
---

# Avoid `do`-statements

Restructure as a `while` with the condition at the top, or as a loop with an
explicit break.

```cpp
while (true) {
    const Move move = next_move(stream);
    if (is_end(move)) { break; }
    emit(move);
}

do {
    const Move move = next_move(stream);
    emit(move);
} while (!is_end(move));                       // condition read last, and out of scope
```

The condition sits at the bottom, so a reader learns the loop's exit only after
reading the body, and any variable the condition names has to be declared outside
the loop. The rewrite keeps the exit visible where the loop starts.

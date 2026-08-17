---
id: POL-0131
kind: guideline
attribution:
  - source: standard-practice
    locator: "pointer expressions"
    upstream: ["CG ES.42"]
---

# Pointer expressions stay simple: dereference, compare to null, nothing else

No arithmetic on pointers, no casting between pointer types, no chains of
indirection. Where iteration is needed, iterate the container.

```cpp
if (tool != nullptr) { use(*tool); }

const Move* p = &moves[0];
while (p != &moves[0] + moves.size()) { ... ++p; }     // no: iterate the container
```

Pointer arithmetic is only defined inside one array, so every expression of this
shape is one off-by-one away from undefined behaviour with no diagnostic. A
container's iterators and a range-`for` express the same walk and cannot leave the
object.

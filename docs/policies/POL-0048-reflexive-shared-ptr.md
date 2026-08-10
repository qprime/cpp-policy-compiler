---
id: POL-0048
kind: anti-pattern
replacement: [POL-0024]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: reflexive shared_ptr"
    upstream: ["CG R.21"]
---

# Never reach for `shared_ptr` because the ownership question is open

`std::shared_ptr` is for genuinely shared ownership: several independent owners
with no primary among them. Reaching for it because it is the form that always
compiles hides the question it was supposed to answer.

Work the ownership decision instead (POL-0024). Most values need no heap at all,
and most that do have exactly one owner.

```cpp
std::shared_ptr<Store> store;   // why is it shared? nothing here says
std::unique_ptr<Store> store;   // one owner, transferred by move
Store store;                    // most often this
```

What is bought is an atomic refcount on every copy and a lifetime that ends at a
moment no single piece of code decides. What is lost is the question: a
`shared_ptr` in a declaration reads as a design decision, so the next reader
assumes sharing was required and writes code that requires it. That is how a
placeholder becomes load-bearing, and by then the cost of asking again is the
cost of tracing every copy.

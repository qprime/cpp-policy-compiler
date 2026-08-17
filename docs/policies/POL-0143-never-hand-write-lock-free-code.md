---
id: POL-0143
kind: anti-pattern
replacement: [POL-0105]
attribution:
  - source: standard-practice
    locator: "concurrency, lock-free programming"
    upstream: ["CG CP.100", "CG CP.101", "CG CP.102"]
---

# Never hand-write a lock-free data structure

```cpp
// Never. A hand-rolled compare-and-swap stack: the ABA problem, the reclamation
// problem, and the memory-ordering problem, none of which a test will show.
void push(Node* n) {
    do { n->next = head_.load(std::memory_order_relaxed); }
    while (!head_.compare_exchange_weak(n->next, n));
}
```

Take a mutex (POL-0105). A single `std::atomic<T>` with the default sequentially
consistent ordering is not this anti-pattern — it is the shared-primitive row of
the mechanism table, and it is fine.

What is excluded is a data structure built out of compare-and-swap loops,
explicit `memory_order` relaxation, or any published algorithm reproduced from
memory.

Lock-free code fails in ways testing does not reach. The defects are
interleavings that occur under a load the test never applied, on a core count
the test machine did not have, or only after the optimizer reorders operations
the relaxed ordering permitted it to reorder. A run that passes is not evidence,
which puts this outside what POL-0001 can offer — neither the type system nor
the test suite constrains it.

The payoff is a constant factor on contention. The cost is a class of defect
that is undetectable in review, unreproducible in the field, and correct only if
the author's memory-ordering reasoning was right the first time.

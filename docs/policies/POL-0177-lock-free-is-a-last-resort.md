---
id: POL-0177
kind: standard
trigger: "write lock-free code"
attribution:
  - source: standard-practice
    locator: "lock-free programming"
    upstream: ["CG CP.100", "CG CP.101", "CG CP.102"]
---

# Lock-free code needs a measurement, a cited algorithm, and a reviewer

Use a mutex. Where a measurement shows the lock is the bottleneck, implement a
published algorithm, cite it in a comment, and have someone else check the memory
ordering.

```cpp
// Treiber stack, Michael & Scott 1996 §3. Release on push pairs with acquire on
// pop so the node's fields are visible to the popping thread.
void push(Node* node) {
    Node* head = head_.load(std::memory_order_relaxed);
    do { node->next = head; }
    while (!head_.compare_exchange_weak(head, node,
                                        std::memory_order_release,
                                        std::memory_order_relaxed));
}
```

Memory ordering bugs are invisible on x86 and appear on ARM, or appear only under a
compiler that reordered a store. That failure mode makes local reasoning and local
testing both unreliable, so the algorithm has to come from the literature rather
than from the author.

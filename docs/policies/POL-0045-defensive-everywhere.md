---
id: POL-0045
kind: anti-pattern
replacement: [POL-0022, POL-0041]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: defensive everywhere"
---

# Never check the same precondition at every call site

The same precondition checked in three functions is not thoroughness. It is an
invariant that was never established, paid for three times, and drifting the
moment one site's fallback differs from another's.

```cpp
// site A
const int attempts = policy.max_attempts > 0 ? policy.max_attempts : kDefaultAttempts;
// site B, written later, different fallback, silent divergence in behaviour
const int attempts = policy.max_attempts > 0 ? policy.max_attempts : 1;
```

Establish the invariant once, at construction (POL-0022), and validate at the
boundary rather than inside (POL-0041). Both defences then delete.

The second check has no information the first did not, and no ability to do
anything useful with a failure, so what it actually contributes is a second
opinion about what an invalid value means. Two opinions in one call chain produce
two behaviours for one input, and nothing connects them, so the disagreement is
invisible until the outputs are compared. It is also self-reinforcing: each new
consumer sees defensive checks upstream, reads them as the local convention, and
adds a third.

---
id: POL-0011
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #6"
  - source: cpp-convention/conventions.md
    locator: "Error message format"
---

# Errors carry the four-part message

Every constructed message states four things. This holds for exceptions, result
payloads, log lines, and structured warnings alike.

1. **What failed.** The class, function, or subsystem.
2. **What field.** The specific parameter or invariant.
3. **What constraint.** The rule that was broken.
4. **Actual value.** What was received.

```cpp
throw std::invalid_argument("RetryPolicy: max_attempts must be > 0, got 0");
```

A message missing any part forces whoever reads it back to the source to
reconstruct the rest, and the reader is often a process that has no source in
front of it. `"invalid argument"` identifies nothing. `"max_attempts is
invalid"` omits the constraint and the value, which are the two parts that say
whether the caller or the callee is wrong. Naming the origin first is what lets
a message read far from where it was thrown still be placed.

---
id: POL-0152
kind: standard
attribution:
  - source: standard-practice
    locator: "unnamed objects"
    upstream: ["CG ES.84", "CG CP.44"]
---

# A local variable has a name, or it is not a variable

Where an object exists for its lifetime alone — a lock, a scope guard — give it a
name. Where the result is genuinely unwanted, do not declare anything.

```cpp
const std::scoped_lock lock(mutex_);           // named: lives to the end of scope
std::scoped_lock(mutex_);                      // temporary: unlocks immediately
```

The second line constructs and destroys the lock in one statement, so the critical
section it was meant to protect runs unlocked. There is no diagnostic, and the code
reads as if it locked.

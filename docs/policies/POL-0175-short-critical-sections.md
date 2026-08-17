---
id: POL-0175
kind: guideline
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.43"]
---

# Do the work outside the lock and hold it only to publish

Compute into locals, then take the lock to swap the result in.

```cpp
const Paths planned = plan_pocket(face, params);      // the expensive part
{
    const std::scoped_lock lock(mutex_);
    results_.push_back(planned);                      // the short part
}
```

Every other thread wanting the mutex waits for the whole body, so work inside the
lock is work the program does serially. Long critical sections also raise the
chance of taking a second lock inside the first, which is where deadlock comes
from.

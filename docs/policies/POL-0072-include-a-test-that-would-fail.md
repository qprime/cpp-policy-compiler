---
id: POL-0072
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing: include a test that would fail"
---

# Include a test that would fail on a plausible wrong implementation

A suite where every test passes against a plausible wrong implementation is not
testing. For each unit, name the wrong version somebody could reasonably have
written, and include the case that distinguishes it.

```cpp
// A checksum that ignores its input passes this
CHECK(checksum(bytes).size() == 32);

// It does not pass this
CHECK(checksum(bytes) != checksum(other_bytes));
```

The wrong implementations worth defeating are the near ones: the off-by-one
boundary, the empty input, the ignored parameter, the swapped pair of arguments
(POL-0016). Not an implementation that returns nothing at all.

Tests written from the code inherit the code's assumptions, so they assert what
the implementation does rather than what it was required to do, and they pass by
construction. That failure mode leaves no trace: the suite is green, the count is
high, and the one thing missing is any case whose outcome was in doubt. Choosing
the wrong implementation first is what makes the test an experiment rather than a
transcript.

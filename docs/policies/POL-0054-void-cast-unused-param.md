---
id: POL-0054
kind: anti-pattern
replacement: [POL-0016]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: void-cast unused param"
---

# Never silence an unused parameter with a void cast

`(void)param;` marks a parameter that should not exist. On a leaf function,
delete the parameter and the call sites that pass it.

Allowed where the signature is mandated and cannot be changed: a virtual
override, an interface implementation, a callback registered with a foreign API.
There the unnamed-parameter form says the same thing without a statement:

```cpp
void on_event(const Event&, int /*retry_count*/) override;
```

An unused parameter is an interface claiming to need something it does not, and
every caller pays by computing a value that is discarded. The cast makes the
warning go away and leaves the claim standing, so the next reader supplies the
argument carefully and the one after that adds a second unused parameter by the
same reasoning. Deleting it is what makes the signature match what the function
does, which is the only version of the signature that stays true.

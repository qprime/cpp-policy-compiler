---
id: POL-0015
kind: standard
trigger: "declare a global variable"
attribution:
  - source: standard-practice
    locator: "global state"
    upstream: ["CG I.2", "CG R.6"]
---

# No non-`const` global variables

Namespace-scope state is `const` or `constexpr`. Mutable state that outlives a
call is owned by an object and passed to whoever needs it.

```cpp
constexpr double kMaxFeedMmPerMin = 12000.0;    // fine

std::vector<Warning> g_warnings;                // no
class Session { std::vector<Warning> warnings_; };   // instead
```

A mutable global gives every function in the program an undeclared parameter and
an undeclared return value. It also makes execution order load-bearing, which is
the fastest route to a defect that reproduces on one machine.

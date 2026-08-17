---
id: POL-0148
kind: guideline
attribution:
  - source: standard-practice
    locator: "constructor mechanics"
    upstream: ["CG C.51", "CG C.52"]
---

# Constructors share their common work by delegating, not by repeating it

```cpp
// Avoid. The same establishment written twice; the second drifts.
Session::Session(Config c) : config_{std::move(c)}, started_{Clock::now()} { validate(); }
Session::Session() : config_{Config::defaults()}, started_{Clock::now()} { validate(); }

// Prefer.
Session::Session(Config c) : config_{std::move(c)}, started_{Clock::now()} { validate(); }
Session::Session() : Session{Config::defaults()} {}
```

A derived class that adds no members of its own inherits its base's constructors
with `using Base::Base` rather than forwarding each one by hand.

A repeated initializer list is the parallel near-duplicate POL-0056 names,
sitting in the one place where the consequence is an invariant. Two constructors
establishing the same invariant separately will eventually establish it
differently, and the object is then valid or not depending on which one the
caller used — which defeats POL-0015 while appearing to satisfy it.

An initialization step that cannot be reached from one delegating chain is a sign
the type has two states rather than one, and the answer is two types (POL-0034)
rather than two constructors.

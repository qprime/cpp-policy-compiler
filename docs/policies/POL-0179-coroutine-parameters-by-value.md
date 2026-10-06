---
id: POL-0179
kind: standard
trigger: "declare a coroutine parameter"
applicability:
  language_version: ["20", "23"]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Coroutines"
    upstream: ["CG CP.53"]
---

# A coroutine owns state needed after suspension

Copy or move the state whose lifetime would otherwise depend on the caller.
Prefer owning parameters by value. A borrowed reference or pointer requires an
explicit guarantee that its referent remains alive through every use, including
suspension and cancellation; passing a pointer or view by value does not provide
that guarantee.

```cpp
Task<Paths> plan_async(PlanarFace face, PocketParams params);

Task<Paths> plan_async(const PlanarFace& face, const PocketParams& params);   // no
```

A coroutine's parameter copies live in its frame, but a reference parameter
copies only the reference. Suspension does not keep the referent alive: if the
caller destroys it before a later use, that use dangles. The caller's frame need
not disappear at suspension, so a reference is not inherently invalid; the
danger is an unstated or unenforced lifetime relationship. By-value pointer and
view parameters have the same borrowing risk.

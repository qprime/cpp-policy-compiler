---
id: POL-0124
kind: standard
attribution:
  - source: standard-practice
    locator: "global and hidden state"
    upstream: ["CG I.1", "CG I.2", "CG I.3", "CG I.22", "CG R.6", "CG E.28"]
---

# A function's inputs and outputs are all in its signature

```cpp
// Never. The result depends on state no caller can see or set.
Registry g_registry;
Plan plan_pocket(const Pocket& p);

// Right. The dependency is a parameter.
Plan plan_pocket(const Registry& registry, const Pocket& p);
```

No non-`const` variable at namespace scope, no singleton, and no error channel
in ambient state — a function reports failure through its return type
(POL-0031), never by setting a flag the caller must remember to read.

A `constexpr` or `const` value at namespace scope is fine and is the intended
home for named constants (POL-0010). What is excluded is mutable state and any
namespace-scope object whose construction runs non-trivial code, because
initialization order across translation units is unspecified.

Hidden state makes a function's result depend on the history of the program
rather than on its arguments, which defeats POL-0007 directly: the same call
returns different answers and nothing in the signature says why. It also makes
the function untestable in the ordinary way, since every test has to establish
and then undo global state, and two tests that forget to undo it interact.

A singleton is this defect with an accessor in front of it. The lifetime and the
threading model are still unstated (POL-0049), and the dependency is still
invisible to every caller.

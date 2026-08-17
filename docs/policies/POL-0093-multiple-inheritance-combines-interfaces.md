---
id: POL-0093
kind: guideline
attribution:
  - source: standard-practice
    locator: "multiple inheritance"
    upstream: ["CG C.135", "CG C.136", "CG C.137"]
---

# Multiple inheritance combines interfaces, not implementations

Deriving from several pure abstract bases is fine. Deriving from several bases
with state is not — compose those as members instead. Do not reach for `virtual`
bases to fix a diamond you chose.

```cpp
class Emitter { public: virtual ~Emitter() = default; virtual std::string emit() const = 0; };
class Named   { public: virtual ~Named() = default;   virtual std::string name() const = 0; };

class GrblPost final : public Emitter, public Named { ... };   // interfaces: fine
```

Two stateful bases means two invariants with one `this` and an initialization
order the derived class does not control. `virtual` inheritance then adds a
runtime offset lookup to reach members and makes construction order harder still.
Composition gives the same reuse with each part's invariant intact.

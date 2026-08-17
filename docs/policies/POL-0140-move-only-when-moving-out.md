---
id: POL-0140
kind: standard
attribution:
  - source: standard-practice
    locator: "move semantics"
    upstream: ["CG ES.56"]
---

# Write `std::move` only where a value is leaving this scope for another

Move into a member, into a container, or into a callee that takes ownership. Do not
move a local you are about to return, do not move a `const` object, and do not read
the source afterwards.

```cpp
moves_.push_back(std::move(move));            // leaving this scope: yes
Toolpath path = assemble();
return path;                                  // elided: no move needed

use(std::move(config));
log(config.name);                             // reads a moved-from object
```

`std::move` is a cast, not an operation: it only marks the value as movable, so
writing it where nothing takes ownership costs nothing and buys nothing. Writing it
where the source is still needed leaves the caller reading an object whose contents
are unspecified.

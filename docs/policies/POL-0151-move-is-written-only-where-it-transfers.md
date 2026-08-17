---
id: POL-0151
kind: standard
attribution:
  - source: standard-practice
    locator: "move and forward"
    upstream: ["CG ES.56", "CG F.19", "CG F.48"]
---

# `std::move` appears only where ownership leaves the current scope

```cpp
// Never. Blocks copy elision; the return was already free.
Plan build() { Plan p = assemble(); return std::move(p); }

// Right.
Plan build() { return assemble(); }

// Right. The value is genuinely leaving this scope.
plans_.push_back(std::move(p));

// Right. A forwarding parameter forwards, once.
template <typename T>
void store(T&& value) { items_.emplace_back(std::forward<T>(value)); }
```

A parameter declared `T&&` in a deduced context is a forwarding reference, not
an rvalue reference: it is passed on with `std::forward<T>` exactly once, and
doing anything else with it after that reads a moved-from object.

`std::move` on a return statement suppresses the copy elision that would
otherwise construct the result in place, so it converts a free return into a
move. It also breaks return-value optimization for a named local, which is the
one case where the compiler was already doing better than the annotation.

Everywhere else, `std::move` is a claim that the source will not be read again.
Writing it where that is untrue leaves a valid but unspecified object that
subsequent code reads without any diagnostic — the value is not garbage, it is
merely not what the author expected, which is the failure POL-0002 ranks worst.

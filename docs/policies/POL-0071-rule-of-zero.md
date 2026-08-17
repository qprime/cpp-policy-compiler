---
id: POL-0071
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: rule of zero"
    upstream: ["CG C.20", "CG C.21", "CG C.22"]
---

# Declare no special member functions; if you declare one, declare all five

A type built out of values and standard containers needs no destructor, no copy,
and no move. If the type's job forces one of the five — copy constructor, copy
assignment, move constructor, move assignment, destructor — write or `= delete`
all five, and keep them consistent with each other.

```cpp
class Toolpath {
 public:
    explicit Toolpath(std::vector<Move> moves);
    // no destructor, no copy, no move — all correct by default

 private:
    std::vector<Move> moves_;
};
```

Declaring a destructor suppresses implicit move generation, which silently turns
every move into a copy — a performance defect with no diagnostic. Declaring some
and not others leaves the type copyable but not movable, or movable in a way that
disagrees with how it copies.

---
id: POL-0021
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #11"
    upstream: ["CG C.20", "CG C.21", "CG C.22"]
  - source: cpp-convention/conventions.md
    locator: "Pattern: rule of zero"
    upstream: ["CG C.66"]
  - source: cpp-convention/mechanisms.md
    locator: "§8 Special members and value semantics"
---

# Rule of zero

Declare no special member function unless you must. If you declare or `= delete`
any one of the copy constructor, copy assignment, move constructor, move
assignment, or destructor, then declare or `= delete` all five.

Move operations are `noexcept`. Comparison is written by hand and symmetric
before C++20; from C++20 it is `= default` on `operator==` and `operator<=>`
for ordering.

POL-0025 carries the shape a type takes when it genuinely must own a resource
directly.

Declaring a destructor suppresses implicit move generation, which silently turns
every move of the type into a copy. There is no diagnostic for that, no test
that fails, and no line of code that changed; the cost appears as a performance
regression whose cause is a declaration in a header. Declaring all five is what
makes the set of operations a single stated decision rather than four
consequences of one.

---
id: POL-0026
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: immutability by default"
    upstream: ["CG Con.1", "CG Con.5", "CG ES.25", "CG P.10"]
---

# Write `const` first, remove it when a mutation is required

The authoring order is the pattern. Every declaration is written `const`, and
`const` comes off only when the code that follows needs to mutate.

```cpp
const Bounds b = bounds_of(records);          // const local
double size_bytes() const { return ...; }     // const member function
void publish(const Payload& payload);         // const parameter
constexpr double kMinFillRatio = 0.5;         // compile-time constant
```

`mutable` exists for a cache that does not participate in the object's observed
value. Anywhere else it is a member that wanted to be non-`const` and was not
declared that way.

POL-0020 states which sites carry `const`. This is how they come to.

Added afterward, `const` records what was true the last time somebody checked,
and the check is skipped exactly on the declarations that were hardest to
reason about. Written first, it is a claim the compiler then verifies, so the
cases where the claim is wrong are the cases that fail to build. The order also
changes what the reader learns from a non-`const` local: it means *this
changes*, and that signal only carries information if the alternative was the
default.

---
id: POL-0135
kind: standard
trigger: "do arithmetic on an unsigned type"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Divergences: [CG ES.107]"
    upstream: ["CG ES.100", "CG ES.101", "CG ES.102", "CG ES.106", "CG ES.107"]
---

# Quantities that may go below zero use signed arithmetic; unsigned arithmetic is deliberate

Use `int`, `std::ptrdiff_t`, or a signed fixed-width type when subtraction or an
intermediate can be negative, including indices used for differences. Unsigned
types are appropriate for modulo arithmetic, masks, shifts, hashes, and APIs whose
range is inherently non-negative. Avoid implicit signed/unsigned mixing; convert
only after establishing the destination range.

```cpp
for (std::ptrdiff_t i = 0; i < std::ssize(moves); ++i) { ... }

const std::uint32_t mask = 0xFFu << shift;       // bits: unsigned

for (std::size_t i = 0; i + 1 < moves.size(); ++i) { ... }   // careful, and easy to get wrong
if (moves.size() - 1 >= 0) { ... }               // always true
```

Unsigned subtraction wraps instead of going negative, so `size() - 1` on an empty
container is a very large number rather than `-1`. Mixing signedness converts the
signed operand to unsigned, which turns a comparison against a negative value into
the opposite answer. Signed overflow is undefined, so choosing signed arithmetic
does not remove the obligation to establish its range.

`gsl::index` would name the signed index type and is not worth a third-party
dependency; a signed standard type carries the same guarantee.

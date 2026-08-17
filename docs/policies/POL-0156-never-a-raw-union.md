---
id: POL-0156
kind: anti-pattern
replacement: [POL-0044]
attribution:
  - source: standard-practice
    locator: "unions"
    upstream: ["CG C.180", "CG Type.7"]
---

# Never declare a raw `union`

```cpp
// Never. Nothing records which member is active; reading the wrong one is UB.
union Value {
    double number;
    std::int64_t count;
};

// Right. The active alternative is part of the type.
using Value = std::variant<double, std::int64_t>;
```

`std::variant` knows which alternative it holds, checks on access, and makes an
added alternative a compile error at every `std::visit` — which is the
exhaustiveness POL-0033 depends on.

A raw `union` puts the discriminant in the programmer's head. Reading a member
other than the one last written is undefined behaviour, and it is undefined
quietly: the bytes are there and reinterpret as something plausible, so the
program continues with a wrong value rather than failing.

Type punning through a union is the same defect as the pointer cast POL-0095
rejects, and it has the same answer: `std::bit_cast` on C++20, `std::memcpy`
before it.

The memory saving that motivates a union is real only where the alternatives are
large and the object count is high. That is a measured, code-local decision, and
`std::variant` costs one discriminant.

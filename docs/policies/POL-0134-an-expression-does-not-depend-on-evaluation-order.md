---
id: POL-0134
kind: standard
attribution:
  - source: standard-practice
    locator: "expression complexity and evaluation order"
    upstream: ["CG ES.40", "CG ES.41", "CG ES.43", "CG ES.44", "CG ES.87"]
---

# One expression, one side effect, and no reliance on the order of the rest

```cpp
// Never. Unspecified which argument is evaluated first.
emit(next_move(cursor), remaining(cursor));

// Never. Two modifications of one object with no sequencing between them.
values[i] = i++;

// Right. Order is stated by statement order.
const auto move = next_move(cursor);
const auto left = remaining(cursor);
emit(move, left);
```

Parenthesize where precedence is not immediately obvious, even where the default
is correct. A condition that is already `bool` is written plainly, without a
redundant `== true` or `!= nullptr`.

An expression that needs study is split into named intermediates, which is
POL-0030 applied inside a statement.

The order in which function arguments are evaluated is unspecified, so an
expression that depends on it produces different results on different compilers
and can change between optimization levels of the same one. That is the class
POL-0007 rules out: the answer is not wrong so much as unverifiable, since no
run tells you what another run will do.

Modifying an object twice without an intervening sequence point is worse — it is
undefined behaviour, and the compiler is entitled to assume it does not happen.

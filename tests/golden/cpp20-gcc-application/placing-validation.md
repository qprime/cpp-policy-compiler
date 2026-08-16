cpp20-gcc-application › Placing validation

Read when: deciding where a check lives — boundaries validate, internals trust.

## SHOULD — Compile time or runtime

POL-0036 · CG P.5, CG P.6, CG P.7, CG Con.5, CG F.4

| Question | Mechanism |
|----------|-----------|
| Can this be wrong at compile time? | Make it a type error: distinct types, `enum class`, exhaustive dispatch (POL-0033) |
| Is this value known at compile time? | `constexpr` (POL-0020) |
| Is this a fact about types the reader should see? | `static_assert` with a message |
| Must this be checked at runtime? | Check it **once**, at the boundary, and encode the result in a type (POL-0027) |

The last row is the one that gets skipped. Having checked at runtime, encode the
result; otherwise the same check reappears downstream and the answer is computed
again by code that could have been given it (POL-0045).

Each row up the table catches its class of mistake earlier and in more of the
cases, which is the whole ordering. A compile-time error is found once, by
whoever is building, for every input. A runtime check is found by whoever runs
the case that triggers it, which is a subset of inputs nobody enumerated. The
runtime check is not wrong where it is the only option; it is wrong where it was
chosen without asking the three questions above it.

## SHOULD — Public API is validated; internals trust their contracts

POL-0041

Validation happens where untrusted values enter: a public entry point, a parsed
file, user input, an FFI seam. Past that edge, internal helpers trust what was
established and do not re-check it.

Where a check is genuinely load-bearing inside, it becomes a type rather than a
repeated test (POL-0027). Where it is a "cannot happen" restatement, it is an
`assert` and nothing more.

The named escape is the FFI layer, which converts and validates at the seam and
is permitted the boilerplate that implies (POL-0064). Document it as the
boundary it is.

Internal re-validation is not defence in depth, because the second check has no
more information than the first and no way to do anything different with a
failure. What it does have is its own idea of what to do when the value is bad,
and two such ideas in one call chain produce two behaviours for one input
(POL-0045). Concentrating validation at the boundary is what makes the boundary
findable later, when the question is where a bad value could have entered.

## NEVER — Never check the same precondition at every call site

POL-0045

The same precondition checked in three functions is not thoroughness. It is an
invariant that was never established, paid for three times, and drifting the
moment one site's fallback differs from another's.

```cpp
// site A
const int attempts = policy.max_attempts > 0 ? policy.max_attempts : kDefaultAttempts;
// site B, written later, different fallback, silent divergence in behaviour
const int attempts = policy.max_attempts > 0 ? policy.max_attempts : 1;
```

Establish the invariant once, at construction (POL-0022), and validate at the
boundary rather than inside (POL-0041). Both defences then delete.

The second check has no information the first did not, and no ability to do
anything useful with a failure, so what it actually contributes is a second
opinion about what an invalid value means. Two opinions in one call chain produce
two behaviours for one input, and nothing connects them, so the disagreement is
invisible until the outputs are compared. It is also self-reinforcing: each new
consumer sees defensive checks upstream, reads them as the local convention, and
adds a third.

---
id: POL-0036
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: compile time or runtime"
    upstream: ["CG P.5", "CG P.6", "CG P.7", "CG Con.5", "CG F.4"]
---

# Compile time or runtime

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

---
id: POL-0129
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "§9 Generic code"
  - source: standard-practice
    locator: "constraining a template"
    upstream: ["CG I.9", "CG T.12", "CG T.13", "CG T.41", "CG T.47", "CG T.150"]
---

# Every template parameter states what it requires

```cpp
// Never, on C++20. The requirement is discoverable only by instantiating it.
template <typename Range>
double total_length(const Range& moves);

// Right.
template <std::ranges::input_range Range>
    requires std::same_as<std::ranges::range_value_t<Range>, Move>
double total_length(const Range& moves);
```

Below C++20 the same information goes in a `static_assert` at the top of the
body. The requirement is stated either way; only the spelling changes with the
standard.

Constrain on what the body actually uses and nothing more. A constraint listing
requirements the implementation never exercises rejects valid callers, and it
becomes wrong silently the moment the body changes.

An unconstrained template with a common name is worse than an unhelpful error:
it enters overload resolution for arguments it was never meant to accept, and it
can win against the intended overload.

An unconstrained parameter moves the interface out of the declaration and into
the body, which is the inversion POL-0006 rejects. The caller learns the
requirement from a diagnostic pointing inside the template, at the line that
happened to fail first — so the error names an implementation detail rather than
the contract that was broken.

This is reached only after POL-0040 and POL-0052 have established that a
template is right at all.

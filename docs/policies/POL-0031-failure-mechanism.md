---
id: POL-0031
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: failure mechanism"
    upstream: ["CG E.1", "CG E.2", "CG E.14", "CG E.15", "CG E.30", "CG F.60", "CG I.5", "CG I.10"]
  - source: cpp-convention/mechanisms.md
    locator: "§5 Failure"
---

# Failure mechanism

Pick by what the caller needs, not by what is convenient to write.

| Mode | Use when |
|------|----------|
| Optional | Absence is the only failure mode and there is nothing to explain (POL-0009) |
| Result type | Failure carries information the caller must act on |
| Exception | Genuinely exceptional: allocation failure, invariant violation, unrecoverable corruption |
| `assert` | "Cannot happen", because upstream validation already guarantees it. Sparingly; repeated asserts mean a missing wrapper type (POL-0027) |
| Silent partial output | **Never.** |

The result type is `std::expected<T, E>` from C++23. Earlier standards use a
project-local result type and migrate on the move to 23; they do not take a
third-party `expected` for it.

Exception types are purpose-designed, never built-in ones reused. Throw by
value, catch by reference, and use no exception specification other than
`noexcept`.

Where a module compiles without exceptions — a real-time target, a small binary,
some FFI hosts — one error-code convention is chosen for that module and stated
in its top-level header. The word doing the work is *one*: a module with two
conventions has neither.

The mechanism is part of the signature, so choosing it wrongly is a decision
every caller inherits and none can revise. An exception where a result belongs
forces every caller into a `try` block for an outcome that is ordinary; a result
where an exception belongs makes an unrecoverable state something a caller can
ignore by not reading the return. Choosing from what the caller must do is what
keeps the cost at the one site that knows.

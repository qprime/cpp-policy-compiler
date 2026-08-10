---
id: POL-0022
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: value type with invariant"
    upstream: ["CG C.2", "CG C.8", "CG C.41", "CG C.42", "CG C.45", "CG C.46", "CG C.49", "CG Con.2"]
  - source: cpp-convention/mechanisms.md
    locator: "§7 Invariants and preconditions"
---

# Value type with invariant

The type that carries a constraint makes the constructor the only way in, so no
consumer has to ask whether the constraint holds.

```cpp
class RetryPolicy {
 public:
    RetryPolicy(int max_attempts, double backoff_ms, double jitter_ratio);

    int max_attempts() const { return max_attempts_; }
    double backoff_ms() const { return backoff_ms_; }
    double jitter_ratio() const { return jitter_ratio_; }

 private:
    int max_attempts_;
    double backoff_ms_;
    double jitter_ratio_;
};

RetryPolicy::RetryPolicy(int max_attempts, double backoff_ms, double jitter_ratio)
    : max_attempts_(max_attempts),
      backoff_ms_(backoff_ms),
      jitter_ratio_(jitter_ratio) {
    if (max_attempts <= 0) {
        throw std::invalid_argument("RetryPolicy: max_attempts must be > 0, got " +
                                    std::to_string(max_attempts));
    }
    if (jitter_ratio < 0.0 || jitter_ratio > 1.0) {
        throw std::invalid_argument("RetryPolicy: jitter_ratio must be in [0, 1], got " +
                                    std::to_string(jitter_ratio));
    }
}
```

Six rules travel with the shape:

- Validate in the constructor, never in an `init()` the caller must remember.
- Throw when construction cannot produce a valid object; the message is
  POL-0011.
- Members are `private` and accessors are `const`.
- Initialize in the member-init list; do not assign in the body.
- A single-argument constructor is `explicit`.
- Do not write a default constructor that only zeroes members. Use default
  member initializers.

Where a caller wants to test rather than catch, add a static `try_from`
alongside. It delegates to the constructor and does not restate the validation;
its return type is the optional mechanism for the declared standard (POL-0009).

```cpp
static std::optional<RetryPolicy> try_from(int max_attempts, double backoff_ms,
                                           double jitter_ratio);
```

Without the invariant, every consumer defends itself, and each one picks its own
value for the invalid case. Two such sites produce two behaviours for one input
and nothing links them, so the disagreement surfaces as an output difference
nobody can trace to a declaration. With the invariant both defences delete, and
the question of what an invalid value means is answered once, where the object
is created.

---
id: POL-0147
kind: standard
attribution:
  - source: standard-practice
    locator: "special members, default and delete"
    upstream: ["CG C.80", "CG C.81"]
---

# A special member that is stated is stated as `= default` or `= delete`

```cpp
// Never. A hand-written copy that does exactly what the compiler would.
Config(const Config& other) : retries_{other.retries_}, path_{other.path_} {}

// Right.
Config(const Config&) = default;
NonCopyable(const NonCopyable&) = delete;
NonCopyable& operator=(const NonCopyable&) = delete;
```

`= default` where the compiler's semantics are wanted and the declaration is
needed anyway — because another special member was declared, or because the
access level differs. `= delete` where the operation should not exist, and then
the whole group goes, since deleting copy without deleting move leaves a type
that moves when the author meant it to do neither.

A hand-written member-wise copy is the compiler's implementation, retyped, and
it stops matching the moment a member is added. Nothing reports the omission:
the new member is simply not copied, and the object is silently half-initialized.

`= delete` is preferred to a private undeclared member because the error arrives
at the call site, naming the deleted function, rather than as a link failure
somewhere else. Most types need none of this — POL-0021 is the default, and this
is what to write when the rule of zero does not apply.

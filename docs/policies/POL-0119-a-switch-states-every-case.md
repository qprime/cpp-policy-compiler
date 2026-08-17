---
id: POL-0119
kind: standard
attribution:
  - source: standard-practice
    locator: "control flow, switch"
    upstream: ["CG ES.78", "CG ES.79"]
---

# A `switch` states every case and never falls through by accident

```cpp
// Never. Is the missing break deliberate? Nothing says, and no warning fires.
switch (mode) {
    case CompactMode::Full: prepare();
    case CompactMode::Incremental: run(); break;
}

// Right. Deliberate fallthrough is marked; the rest break.
switch (mode) {
    case CompactMode::Full:
        prepare();
        [[fallthrough]];
    case CompactMode::Incremental:
        run();
        break;
}
```

A `switch` over an enumeration lists every enumerator and has no `default`.
`default` is for a genuinely open set — a value arriving from outside the
program — and there it handles the common case rather than silently absorbing
everything.

Omitting `default` is what makes `-Werror=switch` under POL-0089 report a new
enumerator as a build error, which is the mechanism POL-0033 relies on. A
`default` arm defeats it: the switch keeps compiling after the enumeration
grows, and the new case falls into whatever the default happened to do. Marked
fallthrough is the same argument at statement level — the compiler cannot
distinguish an intended fallthrough from a forgotten `break` unless the code
says which one it is.

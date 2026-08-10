---
id: POL-0050
kind: anti-pattern
replacement: [POL-0006]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: auto by default"
    upstream: ["CG ES.11"]
---

# Never use `auto` where the type is the load-bearing fact

`auto` removes redundant repetition of a type name. It is not a default, and
where the type is what the reader needs to know, it removes the answer.

```cpp
auto it = entries.begin();               // fine — the type is noise
auto store = std::make_unique<Store>();  // fine — the type is on the right
auto result = compact(store, params);    // not fine — is this a Result, an optional, a bool?
```

The test is whether the right-hand side already spells the type, or the type is
unspellable. Where neither holds, write the type.

Removing a type name removes the one place a reader can check that a call
returns what the next line assumes. That check matters most exactly where the
name was omitted, because a returned optional and a returned value read
identically at the call and differ at every use after it. `auto` in that position
also survives a change to the callee's return type without a diagnostic, so the
code keeps compiling and starts meaning something else.

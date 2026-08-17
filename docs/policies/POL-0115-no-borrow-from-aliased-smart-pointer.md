---
id: POL-0115
kind: standard
attribution:
  - source: standard-practice
    locator: "aliased smart pointers"
    upstream: ["CG R.37"]
---

# Do not pass a pointer or reference taken from a smart pointer that may be reseated

Copy the smart pointer for the duration of the call, or take a local copy of the
owner, when the callee could cause the original to be reset or reassigned.

```cpp
void run(ToolTable& table) {
    const auto held = table.active();          // local share: object stays alive
    process(*held);
}

void run(ToolTable& table) {
    process(*table.active());                  // process() may reload the table
}
```

`process` reaching back into `table` and reloading it drops the last owning
reference, so the reference it is executing against is destroyed underneath it.
The local copy keeps the object alive for exactly as long as the call needs it.

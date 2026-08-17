---
id: POL-0178
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.110", "CG CP.111"]
---

# One-time initialization is a function-local `static` or `std::call_once`

```cpp
const ToolTable& default_tools() {
    static const ToolTable table = load_tool_table(kDefaultsPath);
    return table;
}
```

```cpp
if (table_ == nullptr) {                            // no
    const std::scoped_lock lock(mutex_);
    if (table_ == nullptr) { table_ = load(); }
}
```

Function-local `static` initialization is thread-safe and happens exactly once —
the compiler emits the guard. Hand-written double-checked locking reads the pointer
outside the lock, which is a data race unless the pointer is atomic with the right
ordering, and getting that right is the whole reason the language provides the
feature.

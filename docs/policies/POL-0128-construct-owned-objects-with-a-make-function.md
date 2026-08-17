---
id: POL-0128
kind: pattern
attribution:
  - source: standard-practice
    locator: "make functions"
    upstream: ["CG C.150", "CG C.151", "CG R.22", "CG R.23"]
---

# Make function

```cpp
auto exporter = std::make_unique<GcodeExporter>(config);
auto shared_table = std::make_shared<ToolTable>(load_tools(path));
```

`std::make_unique` and `std::make_shared` are how an owned heap object is
created. Both name the type once, both hand the allocation to its owner within a
single expression, and neither leaves a window in which the memory is unowned
(POL-0127).

`std::make_shared` also places the control block and the object in one
allocation. Reach for it only where ownership is genuinely shared (POL-0048);
the default remains `std::unique_ptr`.

The exception is a custom deleter, which `make_unique` cannot express. There the
constructor takes the raw pointer, still in one statement.

Writing `std::unique_ptr<T>(new T(...))` names `T` twice, which is one more
place for the two to disagree after a later edit. It also reintroduces the
unowned window the smart pointer exists to remove, since the argument is
evaluated before the constructor runs and the compiler may interleave it with
other arguments in the same call.

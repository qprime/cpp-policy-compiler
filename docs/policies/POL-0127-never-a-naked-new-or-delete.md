---
id: POL-0127
kind: anti-pattern
replacement: [POL-0128]
attribution:
  - source: standard-practice
    locator: "allocation"
    upstream: ["CG ES.60", "CG ES.61", "CG R.10", "CG R.12", "CG R.13"]
---

# Never write `new`, `delete`, `malloc`, or `free` outside a resource-owning type

```cpp
// Never. Any throw between the two lines leaks; the delete is on every path.
Exporter* e = new GcodeExporter(config);
run(e);
delete e;

// Never. The allocation is unowned until the call returns, and the order of
// evaluation of the two arguments is unspecified.
emit(std::unique_ptr<Exporter>(new GcodeExporter(cfg)), compute_budget());

// Right.
auto e = std::make_unique<GcodeExporter>(config);
run(*e);
```

Where an allocation genuinely must be explicit, it is handed to its owner in the
same statement and nothing else happens in that statement (POL-0128).

`delete[]` pairs with `new[]` and `delete` with `new`, but neither should appear:
a dynamic array is a `std::vector` (POL-0109).

A raw allocation is a resource with no owner until something takes it, and every
path between the two is a leak the compiler will not mention. It is also the one
case where an exception thrown by unrelated code destroys memory safety, because
the stack unwinds past a pointer nobody is responsible for. RAII removes the
window rather than narrowing it, which is what POL-0003 asks of every resource.

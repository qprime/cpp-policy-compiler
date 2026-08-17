---
id: POL-0083
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: is inheritance right"
    upstream: ["CG C.82"]
---

# Never call a virtual function from a constructor or destructor

Call the base version explicitly, or move the call to a factory that runs after
construction completes.

```cpp
ScanLoop::ScanLoop(const Machine& machine) {
    reset();                    // virtual: runs the base override, not the derived one
}
```

During the base constructor and the base destructor the object's dynamic type is
the base, so virtual dispatch resolves to the base and pure virtual dispatch is
undefined behaviour. The call looks polymorphic and is not, which is a defect no
reader finds by inspection.

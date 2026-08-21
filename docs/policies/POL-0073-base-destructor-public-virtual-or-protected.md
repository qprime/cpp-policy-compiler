---
id: POL-0073
kind: standard
trigger: "declare the destructor of a base class"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: is inheritance right"
    upstream: ["CG C.35", "CG C.127"]
---

# A base class destructor is public and virtual, or protected and non-virtual

If callers delete through the base, it is `public virtual`. If they never do, it
is `protected` non-virtual, and deleting through the base becomes ill-formed. Any
class with a virtual function gets one of the two.

```cpp
class PostProcessor {
 public:
    virtual ~PostProcessor() = default;              // deleted through base
    virtual std::string emit(const Move& move) const = 0;
};

class ScanStep {
 protected:
    ~ScanStep() = default;                           // never deleted through base
};
```

A public non-virtual destructor on a base makes `delete base_ptr` undefined
behaviour that compiles cleanly and leaks the derived part. The two legal shapes
each make the mistake impossible rather than merely unlikely.

---
id: POL-0159
kind: standard
attribution:
  - source: standard-practice
    locator: "overloading and name hiding"
    upstream: ["CG C.138", "CG C.140", "CG F.51"]
---

# A derived class re-exposes the whole overload set, and a default argument is stated once

```cpp
// Never. write(std::span) hides every base overload; the base one stops being callable.
class GcodeExporter : public Exporter {
 public:
    void write(std::span<const Move>) override;
};

// Right.
class GcodeExporter : public Exporter {
 public:
    using Exporter::write;
    void write(std::span<const Move>) override;
};
```

Prefer a default argument to two overloads that differ only by one parameter. A
default states the relationship once; two overloads state it twice and the
second one drifts (POL-0056).

A default argument on a virtual function is never repeated or changed in an
override. Default arguments are resolved by static type and the call by dynamic
type, so the override runs with the base's default, and the code reads as if the
override's applies.

A name declared in a derived class hides every base declaration of that name,
regardless of signature. So adding one overload silently removes the others from
overload resolution for that type, and callers get a conversion error naming
argument types rather than any mention of the hiding.

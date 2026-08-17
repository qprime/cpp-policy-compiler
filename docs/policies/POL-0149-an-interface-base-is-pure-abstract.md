---
id: POL-0149
kind: standard
attribution:
  - source: standard-practice
    locator: "abstract interface shape"
    upstream: ["CG C.121", "CG C.126"]
---

# A base used as an interface is pure abstract and has no constructor

```cpp
class Exporter {
 public:
    virtual ~Exporter() = default;
    Exporter(const Exporter&) = delete;
    Exporter& operator=(const Exporter&) = delete;

    virtual void write(std::span<const Move> moves) = 0;
    virtual std::string_view extension() const = 0;

 protected:
    Exporter() = default;
};
```

No data members, no implemented functions, every function pure virtual. An
abstract class with no state needs no user-written constructor — there is
nothing to establish — so the only one present is the protected default that
stops the interface being instantiated directly.

Adding data or an implementation to an interface base makes it two things at
once: a contract every implementer must satisfy, and a partial implementation
every implementer inherits whether it suits them or not. Changing either half
then forces a change on every derived class, which is the coupling POL-0018
draws dependency direction to avoid.

This is the shape after POL-0037 has established that a hierarchy is right.
Variation over a fixed, known set is `std::variant` (POL-0044); an interface is
for a set that is open, where implementations arrive from elsewhere.

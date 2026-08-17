---
id: POL-0063
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: value type with invariant"
    upstream: ["CG C.9", "CG C.133", "CG C.134"]
---

# Data members are private and share one access level

Every data member of a `class` is `private`. No `protected` data — a derived class
gets access through a `protected` member function if it needs it. An aggregate
`struct` has all-public members and no invariant; there is no middle shape.

```cpp
class Spindle {
 public:
    double rpm() const { return rpm_; }

 protected:
    void set_rpm(double rpm);      // controlled, not raw access

 private:
    double rpm_;
};
```

`protected` data widens the invariant's guardianship to every present and future
derived class, which is a wider contract than `public` and harder to see. Mixed
access levels on non-`const` data mean no single place is responsible for the
invariant.

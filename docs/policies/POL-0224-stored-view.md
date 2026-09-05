---
id: POL-0224
kind: anti-pattern
trigger: "store a span or string_view without an explicit lifetime contract"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "4. Sequences"
replacement: ["POL-0222"]
---

# A stored view with no enforced lifetime relationship

```cpp
class Job {
 public:
    explicit Job(std::string_view name) : name_(name) {}

 private:
    std::string_view name_;        // valid only while the caller's string lives
};
```

The view refers to data the object does not own, so the object's validity depends on
a caller going out of scope later — a use-after-free waiting for the first caller who
passes a temporary. Own the data with `std::string` or `std::vector<T>` if the object
retains it; take the view as a parameter if it needs it only for the call.

A stored view is legitimate when the type's documented contract ties its lifetime
to stable backing storage and construction prevents temporaries or other short-lived
sources. Make that exceptional borrowing relationship explicit; otherwise own the
retained data.

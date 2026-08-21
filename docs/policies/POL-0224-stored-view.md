---
id: POL-0224
kind: anti-pattern
trigger: "store a span or a string_view as a member"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "4. Sequences"
replacement: ["POL-0222"]
---

# A `std::span` or `std::string_view` stored as a member

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

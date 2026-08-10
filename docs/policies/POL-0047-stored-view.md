---
id: POL-0047
kind: anti-pattern
replacement: [POL-0035]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: stored view"
  - source: cpp-convention/mechanisms.md
    locator: "§4 Sequences, in every standard"
---

# Never store a non-owning view as a member

A view refers to data it does not own — `std::span` or `std::string_view` where
the declared standard has them, an iterator pair or a bare pointer earlier.
Stored as a member, it ties the object's validity to data the object does not
control.

```cpp
// Never: the object outlives whatever the caller passed, and nothing says so
class Parser {
 public:
    explicit Parser(std::string_view text) : text_(text) {}
 private:
    std::string_view text_;
};

// Instead: own it if the object retains it
class Parser {
 public:
    explicit Parser(std::string text) : text_(std::move(text)) {}
 private:
    std::string text_;
};
```

Take a view as a parameter where the function needs the data only for the
duration of the call. Store an owning member where the object retains it. The
choice is decided by lifetime, not by the cost of the copy.

A stored view is a use-after-free waiting for a caller to go out of scope first,
and the construction site is where it looks correct. The defect surfaces
somewhere else, at a time determined by the caller's control flow, and it
surfaces as garbage data rather than as a fault, because the memory is usually
still mapped. Nothing in the class can detect it: the view has no way to know
whether what it points at is still there.

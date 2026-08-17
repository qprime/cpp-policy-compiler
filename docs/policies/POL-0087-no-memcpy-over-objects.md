---
id: POL-0087
kind: standard
attribution:
  - source: standard-practice
    locator: "object copying"
    upstream: ["CG C.90", "CG SL.con.4"]
---

# Objects are copied by their constructors and assignment operators, not by `memcpy`

Use assignment, construction, or a standard algorithm. `std::memcpy` and
`std::memset` are for byte buffers of trivially copyable types, and nothing else.

```cpp
Tool copy = original;                             // yes
std::memcpy(&copy, &original, sizeof(Tool));      // no
std::memset(&tool, 0, sizeof(Tool));              // no
```

`memcpy` over a non-trivially-copyable type duplicates pointers without ownership
and skips every invariant the constructor enforces; `memset` over one destroys
its vtable and its members' internal state. Both are undefined behaviour that
usually appears to work at first.

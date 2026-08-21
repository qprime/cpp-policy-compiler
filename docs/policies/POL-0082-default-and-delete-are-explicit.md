---
id: POL-0082
kind: standard
trigger: "write a special member the compiler would write, or remove one"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "8. Special members and value semantics"
    upstream: ["CG C.80", "CG C.81"]
---

# Say `= default` for the compiler's version and `= delete` to remove one

Where a special member must appear — because another one forced the set — write
`= default` for the ones whose generated behaviour is right and `= delete` for the
ones the type must not have. Never write an empty body where `= default` will do.

```cpp
class SerialPort {
 public:
    ~SerialPort();
    SerialPort(const SerialPort&) = delete;
    SerialPort& operator=(const SerialPort&) = delete;
    SerialPort(SerialPort&&) noexcept = default;
    SerialPort& operator=(SerialPort&&) noexcept = default;
};
```

`= default` keeps the member trivial where it can be, which `{}` does not.
`= delete` makes a wrong call a compile error at the call site; the older trick of
declaring it private and undefined makes it a link error with no line number.

---
id: POL-0011
kind: guideline
trigger: "touch an OS handle, a C library object, or a bit-packed format"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: rule of zero"
    upstream: ["CG P.11"]
---

# Wrap a messy construct in one small type rather than spreading it

When code must touch something ugly — an OS handle, a C library object, a
bit-packed wire format — put it behind one type whose only job is that. Every
other type composes it and never sees the mess.

```cpp
class SerialPort {
 public:
    explicit SerialPort(const std::string& device);
    ~SerialPort();
    SerialPort(const SerialPort&) = delete;
    SerialPort& operator=(const SerialPort&) = delete;
    SerialPort(SerialPort&&) noexcept;
    SerialPort& operator=(SerialPort&&) noexcept;

    std::size_t write(std::span<const std::byte> bytes);

 private:
    int fd_;
};
```

One type owning the mess is one place to audit and one place to port. Spread
across callers, the same mess is a cleanup nobody can finish and a defect class
that reappears with every new call site.

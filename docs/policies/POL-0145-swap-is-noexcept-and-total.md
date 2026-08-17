---
id: POL-0145
kind: standard
attribution:
  - source: standard-practice
    locator: "swap"
    upstream: ["CG C.83", "CG C.84", "CG C.85"]
---

# A value type that needs `swap` provides a `noexcept` one that cannot fail

```cpp
class Buffer {
 public:
    friend void swap(Buffer& a, Buffer& b) noexcept {
        using std::swap;
        swap(a.data_, b.data_);
        swap(a.size_, b.size_);
    }
 private:
    std::unique_ptr<std::byte[]> data_;
    std::size_t size_{0};
};
```

Provide it as a free function in the type's namespace so argument-dependent
lookup finds it (POL-0123), and call it through the `using std::swap` idiom so
the member-wise fallback applies where no custom one exists.

Most types need none of this: rule of zero (POL-0021) gives a correct `swap`
already, and this is written only where the special members were written.

`swap` is `noexcept` because the standard library and the copy-and-swap idiom
both depend on it — a `swap` that can throw leaves both objects in an
indeterminate state with no way to recover either, which is the case POL-0144
rules out for the same reason. It also has no failure mode to report: exchanging
two objects that already exist allocates nothing and acquires nothing.

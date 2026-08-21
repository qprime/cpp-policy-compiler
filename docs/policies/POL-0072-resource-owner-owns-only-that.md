---
id: POL-0072
kind: pattern
trigger: "write a type that owns a raw resource"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: rule of zero"
    upstream: ["CG C.30", "CG C.31", "CG C.32", "CG C.33"]
---

# A type that owns a raw resource owns nothing else

When a resource has no RAII wrapper — an OS handle, a C library object — write a
type whose only member is that resource and whose destructor releases it.
Everything else composes that type.

```cpp
class ClipperPaths {
 public:
    explicit ClipperPaths(const Polygon& poly);
    ~ClipperPaths() { clipper_free(handle_); }

    ClipperPaths(const ClipperPaths&) = delete;
    ClipperPaths& operator=(const ClipperPaths&) = delete;
    ClipperPaths(ClipperPaths&& other) noexcept;
    ClipperPaths& operator=(ClipperPaths&& other) noexcept;

 private:
    clipper_paths* handle_;
};
```

A raw pointer member is the question *is this owning* — answer it in the type. If
it owns, the destructor releases it and the other four special members follow. If
it does not, the member documents whose lifetime it depends on. Mixing resource
ownership with business logic means every future change to the logic risks the
release path.

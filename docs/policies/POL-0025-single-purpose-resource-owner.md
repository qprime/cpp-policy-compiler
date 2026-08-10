---
id: POL-0025
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: rule of zero"
    upstream: ["CG C.20", "CG C.31", "CG P.11"]
---

# A type that owns a resource directly owns nothing else

A type built out of values and standard containers declares no special member
functions, because the generated ones are correct.

```cpp
class Journal {
 public:
    explicit Journal(std::vector<Entry> entries);
    // no destructor, no copy, no move — all correct by default

 private:
    std::vector<Entry> entries_;
};
```

A resource with no RAII wrapper — an OS handle, a C library object, a mapping —
gets a type of its own that does nothing but own it. That type writes the five
special members (POL-0021); everything else composes it and goes back to
declaring none.

```cpp
class FileHandle {          // owns the descriptor and nothing else
 public:
    explicit FileHandle(const std::string& path);
    ~FileHandle();
    FileHandle(FileHandle&&) noexcept;
    FileHandle& operator=(FileHandle&&) noexcept;
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    int fd() const { return fd_; }

 private:
    int fd_;
};
```

Hand-written special members are where lifetime bugs live, so the pattern is
arranged to need as few of them as possible. Confining them to a type with one
member means the copy, the move, and the destructor each have one thing to get
right, and they are reviewable in isolation from whatever composes them. A type
that owns a handle *and* holds application state has to get both right in every
one of the five, and gets rewritten whenever the application state changes.

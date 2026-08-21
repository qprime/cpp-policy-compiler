---
id: POL-0112
kind: guideline
trigger: "overload an allocation function"
attribution:
  - source: standard-practice
    locator: "allocation overloads"
    upstream: ["CG R.15"]
---

# A type that overloads allocation overloads the matching deallocation

If a class declares `operator new`, it declares `operator delete` with the
matching signature, in the same class, releasing to the same arena.

```cpp
class ScanNode {
 public:
    static void* operator new(std::size_t size) { return scan_arena().allocate(size); }
    static void operator delete(void* p, std::size_t size) noexcept {
        scan_arena().deallocate(p, size);
    }
};
```

An overloaded `operator new` without its partner sends the memory back to the
global `operator delete`, which does not own it. That is heap corruption with no
diagnostic and no crash near the cause.

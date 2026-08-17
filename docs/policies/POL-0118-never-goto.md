---
id: POL-0118
kind: anti-pattern
replacement: [POL-0117]
attribution:
  - source: standard-practice
    locator: "control flow, goto"
    upstream: ["CG ES.76"]
---

# Never write `goto`

```cpp
// Never. The C idiom for cleanup, in a language that has destructors.
int load(const char* path) {
    FILE* f = std::fopen(path, "rb");
    if (!f) { goto fail; }
    if (!read_header(f)) { goto cleanup; }
    ...
cleanup:
    std::fclose(f);
fail:
    return -1;
}

// Right. The destructor is the cleanup path, and there is one exit per outcome.
std::expected<Header, LoadError> load(const std::filesystem::path& path) {
    auto file = FileHandle::open(path);
    if (!file) { return std::unexpected(LoadError::NotFound); }
    return read_header(*file);
}
```

Take an early `return` and a resource-owning type (POL-0117, POL-0025).

`goto` exists in generated C++ because the training corpus contains C, where it
is the only way to reach one cleanup block from several failure points. C++
removed the need: a destructor runs on every path out of a scope, including the
ones nobody wrote. What remains is a jump that makes the set of paths into a
block unbounded, so no reader can enumerate the states in which a label is
reached, and no compiler warning depends on it.

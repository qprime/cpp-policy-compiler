---
id: POL-0055
kind: anti-pattern
replacement: [POL-0002]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: empty-stub public function"
---

# Never ship a public function that returns `{}` because it is unimplemented

A function in a public header returning a default-constructed value is
indistinguishable from one that legitimately produced an empty result.

```cpp
// Never: the caller gets an empty result and no reason to doubt it
std::vector<Entry> load_entries(const Path& path) { return {}; }

// Instead, where a caller needs the symbol before the body exists
[[noreturn]] std::vector<Entry> load_entries(const Path& path);
// ... throws std::logic_error("not implemented: load_entries")
```

Deletion is the first answer. The throwing form exists for the case where a
caller must compile against the symbol first. An unimplemented function gets no
FFI binding.

The empty return is a silent wrong answer, which is the failure mode with no
downstream detection at all (POL-0002). Callers write their handling for the
empty case, tests are written that pass against it, and the stub acquires
dependants that will keep working when the real body lands and starts returning
data. Whoever implements it then discovers the interesting part was never the
body, it was the four callers who built on the empty result.

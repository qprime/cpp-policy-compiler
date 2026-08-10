---
id: POL-0052
kind: anti-pattern
replacement: [POL-0040]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: premature template"
    upstream: ["CG T.10", "CG T.120"]
---

# Never templatize for two callers

A function with two concrete callers is not generic. It is two callers.

```cpp
// Never: the parameter is a coincidence of the two call sites
template <typename Container>
std::size_t total_size(const Container& c);

// Instead: write what the callers need; generalize on the third
std::size_t total_size(const std::vector<Entry>& entries);
```

Templatize on a third concrete caller, or where the alternative is a
runtime-typed interface that loses checking (POL-0040). On C++20 the parameter
carries a concept; earlier it carries a `static_assert`.

Generalizing from two examples produces an abstraction shaped by whatever those
two happened to share, which is usually not the axis that varies. Two callers do
not distinguish a real axis from a coincidence, so the third caller either fits
by luck or forces the parameterization to be redone with dependants already
attached. Waiting costs one duplicated function, which is cheap and visible; the
wrong axis costs a rewrite and is neither.

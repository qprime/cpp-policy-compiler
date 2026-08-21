---
id: POL-0202
kind: guideline
trigger: "constrain on a syntactic accident two types share"
attribution:
  - source: standard-practice
    locator: "tag types"
    upstream: ["CG T.24"]
---

# Where two requirements differ only in meaning, distinguish them with a tag

Give the type an explicit trait or tag it opts into, and constrain on that rather
than on a syntactic accident.

```cpp
struct ClosedPathTag {};
struct OpenPathTag {};

template <class T>
concept ClosedPath = std::same_as<typename T::path_category, ClosedPathTag>;
```

Two path types can expose the same operations and mean different things — one closes,
one does not — so no syntactic requirement separates them. The tag makes the
distinction explicit and requires the type's author to state which they are, which is
the only place the answer is actually known.

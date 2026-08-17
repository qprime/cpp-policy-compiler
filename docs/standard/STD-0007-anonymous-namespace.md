---
id: STD-0007
group: files-and-layout
enforced_by: clang-tidy
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: module boundary"
    upstream: ["CG SF.21", "CG SF.22"]
---

# Internal entities live in an anonymous namespace in the source file

Everything not declared in the header goes in an unnamed namespace in the `.cpp`.
Never an unnamed namespace in a header, and never `static` at namespace scope in
its place.

```cpp
// algo/plan_2d.cpp
namespace proj::algo {
namespace {

constexpr int kHelixSegments = 60;
Paths plan_pocket_spiral(const ConvexPolygon& face, const PocketParams& params);

}  // namespace
}  // namespace proj::algo
```

In a header, an unnamed namespace gives every including translation unit its own
copy of each entity, so a `constexpr` becomes a distinct object per file and
addresses compare unequal.

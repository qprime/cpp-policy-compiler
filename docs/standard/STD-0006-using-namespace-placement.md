---
id: STD-0006
group: files-and-layout
enforced_by: clang-tidy
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: module boundary"
    upstream: ["CG SF.6", "CG SF.7"]
---

# `using namespace` appears only inside a function body

Never at namespace scope in a header. Never at global scope anywhere. A single
`using` declaration naming one entity is fine at function scope; the directive form
is for a customization point or a literal suffix.

```cpp
std::string format_feed(double mm_per_min) {
    using namespace std::string_literals;      // function scope: fine
    return "F"s + std::to_string(mm_per_min);
}
```

```cpp
// plan_2d.hpp
using namespace std;                           // no: every includer inherits it
```

A directive in a header applies to every translation unit that includes it,
directly or not, so one header can change overload resolution across the whole
build.

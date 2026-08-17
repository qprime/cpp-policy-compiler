---
id: POL-0066
kind: pattern
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "2. Closed-set variation"
    upstream: ["CG C.180", "CG C.181", "CG C.182"]
---

# A fixed set of alternatives is dispatched so that adding one breaks the build

Write `std::variant` plus `std::visit` with one overload per alternative. Where a
`union` is genuinely needed for size, it is an anonymous `union` behind a
discriminant, never a bare one.

```cpp
struct Comment { std::string text; };
struct SetRpm  { double rpm; };
struct Rapid   { std::optional<double> x, y, z; };
struct Cut     { std::optional<double> x, y, z, feed; };

using Move = std::variant<Comment, SetRpm, Rapid, Cut>;

std::string emit(const Move& move) {
    return std::visit(overloaded{
        [](const Comment& c) { return "; " + c.text; },
        [](const SetRpm& s)  { return format_rpm(s.rpm); },
        [](const Rapid& r)   { return format_rapid(r); },
        [](const Cut& c)     { return format_cut(c); },
    }, move);
}
```

One overload per alternative, never a generic `[](auto&&)` fallback: a catch-all
compiles for every future alternative and silently swallows the case you just
added, destroying the only property the variant was chosen for. Below C++17 the
same guarantee comes from an `enum class` tag and a `default`-less `switch` under
`-Werror=switch`.

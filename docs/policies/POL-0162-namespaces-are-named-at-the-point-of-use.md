---
id: POL-0162
kind: standard
attribution:
  - source: standard-practice
    locator: "namespaces"
    upstream: ["CG SF.6", "CG SL.3"]
---

# No `using namespace` in a header, and nothing is added to `namespace std`

```cpp
// Never, in a header. Every file that includes it inherits the whole namespace.
using namespace std;

// Right. Qualify, or name the one thing, in the narrowest scope that needs it.
std::vector<Move> moves;

void sort_moves(std::vector<Move>& moves) {
    using std::swap;                      // a customization point, function scope
    std::ranges::sort(moves, by_depth);
}
```

In a source file a `using` declaration for a specific name is fine at function
scope. A `using namespace` directive is permitted only at function scope, and
`using namespace std` is not written at all.

`namespace std` is not extended. The one permitted addition is a specialization
of a standard template for a type of your own — `std::hash<ToolId>` (POL-0146)
— which is what the standard explicitly allows.

A directive in a header imposes itself on every translation unit downstream,
where it silently changes overload resolution in code that never asked for it.
The failure is not a compile error at the header but an ambiguity or a wrong
overload selected several files away, with nothing at that site to explain why.

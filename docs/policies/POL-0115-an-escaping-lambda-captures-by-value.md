---
id: POL-0115
kind: standard
attribution:
  - source: testimony/coding-rules-2026-07.md
    locator: "Lambdas 3"
  - source: testimony/coding-rules-2026-07.md
    locator: "Lambdas 4"
  - source: testimony/coding-rules-2026-07.md
    locator: "Lambdas 5"
  - source: standard-practice
    locator: "lambdas, capture lifetime"
    upstream: ["CG F.52", "CG F.53"]
---

# A lambda that outlives the current scope captures by value

```cpp
// Never. handler_ outlives this function; label_ is a dangling reference.
void Panel::install() {
    const std::string label_ = title();
    handler_ = [&label_] { log(label_); };
}

// Right. The lambda owns what it needs.
void Panel::install() {
    handler_ = [label = title()] { log(label); };
}

// Right. Runs and dies inside the call; borrowing is safe and avoids a copy.
std::ranges::sort(tools, [&required_mm](const Tool& a, const Tool& b) {
    return a.fit(required_mm) < b.fit(required_mm);
});
```

Stored in a member, returned, queued, or handed to another thread all count as
outliving. By-reference capture is permitted only where the lambda provably
runs and dies within the current scope, which is the algorithm-comparator case
above.

A by-reference capture is a non-owning view with the lifetime rules of one
(POL-0047), and it carries no diagnostic when it escapes. The compiler accepts
a returned lambda holding a reference to a dead local exactly as readily as a
correct one, so the defect surfaces as corrupted data at call time rather than
as a build failure. Capturing by value converts the question from a lifetime
the reader has to trace into a copy the declaration states.

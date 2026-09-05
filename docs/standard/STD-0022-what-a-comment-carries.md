---
id: STD-0022
group: comments
enforced_by: review
review_trigger: "a comment restates code or fails to explain non-obvious intent"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Naming"
    upstream: ["CG NL.1", "CG NL.2", "CG NL.3"]
---

# A comment states intent, never mechanism

Write a comment for what the code cannot say: why this constant, why this order,
which rule an exception breaks, what a foreign API requires. Do not restate the
line below it. Keep it to a sentence or two.

```cpp
// Clipper needs closed rings wound clockwise; ours arrive counter-clockwise.
std::ranges::reverse(points);

// Reverse the points.
std::ranges::reverse(points);            // no
```

A restating comment is a second copy of the code that nothing keeps in step, so it
becomes wrong at the first edit and then misleads. Where a name can carry the
meaning, the name is the better comment.

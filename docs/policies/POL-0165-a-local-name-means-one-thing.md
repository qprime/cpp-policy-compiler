---
id: POL-0165
kind: standard
attribution:
  - source: standard-practice
    locator: "local names"
    upstream: ["CG ES.12", "CG ES.26"]
---

# A local name is never reused and never shadows an outer one

```cpp
// Never. count means two things, and the inner tool hides the outer one.
int count = tools.size();
count = failures.size();

for (const auto& tool : tools) {
    for (const auto& tool : tool.inserts()) { check(tool); }
}

// Right.
const auto tool_count = tools.size();
const auto failure_count = failures.size();

for (const auto& tool : tools) {
    for (const auto& insert : tool.inserts()) { check(insert); }
}
```

A variable holds one thing for its whole life. Reusing it for a second purpose
is two variables sharing storage, and it is what blocks the `const` POL-0020
asks for.

Shadowing compiles silently, so an edit to the inner block that meant to touch
the outer name touches the inner one instead, and the outer value is simply
never updated. `-Wshadow` reports it, which is why the warning set in POL-0089
is worth having.

Both are the same defect at different scales: a name that does not identify one
value forces the reader to track which meaning is live at each line, and the
declaration no longer answers what the name is (POL-0097).

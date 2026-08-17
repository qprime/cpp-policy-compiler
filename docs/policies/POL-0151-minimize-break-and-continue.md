---
id: POL-0151
kind: guideline
attribution:
  - source: standard-practice
    locator: "loop exits"
    upstream: ["CG ES.77"]
---

# Prefer a loop whose condition says when it stops

Where the body is short, a `break` or `continue` is fine. Where the loop is long or
has several of them, extract the body into a named function and return from it, or
express the traversal with an algorithm.

```cpp
const auto first_cut = std::ranges::find_if(moves, is_cut);

for (const Move& move : moves) {
    if (!is_cut(move)) { continue; }
    if (out_of_envelope(move)) { break; }
    ...                                        // 30 lines, two hidden exits
}
```

Several exits scattered through a long body mean the loop's exit conditions cannot
be read in one place, so a reader has to hold the whole body to know when it stops.

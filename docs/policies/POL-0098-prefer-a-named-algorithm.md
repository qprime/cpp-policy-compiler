---
id: POL-0098
kind: standard
attribution:
  - source: standard-practice
    locator: "iteration"
    upstream: ["CG ES.71", "CG SL.con.1"]
---

# Prefer a named standard algorithm to a hand-written loop

```cpp
// Never. The reader reconstructs "first tool wide enough" from the body.
const Tool* found = nullptr;
for (std::size_t i = 0; i < tools.size(); ++i) {
    if (tools[i].diameter_mm >= required_mm) { found = &tools[i]; break; }
}

// Right. The name is the intent.
const auto found = std::ranges::find_if(
    tools, [required_mm](const Tool& t) { return t.diameter_mm >= required_mm; });
```

On C++20 prefer the `std::ranges` overloads: passing the container once removes
the mismatched-iterator-pair failure mode. Below C++20 the iterator pair is the
only spelling.

Where no algorithm fits, use range-`for` rather than an index loop. Reach for
an index only when the index itself is part of the computation.

An index loop makes the reader derive the intent from the mechanism, which is
the inversion POL-0006 names. It also carries the bound, the comparison, and
the increment as three separate things to get wrong, and off-by-one lives in
all three. A named algorithm has none of them and states in its name what the
loop would have had to be read to discover.

---
id: POL-0013
kind: anti-pattern
replacement: [POL-0009]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: sentinel value"
---

# Never encode absence in a sentinel value

NaN meaning *no value*. `-1` meaning *not found*. `""` meaning *unset*. `0`
meaning *unset* on a field where zero is a legal reading. Each takes a value the
type can legitimately hold and overloads it with a second meaning the type
cannot distinguish from the first.

```cpp
// Never: the signature admits -1, so absence flows into arithmetic and indexing
int find_index(const std::vector<Item>& items, Id id);   // -1 when absent
const int i = find_index(items, id);
total += weights[i];                                     // -1 becomes a huge index

// Instead: absence has its own type, and the check cannot be skipped
std::optional<std::size_t> find_index(const std::vector<Item>& items, Id id);
if (const auto i = find_index(items, id)) { total += weights[*i]; }
```

Shown in its C++17 form. POL-0009 carries the positive rule and the mechanism
for each standard. NaN in output is a defect to investigate, never a value with
meaning.

The cost is paid where the two meanings collide, which is never the site that
chose the sentinel. A NaN from a failed computation and a NaN meaning "nothing
here" are the same bits, so the bug and the intent are indistinguishable
everywhere downstream. Sentinels look cheap because they need no new type, and
they are what generation reaches for by default when working from the shape of
the data alone.

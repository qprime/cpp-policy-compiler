---
id: POL-0102
kind: anti-pattern
replacement: [POL-0101]
attribution:
  - source: standard-practice
    locator: "arithmetic, mixed comparison"
    upstream: ["CG ES.100"]
---

# Never compare a signed value with an unsigned one

```cpp
// Never. offset converts to unsigned; a negative offset passes the guard.
int offset = compute_offset();
if (offset < path.size()) { use(path[offset]); }

// Right. One type, and the negative case is caught.
const auto count = static_cast<std::int64_t>(path.size());
if (offset >= 0 && offset < count) { use(path[static_cast<std::size_t>(offset)]); }
```

The fix is the type, not a cast at the comparison. A cast that silences the
warning keeps the defect and removes the diagnostic.

The signed operand converts to unsigned before the comparison, which turns
`-1 < 1u` into false. A bounds check written against a negative index therefore
admits it, and the indexing that follows reads out of bounds. `-Wsign-compare`
under POL-0089 makes this a build error, which is the only reason it is
survivable at all — the line reads correctly in every language the author might
be coming from, and it does not mean what it says here.

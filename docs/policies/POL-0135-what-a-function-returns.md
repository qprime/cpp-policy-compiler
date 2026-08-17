---
id: POL-0135
kind: guideline
attribution:
  - source: standard-practice
    locator: "return types"
    upstream: ["CG F.42", "CG F.44", "CG F.45", "CG F.49"]
---

# What a function returns

| Return | When |
|--------|------|
| By value | The usual case, including several outputs as a struct (POL-0023) |
| `T&` | A copy is genuinely undesirable and there is always an object to return |
| `T*` | A position that may not exist — and `std::optional` is preferred where it can hold the answer |
| `std::optional<T>` / `std::expected<T, E>` | The operation can fail (POL-0031) |

```cpp
// Never. Returning const by value blocks the caller from moving out of it.
const Plan build(const Input& in);

// Never. Returns a reference to a destroyed temporary.
Plan&& build(const Input& in);

// Right.
Plan build(const Input& in);
```

Never return an rvalue reference, and never write `return std::move(local)` — it
prevents the copy elision that would otherwise remove the move entirely.

A returned `T*` says only *here is a position*; it never means the caller now
owns something. Ownership transfer is `std::unique_ptr` (POL-0014).

Return by value is the default because it is the only form with no lifetime
question attached. A reference or pointer return makes the caller responsible
for knowing how long the referent lives, and that knowledge is not in the
signature — which is exactly what POL-0003 asks a declaration to carry.

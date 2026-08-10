---
id: POL-0035
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: how to pass a parameter"
    upstream: ["CG F.15", "CG F.16", "CG F.17", "CG F.18", "CG F.20", "CG F.21", "CG F.24", "CG F.43", "CG F.60", "CG Con.3"]
  - source: cpp-convention/conventions.md
    locator: "Tier 2: sequence parameters, non-owning string parameters"
  - source: cpp-convention/mechanisms.md
    locator: "§4 Sequences"
    upstream: ["CG I.13"]
---

# How to pass a parameter

| Pass by | When |
|---------|------|
| Value | Small and cheap to copy; or the callee modifies its own copy; or the callee moves from it |
| `const T&` | A larger type the callee only reads |
| `T&` | In-out. Rare — prefer returning a value |
| `T*` | Null is a meaningful value |
| `T&&` | The callee moves from it and the caller knows |
| Sequence view | A read-only or write-through sequence, spelled per the declared standard |
| Return by value | Output. Always preferred to an out-parameter |

Return a struct for multiple outputs. Never return a reference or a pointer to a
local.

The sequence view and the non-owning string parameter are the two rows whose
spelling moves with the standard:

| | C++11 | C++17 | C++20 |
|---|-------|-------|-------|
| Sequence | Iterator pair, or `const std::vector<T>&` when the caller genuinely owns a vector | same | `std::span<const T>` to read, `std::span<T>` to write |
| Non-owning string | `const std::string&` | `std::string_view` | `std::string_view` |

A `(const T*, size_t)` pair is permitted only at an `extern "C"` boundary, and it
is converted on entry (POL-0046). A non-owning view is never stored as a member
in any standard (POL-0047).

Passing is the one decision in a signature that every call site pays and none
can change. Getting it wrong is rarely a defect and always a cost: a large type
by value copies at every call, an out-parameter forces a default-constructed
local before every call, and a reference where a value belongs adds a lifetime
question to a function that had none. The table exists so the choice is made
from what the callee does rather than from what reads well in the declaration.

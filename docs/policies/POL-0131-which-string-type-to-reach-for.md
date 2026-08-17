---
id: POL-0131
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "§11 Strings and formatting"
  - source: standard-practice
    locator: "string types"
    upstream: ["CG SL.str.1", "CG SL.str.4", "CG SL.str.5", "CG SL.str.10", "CG SL.str.12"]
---

# The string type states what it owns and what it holds

| Need | Type |
|------|------|
| Own a character sequence | `std::string` |
| Refer to one without owning it | `std::string_view`; `const std::string&` below C++17 |
| A single character | `char` |
| Raw bytes that are not text | `std::span<const std::byte>` |
| Locale-sensitive operation | `std::string`, never a view |

```cpp
void log_label(std::string_view label);
std::string build_label(const Tool& t);
const auto suffix = "mm"s;
```

Use the `s` suffix where a `std::string` is wanted from a literal, so overload
resolution does not pick the `const char*` form and allocate somewhere else.

A `std::string_view` is a non-owning view and carries POL-0047's rule with it: a
parameter, never a member, and never returned from a function whose argument
owned the characters.

`char*` for a sequence is the pointer-and-length pair POL-0046 rejects, with the
length replaced by a convention about a terminator. Bytes that are not text are
`std::byte` rather than `char` because `char` participates in arithmetic and
locale rules that mean nothing for a byte, and its signedness is
implementation-defined — so the same expression differs across platforms
(POL-0007).

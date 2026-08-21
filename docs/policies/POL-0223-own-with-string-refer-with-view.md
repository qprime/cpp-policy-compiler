---
id: POL-0223
kind: standard
trigger: "hold characters, or refer to characters you do not own"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "11. Strings and formatting"
    upstream: ["CG SL.str.1", "CG SL.str.2", "CG SL.str.4", "CG SL.str.5", "CG SL.str.10", "CG SL.str.11", "CG SL.str.12"]
---

# Own characters with `std::string`; refer to them with `std::string_view`

| Need | Type |
|------|------|
| Own a character sequence | `std::string` |
| Refer to one, read-only | `std::string_view` |
| Refer to one, mutating | `std::span<char>` |
| One character | `char`, or `char*` for exactly one |
| Raw bytes that are not text | `std::byte` |
| Locale-sensitive operation | `std::string`, at one boundary |

```cpp
class Job {
    std::string name_;                          // owns
};

bool is_comment(std::string_view line);         // refers
void upcase(std::span<char> text);              // mutates
std::span<const std::byte> payload();           // bytes, not characters

using namespace std::string_literals;
const auto prefix = "G1"s;                      // a string, not a char*
```

`std::string_view` does not own, so storing one as a member ties the object's
validity to data it does not control. `std::byte` has no arithmetic and no character
semantics, which is what stops byte buffers being formatted as text by accident.

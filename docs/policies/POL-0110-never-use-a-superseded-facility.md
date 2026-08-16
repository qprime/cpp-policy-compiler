---
id: POL-0110
kind: anti-pattern
replacement: [POL-0109]
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "§13 Standard-specific bans"
  - source: standard-practice
    locator: "standard library, superseded facilities"
    upstream: ["CG SL.io.50"]
---

# Never use a facility a later standard superseded

| Never | Since | Use instead |
|-------|-------|-------------|
| `std::auto_ptr` | C++11 | `std::unique_ptr` |
| `std::bind` | C++11 | a lambda |
| `throw()` exception specification | C++11 | `noexcept` |
| `NULL`, or `0` as a null pointer | C++11 | `nullptr` |
| `register` | C++11 | *(delete it)* |
| `std::random_shuffle` | C++11 | `std::shuffle` |
| `std::endl` where `'\n'` will do | any | `'\n'` |
| `std::ostringstream` to format a number | C++20 | `std::format` |
| `enable_if` SFINAE for a constraint | C++20 | a concept or `requires` |
| Compound assignment on `volatile` | C++20 | `std::atomic` |
| A third-party `expected` | C++23 | the project's result type until `std::expected` |

`std::endl` flushes, which turns a loop of writes into a loop of system calls
for no effect the author intended.

Every entry here remains legal, which is the reason the list exists. A
generator's training weights decades of code that predates the replacement, so
these are what it produces by default and nothing in the build objects. Each
has a direct modern equivalent that is shorter, safer, or both, so the
replacement costs nothing but knowing which one it is (POL-0093).

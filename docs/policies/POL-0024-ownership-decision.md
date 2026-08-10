---
id: POL-0024
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: ownership decision"
    upstream: ["CG R.3", "CG R.4", "CG R.5", "CG R.20", "CG R.21", "CG F.60"]
---

# Ownership decision

Four questions, in order. The first *yes* is the answer.

| Question | Answer |
|----------|--------|
| Does this need to outlive the current scope? | **No** → a value or an automatic variable. Do not heap-allocate. |
| Is there exactly one owner? | **Yes** → `std::unique_ptr<T>`, transferred by move. |
| Are there genuinely multiple independent owners with no primary? | **Yes** → `std::shared_ptr<T>`. |
| None of the above; you only need to look at it | `const T&`, or `T*` where null is meaningful. Non-owning, always. |

Most code stops at the first question. A value member, a `std::vector<T>`, and a
`const&` parameter cover the large majority of real ownership needs, and they
are the forms that leave no lifetime question to answer.

Answer the questions in order rather than reaching for the form that always
works. `std::shared_ptr` always works, which is why it is what an unresolved
ownership question turns into (POL-0048): the design keeps compiling and the
question stops being asked. Asking in this order forces the cheapest correct
answer, and it makes the expensive one a decision somebody made rather than a
default nobody noticed.

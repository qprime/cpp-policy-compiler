---
id: POL-0044
kind: anti-pattern
replacement: [POL-0033, POL-0037]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: inheritance for variation"
    upstream: ["CG C.129"]
---

# Never build a hierarchy to represent a fixed set of alternatives

A base class with a virtual destructor and one derived class per alternative is
a v-table where a variant belongs.

```cpp
// Never: the alternatives are fixed, and this spends an allocation to say so
class Event { public: virtual ~Event() = default; };
class Connect : public Event { std::string endpoint_; };
class Send : public Event { std::size_t size_bytes_; };

// Instead: the set is closed, so the compiler can check it is covered
using Event = std::variant<Connect, Send, Close>;
```

Inherit only for an open set of behaviours injected by a caller, behind an
interface that carries no data. POL-0037 is the test.

Three costs arrive together and none of them is visible at the declaration. Every
value becomes a heap allocation and a pointer chase, which is a performance
decision made by a type choice. Handling moves into virtual functions, so adding
an operation touches every class rather than one function. Most of all, the
compiler stops being able to report a missing case: adding a fourth derived class
is well-formed everywhere, including at the sites that needed to know.

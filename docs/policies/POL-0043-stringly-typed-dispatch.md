---
id: POL-0043
kind: anti-pattern
replacement: [POL-0033]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: stringly-typed dispatch"
  - source: cpp-convention/mechanisms.md
    locator: "§2 Closed-set variation, anti-pattern in every standard"
---

# Never dispatch on a string tag

A struct with a `std::string kind` field and optional payload members is a
tagged union with no checking. Nothing constrains the tag to a known value,
nothing ties a payload to the tag that makes it meaningful, and nothing reports
a case that went unhandled.

```cpp
// Never: any string is a legal tag, and no payload is tied to one
struct Event {
    std::string kind;                        // "connect", "send", "close"
    std::optional<std::string> endpoint;
    std::optional<std::size_t> size_bytes;
    std::optional<int> code;
};

// Instead: one alternative per case, each carrying only its own payload
struct Connect { std::string endpoint; };
struct Send    { std::size_t size_bytes; };
struct Close   { int code; };
using Event = std::variant<Connect, Send, Close>;

std::string render(const Event& event) {
    return std::visit(overloaded{
        [](const Connect& e) { return "connect " + e.endpoint; },
        [](const Send& e)    { return "send " + std::to_string(e.size_bytes); },
        [](const Close& e)   { return "close " + std::to_string(e.code); },
    }, event);
}
```

An `enum class` paired with an if/else-if chain is half a fix. The tag becomes a
real type, and nothing still forces the chain to handle every case. Shown in its
C++17 form; POL-0033 carries the mechanism for each declared standard.

The string tag is what generation reaches for when working from example data,
because the data shows a field whose values happen to be strings. Every property
worth having is then absent at once: the set of alternatives is not written down
anywhere, a typo in a tag is a runtime miss rather than a compile error, and a
payload can be present for the wrong tag or absent for the right one. The cost
is paid by whoever adds the fourth alternative and does not find the site that
needed it.

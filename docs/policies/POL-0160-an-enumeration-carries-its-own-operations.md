---
id: POL-0160
kind: guideline
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "§12 Enumerations"
  - source: standard-practice
    locator: "enumerations, operations"
    upstream: ["CG Enum.4", "CG Enum.6"]
---

# An enumeration is named, and its operations live beside it

```cpp
enum class Severity { Trace, Debug, Info, Warn, Error };

constexpr std::string_view to_string(Severity s) {
    switch (s) {
        case Severity::Trace: return "TRACE";
        case Severity::Debug: return "DEBUG";
        case Severity::Info:  return "INFO";
        case Severity::Warn:  return "WARN";
        case Severity::Error: return "ERROR";
    }
    return "UNKNOWN";
}
```

Conversion, ordering, and validation are free functions in the enumeration's
namespace (POL-0123), each a `switch` with no `default` so a new enumerator is a
build error (POL-0119).

An unnamed enumeration has no type, so its enumerators are integers with a
scope. That gives up everything POL-0103 established — no distinct type, no
exhaustiveness, no overload that can take one.

Without named operations, every call site writes its own `switch` or, worse, a
cast to `int` and an array index. Those copies drift the moment an enumerator is
added, and the array-index form does not even fail to compile: it reads past the
end of the table and returns whatever was there (POL-0133).

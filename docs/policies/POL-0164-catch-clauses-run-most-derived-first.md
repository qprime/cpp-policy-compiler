---
id: POL-0164
kind: standard
attribution:
  - source: standard-practice
    locator: "exception handling, catch order"
    upstream: ["CG E.31"]
---

# `catch` clauses are ordered most-derived first, and catch by `const&`

```cpp
// Never. The base clause matches everything; the second is unreachable.
try { load(path); }
catch (const std::exception& e) { report(e); }
catch (const std::filesystem::filesystem_error& e) { retry(e); }

// Right.
try { load(path); }
catch (const std::filesystem::filesystem_error& e) { retry(e); }
catch (const std::exception& e) { report(e); }
```

Catch by `const&`. Catching by value slices a derived exception down to the
caught type (POL-0121), so the handler loses exactly the information that
distinguished it.

`catch (...)` appears only where the frame must not propagate — the outermost
handler of a thread, or the binding layer translating to the host language
(POL-0059) — and it always rethrows or reports rather than discarding.

Clauses are tried in written order, not by best match, which is the opposite of
overload resolution and the reason this needs stating at all. A base-class
clause written first silently makes every later clause dead code, and most
compilers do not warn.

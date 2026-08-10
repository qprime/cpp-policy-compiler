---
id: POL-0053
kind: anti-pattern
replacement: [POL-0032, POL-0039]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: mid-stack exception translation"
    upstream: ["CG E.3", "CG E.17", "CG E.18"]
---

# Never catch to re-throw a different type at every layer

Catching an exception in order to throw a different one, layer after layer,
produces noise that buries the one place handling actually happens.

```cpp
// Never: three layers of this, and the original site is gone by the top
try {
    return parse(text);
} catch (const ParseError& e) {
    throw StoreError(std::string("parse failed: ") + e.what());
}
```

Translate exactly once, at the FFI boundary, into the host language's mechanism
(POL-0059). Everywhere else, let the exception pass and let the layer that can
act on it catch it (POL-0032).

Exceptions as control flow are forbidden outright.

Each translation replaces a type the handler could have matched on with a string
the handler cannot, and discards the context the original carried. The `try`
blocks then have to exist at every layer, which means every layer's ordinary
path is written around a failure it does nothing about. What survives to the top
is a message assembled from prefixes, and no way to tell which layer originated
the failure or what the caller could have done differently.

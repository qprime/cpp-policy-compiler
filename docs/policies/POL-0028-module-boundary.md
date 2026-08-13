---
id: POL-0028
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: module boundary"
    upstream: ["CG SF.2", "CG SF.5", "CG SF.7", "CG SF.8", "CG SF.11", "CG SF.20", "CG SF.21", "CG SF.22"]
  - source: cpp-convention/conventions.md
    locator: "Trap: cargo-culted mutex"
---

# Module boundary

A header is an interface. What it exposes is a promise; what it hides is free to
change.

```cpp
// include/proj/store/compact.hpp
#ifndef PROJ_STORE_COMPACT_HPP
#define PROJ_STORE_COMPACT_HPP

#include <vector>
#include "proj/types.hpp"

namespace proj::store {

Result compact(const Store& store, const CompactParams& params);

}  // namespace proj::store

#endif  // PROJ_STORE_COMPACT_HPP
```

```cpp
// store/compact.cpp
#include "proj/store/compact.hpp"

namespace proj::store {
namespace {

constexpr int kMaxPassCount = 8;
Result compact_incremental(const Store& store, const CompactParams& params);

}  // namespace
}  // namespace proj::store
```

| Rule | |
|------|--|
| Internal entities live in an anonymous namespace in the `.cpp` | `CG SF.22` |
| Never an anonymous namespace in a header | `CG SF.21` |
| A header is self-contained and compiles alone | `CG SF.11` |
| No object definitions or non-inline function definitions in a header | `CG SF.2` |
| A `.cpp` includes the header declaring its own interface, first | `CG SF.5` |
| No `using namespace` at header scope | `CG SF.7` |
| An `#ifndef` include guard on every header, named `PROJECT_COMPONENT_FILE_HPP`; `#pragma once` is a non-standard vendor extension and is not used | `CG SF.8` |
| Namespaces express logical structure, nested by layer | `CG SF.20` |

Where a module's threading model is not obvious from its declarations, it is
stated in one or two sentences at the top of the header. That statement is what
POL-0049 asks for in place of a defensive mutex; the default it overrides is
single-threaded by contract.

The test for a leaky header: if changing a private implementation detail forces
unrelated translation units to recompile, the detail is in the wrong file.

Everything a header declares is something every consumer now depends on, whether
or not any of them use it. That dependency is invisible at the point it is
created and expensive at every point it is later discovered, because removing a
declaration means finding every file that reached for it. Keeping the header to
the promise is what makes the implementation changeable without a survey of
consumers.

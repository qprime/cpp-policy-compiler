---
id: STD-0005
group: files-and-layout
enforced_by: clang-format
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: module boundary"
    upstream: ["CG SF.4", "CG SF.5", "CG SF.10", "CG SF.11", "CG SF.12", "CG SF.13"]
---

# Includes are grouped in four blocks, own header first

1. The header this source file implements
2. C++ standard library
3. External libraries
4. This project

Blank line between blocks, alphabetical within a block. Quoted form for this
project's headers, angle brackets for everything else. Every header compiles on its
own, and nothing relies on a name arriving through another header.

```cpp
#include "proj/algo/plan_2d.hpp"

#include <optional>
#include <vector>

#include <clipper2/clipper.h>

#include "proj/geom/polygon.hpp"
#include "proj/types.hpp"
```

Own-header-first is what proves the header is self-contained: if it needs something
it does not include, this source file fails to compile.

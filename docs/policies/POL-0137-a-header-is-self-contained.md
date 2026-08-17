---
id: POL-0137
kind: standard
attribution:
  - source: standard-practice
    locator: "include order and self-containment"
    upstream: ["CG SF.4", "CG SF.10", "CG SF.12", "CG SF.13"]
---

# A header compiles on its own, and includes come first

```cpp
// compact.cpp
#include "proj/store/compact.hpp"   // this file's own header, first

#include <algorithm>                 // standard library
#include <vector>

#include "proj/store/entry.hpp"      // project headers
```

A source file includes its own header first, which is what proves the header
stands alone. Everything a header names, it includes; nothing relies on a
transitive include, because the day the intermediate header drops one, this file
stops compiling for a reason unrelated to any change made to it.

Project headers use the quoted form with a path from the include root; standard
and third-party headers use angle brackets. Header names are spelled with
forward slashes and in the case the file actually has, so the build works on a
case-sensitive filesystem.

Every include appears before the first declaration in the file. An include that
follows a declaration makes the included header's meaning depend on what came
before it — macros, `using` declarations, partial types — so the same header
means different things in different files, which is the drift POL-0028 draws the
module boundary to prevent.

---
id: STD-0004
group: files-and-layout
enforced_by: clang-tidy
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: module boundary"
    upstream: ["CG SF.8"]
---

# Include guards are `#ifndef PROJECT_COMPONENT_FILE_HPP`

Every header opens with an `#ifndef`/`#define` pair and closes with an `#endif`
carrying the same name in a comment. The name is project, component, and file,
uppercased and underscore-joined, ending `_HPP`.

```cpp
#ifndef PROJ_ALGO_PLAN_2D_HPP
#define PROJ_ALGO_PLAN_2D_HPP

...

#endif  // PROJ_ALGO_PLAN_2D_HPP
```

`#pragma once` is a vendor extension, not standard C++.

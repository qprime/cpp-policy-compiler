---
id: POL-0228
kind: standard
trigger: "write an error message"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #6"
---

# Every error message carries four parts

What failed, what field, what constraint, and the actual value — in that order, in
one sentence. This holds for an exception, a result payload, a log line, and a
structured warning alike.

```cpp
throw std::invalid_argument("SheetConfig: width_mm must be > 0, got -3.5");
//                           ^^^^^^^^^^^  ^^^^^^^^     ^^^^^     ^^^^^^^^
//                           what failed  what field   constraint  actual

throw std::invalid_argument("invalid width");        // none of the four
throw std::invalid_argument("SheetConfig: bad input");   // two of the four
```

The actual value is the part most often left out and the part that ends the
investigation: without it the reader knows a rule was broken but not by what, so
they reproduce the failure to learn what the message could have told them. The
subsystem name is what makes the message greppable back to one file.

The format is identical in the Python convention, deliberately, so a message reads
the same regardless of which side of the FFI produced it.

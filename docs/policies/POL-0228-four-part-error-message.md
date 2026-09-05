---
id: POL-0228
kind: standard
trigger: "write an error message"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #6"
---

# An input error names the operation, subject, constraint, and safe actual value

For rejected input, state what failed, which field, the constraint, and a safe,
bounded representation of the actual value—in that order, in one sentence. Omit
the value or redact it when it contains a credential, personal data, unbounded
payload, or other information the diagnostic channel must not expose. Failures
without a field or actual value state the applicable context instead of inventing
one.

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

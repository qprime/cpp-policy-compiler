---
id: POL-0089
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments: warnings"
---

# Warnings are errors, and the set is fixed

Every target compiles under `-Wall -Wextra -Wpedantic -Wconversion
-Wsign-conversion -Werror`. `-Werror=switch` is additionally load-bearing rather
than stylistic on a C++11 project, because it is what makes closed-set
exhaustiveness a compile error there (POL-0033).

A per-site disable is permitted and carries a comment stating why, next to the
pragma. A disable without one is indistinguishable from a warning somebody could
not fix.

The conversion warnings are the two most often removed and the two worth most.
Narrowing and sign-changing conversions are silent at the language level and
produce wrong values rather than diagnostics, which is exactly the class this
corpus treats as undefined behaviour's quieter neighbour (POL-0019).

A warning that does not stop the build is a message in a stream nobody reads,
and the number of them only goes up, so the signal is gone by the second week.
Making them errors keeps the count at zero, which is the only count at which a
new one is visible. The set is fixed rather than chosen per project because a
project that picks its own set picks it by removing whatever is currently
failing, and what is currently failing is the interesting part.

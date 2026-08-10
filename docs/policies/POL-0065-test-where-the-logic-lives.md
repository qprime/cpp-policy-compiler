---
id: POL-0065
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing: test where the logic lives"
---

# Test where the logic lives

A unit test targets the function or the class that holds the logic, not the
pipeline that calls it. A test that drives the whole pipeline to exercise one
branch is an integration test, and integration tests are few.

The test for which kind is being written: name the thing that would be wrong if
the test failed. Where that is one function, the test belongs against that
function. Where it is the composition, the test belongs at the composition and
there are only a handful of those.

A pipeline test that fails names the pipeline. Finding which of its stages is
actually wrong is then a separate investigation, run every time, and it takes
longer than the test did. A pipeline test also passes for the wrong reasons:
one stage compensating for another's error produces correct end-to-end output
from two defects, and the composition is the level at which that is invisible.
Testing at the level of the logic makes a failure name its own cause.

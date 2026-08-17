---
id: POL-0168
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
    upstream: ["CG CP.9"]
---

# Once concurrency exists, ThreadSanitizer runs in a build configuration

Add a TSan configuration when the first thread appears and run the test suite under
it. Findings block merge like any other sanitizer finding.

```
cmake -B build-tsan -DCMAKE_CXX_FLAGS="-fsanitize=thread -g"
```

A data race is undefined behaviour that usually produces correct output on the
machine it was written on, so review and testing do not find it. TSan does, and it
is the only cheap tool that does.

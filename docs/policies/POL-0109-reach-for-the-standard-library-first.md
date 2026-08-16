---
id: POL-0109
kind: guideline
attribution:
  - source: standard-practice
    locator: "standard library"
    upstream: ["CG SL.1", "CG SL.2"]
---

# Reach for the standard library before writing the facility yourself

```cpp
// Avoid. A hand-rolled split is code to review, test, and carry forever.
std::vector<std::string> split(const std::string& s, char sep);

// Prefer, on C++20.
for (const auto part : std::views::split(text, ',')) { use(part); }
```

Where the standard has no answer, take the project's existing dependency
before adding a new one, and write the facility only when neither has it.

A C-library facility is never the answer where a C++ one exists: `qsort` takes
a `void*` comparator that defeats type checking and inlining, `strcpy` has no
bound, and `rand` has no distribution guarantee worth relying on.

A hand-written equivalent has to be reviewed, tested, and maintained, and it
will not match the standard version at the edges nobody wrote a test for —
empty input, a single element, self-assignment, an allocation that throws
partway. The standard version has those settled and has had them exercised by
every program that ever ran.

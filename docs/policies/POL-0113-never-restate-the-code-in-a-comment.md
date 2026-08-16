---
id: POL-0113
kind: anti-pattern
replacement: [POL-0112]
attribution:
  - source: standard-practice
    locator: "comments, restatement"
    upstream: ["CG NL.2"]
---

# Never write a comment that restates the code

```cpp
// Never.
// Increment the retry count.
++retries;

// Never. The signature already says all of this.
/// @brief Gets the diameter.
/// @return The diameter.
double diameter_mm() const;
```

Delete it. Where the line genuinely needs explaining, the explanation is a
name or a function (POL-0030), not a sentence above it.

A restating comment doubles the edit surface for no information, and the two
copies drift on the first change that touches one of them. What remains is a
false statement sitting immediately beside a true one, with nothing marking
which is which — and the comment is what a reader in a hurry reads.

Generated docstring blocks are the same defect at scale. They pass any
documentation-coverage check while telling the reader nothing the declaration
did not already say (POL-0112).

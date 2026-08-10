---
id: POL-0058
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions: validation is the calling side's job"
---

# The calling side validates before crossing

The caller validates its arguments before an FFI call. The callee may `assert`
cheaply; it does not re-validate defensively.

This is POL-0041 applied to a seam where the two sides have different type
systems. The validation belongs on the side that has the user's input, the
context to say what went wrong, and something useful to do about it.

An `assert` on the callee side is permitted and is not a second validation. It
documents the contract and fails loudly in a build that checks it, rather than
selecting a fallback.

Split validation across a seam produces two answers to what an invalid argument
means, and the far side's answer is always worse: it has the value and nothing
else. Its diagnostic cannot name the field the user actually supplied, and its
recovery cannot ask for a corrected one. Making the obligation one-sided also
makes it checkable, because there is exactly one place per call where the
argument was known to be good.

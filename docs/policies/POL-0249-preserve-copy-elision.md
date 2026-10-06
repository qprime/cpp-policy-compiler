---
id: POL-0249
kind: guideline
trigger: "return a value assembled over several statements or selected between branches"
review_trigger: "a value-returning function uses std::move on a local or selects named results with a conditional expression"
attribution:
  - source: standard-practice
    locator: "C++ [class.copy.elision], [stmt.return], and [dcl.init]; CG F.20 and F.48"
    upstream: ["CG F.20", "CG F.48"]
---

# Shape value returns for copy elision

Prefer returning a newly constructed value directly. If construction spans
several statements, prefer one named result where that keeps construction and
control flow clear. Return an eligible local by name rather than adding
`std::move`. Do not introduce default construction or assignment solely to
force all branches through one result variable.

```cpp
Toolpath make_line(Vec2 from_mm, Vec2 to_mm) {
    return Toolpath{from_mm, to_mm};
}

Toolpath make(const Request& request) {
    if (request.is_line()) {
        return Toolpath{request.from_mm(), request.to_mm()};
    }
    return Toolpath{request.arc()};
}

Toolpath assemble(const Job& job) {
    Toolpath path;
    path.reserve(job.segment_count());
    for (const Segment& segment : job.segments()) {
        path.append(segment);
    }
    if (job.closed()) {
        path.close();
    }
    return path;
}
```

```cpp
// Bad: constructs both alternatives and returns an lvalue expression.
Toolpath make(bool closed) {
    Toolpath open = assemble_open();
    Toolpath loop = assemble_closed();
    return closed ? loop : open;
}
```

Since C++17, a prvalue of the function's return type initializes the result
directly; C++14 permits but does not guarantee this elision. Returning a
non-volatile automatic local of the same class type, other than a parameter,
permits named return value optimization (NRVO). NRVO is optional: the return
must still be valid if elision does not occur. Implicit move applies to eligible
locals, but the selected constructor can copy, and a deleted move can make the
return ill-formed.

The conditional expression above is an lvalue, not the name of an eligible
local, so it does not qualify for NRVO or implicit move. Separate `return local;`
statements can each qualify for NRVO even when they name different locals;
whether a compiler performs it depends on the implementation and control flow.
Prefer the direct branch returns shown above when each branch constructs its
own result. Moving a member or another expression that is not eligible for
implicit move can be appropriate when ownership is intentionally transferred.

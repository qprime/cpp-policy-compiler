---
id: POL-0249
kind: guideline
trigger: "return a value assembled over several statements or selected between branches"
review_trigger: "a function returns different named locals on different paths"
attribution:
  - source: standard-practice
    locator: "copy elision and named return value optimization"
    upstream: ["CG F.20", "CG F.48"]
---

# Shape value returns for copy elision

Return a newly constructed value directly when possible. If construction spans
several statements, build one named result and return that same object from
every path. Do not add `std::move` to a return.

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
// Bad: competing named results prevent NRVO.
Toolpath make(bool closed) {
    Toolpath open = assemble_open();
    Toolpath loop = assemble_closed();
    return closed ? loop : open;
}
```

Directly returned values have guaranteed copy elision since C++17. A returned
named local is eligible for named return value optimization and is moved if the
compiler does not elide it. Competing named locals prevent NRVO; return a value
directly from each branch or carry the result in one object instead.

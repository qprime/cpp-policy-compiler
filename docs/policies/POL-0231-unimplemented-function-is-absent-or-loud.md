---
id: POL-0231
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: empty-stub public function"
---

# An unimplemented public function is deleted, or it is loud

Delete it until it works. Where a caller genuinely needs the symbol first, mark it
`[[noreturn]]` and throw `std::logic_error("not implemented: <name>")`. Either way it
gets no FFI binding until it is real.

```cpp
[[noreturn]] Paths plan_trochoidal(const PlanarFace& face, const PocketParams& params) {
    throw std::logic_error("not implemented: plan_trochoidal");
}

Paths plan_trochoidal(const PlanarFace& face, const PocketParams& params) {
    return {};                     // indistinguishable from an empty result
}
```

An empty return is a valid answer for most of these signatures, so the stub reports
success and the caller plans a job with no toolpaths in it. The throw makes the gap
arrive at the first call instead of at the machine.

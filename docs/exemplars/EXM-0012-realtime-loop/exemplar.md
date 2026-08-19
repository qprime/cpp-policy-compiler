---
id: EXM-0012
demonstrates:
  - POL-0023
  - POL-0028
  - POL-0032
  - POL-0041
  - POL-0112
  - POL-0128
  - POL-0159
  - POL-0161
  - POL-0162
  - POL-0163
  - POL-0228
  - POL-0240
  - POL-0244
  - POL-0245
  - STD-0021
applicability:
  language_version: ["20", "23"]
  domain: ["realtime"]
---

# A scan-cycle path that allocates nothing, waits for nothing, and says nothing

Every buffer `SampleLoop` needs is reserved in its constructor, which is the one
place a deadline-bound component is allowed to allocate. `write_scan` runs inside the
cycle: it takes no lock, writes no log line, performs no I/O, and refuses to grow
its buffer. A reading that does not fit is counted, and the caller reads the count
at the scan boundary.

`noexcept` on `write_scan` is a claim that holds, because the body reaches nothing
that can throw.

This exemplar is authored and verified against `cpp23-gcc-realtime`. Under a
configuration whose domain is not realtime it constrains out entirely.

## Reading order

- `include/sampler/device/sample_loop.hpp` — the deadline-bound operation marked
  `noexcept`, and two accessors that let the caller see what the cycle recorded
- `device/sample_loop.cpp` — the reserve in the constructor and the capacity check
  that replaces a `push_back` which would have grown
- `device/sample_loop_test.cpp` — the replaced global allocator, the one global the
  corpus permits and the comment saying why, and a claim scoped to exactly what a
  counted delta establishes: this input, this path, zero calls
- `include/sampler/core/temperature.hpp`, `core/temperature.cpp`,
  `core/temperature_test.cpp` — copied verbatim from EXM-0001

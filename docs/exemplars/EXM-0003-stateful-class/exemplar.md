---
id: EXM-0003
demonstrates:
  - POL-0058
  - POL-0063
  - POL-0064
  - POL-0071
  - POL-0088
  - POL-0128
  - POL-0156
  - POL-0159
  - POL-0195
  - POL-0228
  - POL-0240
  - POL-0244
  - POL-0245
  - POL-0247
  - STD-0011
  - STD-0020
applicability:
  language_version: ["20", "23"]
---

# A class that holds state, reached by nobody and reaching nothing

`SampleBuffer` keeps the last N readings. It has an invariant, a representation it
does not publish, and no collaborators at all — no clock, no sink, no device. The
contrast with EXM-0005, which receives both of its collaborators, is the whole point
of EXM-0005.

The five special members are absent because a `std::vector` member already gives the
right copy, move, and destruction.

### Reading order

- `include/sampler/core/sample_buffer.hpp` — standard member names where the
  standard library has one, and `is_`-prefixed names where it does not; the
  representation last
- `core/sample_buffer.cpp` — the capacity invariant, and an eviction written the
  obvious way because no measurement has said otherwise
- `core/sample_buffer_test.cpp` — `drops_the_oldest_reading_when_full` compares the
  whole sequence, so an implementation that evicted the newest fails it
- `include/sampler/core/temperature.hpp`, `core/temperature.cpp`,
  `core/temperature_test.cpp` — copied verbatim from EXM-0001

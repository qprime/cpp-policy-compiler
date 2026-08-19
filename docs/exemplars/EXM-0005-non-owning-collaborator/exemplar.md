---
id: EXM-0005
demonstrates:
  - POL-0014
  - POL-0016
  - POL-0021
  - POL-0022
  - POL-0025
  - POL-0040
  - POL-0057
  - POL-0070
  - POL-0073
  - POL-0081
  - POL-0090
  - POL-0092
  - POL-0240
  - POL-0244
  - POL-0245
  - STD-0007
  - STD-0022
applicability:
  language_version: ["20", "23"]
---

# A class that receives both its collaborators and owns neither

`Sampler` takes a clock and a sink through its constructor and holds each as a
non-owning pointer. Nothing is reached for, nothing is constructed on its behalf,
and its destructor releases nothing — which is what lets the test hand it a sink it
can read afterwards. EXM-0003, whose class has no collaborators at all, is the
contrast this exists against.

The constructor takes references so neither argument can be null; the members are
pointers because a reference member would delete assignment.

## Reading order

- `include/sampler/device/clock.hpp` — a pure abstract base: no data, public
  virtual destructor, copy suppressed, protected default constructor
- `include/sampler/device/reading_sink.hpp` — the same shape beside the aggregate
  it carries, which has no invariant and therefore no class
- `include/sampler/device/sampler.hpp` — the whole dependency visible in the
  constructor signature, and the lifetime assumption stated where a reader of the
  header will meet it
- `device/sampler.cpp` — three lines, because everything it needs arrived through
  the constructor
- `device/sampler_test.cpp` — the two doubles in an anonymous namespace, and
  `destruction_leaves_the_sink_untouched` reading the sink after the sampler is
  gone
- `include/sampler/core/temperature.hpp`, `core/temperature.cpp`,
  `core/temperature_test.cpp` — copied verbatim from EXM-0001

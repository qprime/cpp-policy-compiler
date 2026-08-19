---
id: EXM-0001
demonstrates:
  - POL-0058
  - POL-0059
  - POL-0060
  - POL-0063
  - POL-0069
  - POL-0071
  - POL-0085
  - POL-0133
  - POL-0183
  - POL-0217
  - POL-0228
  - POL-0229
  - POL-0240
  - POL-0242
  - POL-0244
  - POL-0245
  - STD-0003
  - STD-0004
  - STD-0005
  - STD-0008
  - STD-0009
  - STD-0011
  - STD-0012
  - STD-0020
applicability:
  language_version: ["20", "23"]
---

# Three scalar value types, each establishing its invariant in its constructor

`Temperature`, `DeviceId`, and `SampleInterval` are the vocabulary the rest of the
corpus is written in. Each wraps one scalar, rejects the values its domain has no
meaning for, and is otherwise as ordinary as `int`.

Defaulted `operator==` and `operator<=>` are what set the C++20 floor.

### Reading order

- `include/sampler/core/temperature.hpp` — the shape of a validated scalar: one
  private member, an `explicit` constructor, a computing accessor beside a
  returning one, defaulted equality
- `core/temperature.cpp` — the constructor throwing and `try_from` reporting
  absence, over one predicate rather than two copies of the check
- `core/temperature_test.cpp` — every rejected input has a test and `celsius()`
  has none
- `include/sampler/core/device_id.hpp` — the same shape over a `std::string`,
  ordered so it can key a container
- `core/device_id.cpp` — a constructor that moves its argument into place and
  validates what landed
- `include/sampler/core/sample_interval.hpp` — the unit carried by
  `std::chrono::milliseconds` on the way in and by the name `rate_hz` on the way
  out
- `core/sample_interval.cpp` — the one narrowing conversion in the exemplar,
  written out

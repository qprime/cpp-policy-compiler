---
id: EXM-0007
demonstrates:
  - POL-0013
  - POL-0019
  - POL-0033
  - POL-0041
  - POL-0056
  - POL-0058
  - POL-0133
  - POL-0183
  - POL-0191
  - POL-0228
  - POL-0240
  - POL-0244
  - POL-0245
  - POL-0247
  - STD-0011
  - STD-0012
applicability:
  language_version: ["20", "23"]
---

# A domain failure and a programmer error, reported two different ways

Nothing here parses anything or touches a boundary. An input the domain admits but
cannot act on — samples that will not hold still — comes back as absence. An input
that should never have been constructed — a calibration with a scale of zero — throws
where it was constructed, so it never reaches this function at all. The third
mechanism, an `assert` on the non-empty span, is the one no test can claim.

## Reading order

- `include/sampler/core/calibration.hpp` — the two mechanisms visible in the
  declarations: a constructor that can throw, and a `try_` that cannot
- `core/calibration.cpp` — the guard returning `std::nullopt`, the constructor
  throwing with the value that failed, and the `assert` for the condition upstream
  is expected to have settled
- `core/calibration_test.cpp` — `catches_a_plausible_wrong_implementation` asserts
  the calibrated value, so an implementation that ignored the offset, or returned
  the mean unchanged, fails it
- `include/sampler/core/temperature.hpp`, `core/temperature.cpp`,
  `core/temperature_test.cpp` — copied verbatim from EXM-0001

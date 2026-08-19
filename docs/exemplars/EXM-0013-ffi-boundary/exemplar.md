---
id: EXM-0013
demonstrates:
  - POL-0026
  - POL-0028
  - POL-0043
  - POL-0072
  - POL-0079
  - POL-0080
  - POL-0082
  - POL-0109
  - POL-0143
  - POL-0178
  - POL-0183
  - POL-0186
  - POL-0187
  - POL-0216
  - POL-0228
  - POL-0230
  - POL-0234
  - POL-0240
  - POL-0244
  - POL-0245
  - POL-0246
  - STD-0001
  - STD-0004
applicability:
  language_version: ["23"]
---

# One wrapper over a C driver, and the only structured output in the corpus

`DriverSession` is the only code that names a `sampler_driver_*` symbol. It acquires
the foreign handle in its constructor, releases it in its destructor, and converts
every status code the driver can return into a domain failure exactly once. Callers
never see the C API.

`driver.h` is the one file in the corpus that is correctly a `.h`: it is compilable
as C, reachable from both languages, and its guard ends `_H` because that is what
uppercasing the file name gives.

The serializer is golden-tested. `frame.golden` is checked in and diffed on every
run, and the test resolves it relative to the project root, which is where the test
binary runs.

`std::expected` is what sets the C++23 floor.

## Reading order

- `include/sampler/ffi/driver.h` — the C-shaped surface: trivially copyable types,
  an out-parameter for the handle, a status code instead of an exception
- `include/sampler/ffi/driver_adapter.hpp` — the layer declared as the exception to
  validate-at-the-boundary, and a purpose-designed exception type carrying the
  failure it names
- `ffi/driver_adapter.cpp` — the status translated in one `switch`, the handle owned
  by all five special members, and the C string produced at the seam and carried no
  further
- `ffi/driver_adapter_test.cpp` — the fake driver asserting what the C signatures
  cannot state, its counters in a function-local static, and open and close counted
  to a balance
- `ffi/testdata/frame.golden` — three frames, checked in
- `include/sampler/core/temperature.hpp`, `core/temperature.cpp`,
  `core/temperature_test.cpp` — copied verbatim from EXM-0001

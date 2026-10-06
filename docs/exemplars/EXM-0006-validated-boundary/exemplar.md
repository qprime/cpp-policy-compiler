---
id: EXM-0006
situation: turn bytes from outside the program into a validated value or a named failure
demonstrates:
  - POL-0005
  - POL-0041
  - POL-0056
  - POL-0105
  - POL-0133
  - POL-0135
  - POL-0136
  - POL-0183
  - POL-0194
  - POL-0227
  - POL-0240
  - POL-0243
  - POL-0244
  - POL-0245
  - STD-0010
  - STD-0019
applicability:
  language_version: ["23"]
---

# Bytes from outside the program become a validated value, or a named failure

`parse_frame` takes a span, so the bounds arrive with the data, and it establishes
three separate facts before it will return a `Reading`: the frame is whole, the
temperature is a number, and the number is one the domain admits. Each failure the
caller must act on differently has its own enumerator.

`reading_to_frame` checks the binary32 wire range before narrowing a `double`.
It returns `EncodeError::TemperatureOutOfRange` in `std::expected` if the value
exceeds that range or rounding takes it outside the temperature domain. A
validated domain value need not fit a wire
format. The implementation requires eight-bit bytes and IEEE binary32 `float`.
Encoding quantizes arbitrary `double` values; it preserves decoded wire values,
but does not promise an exact round trip for every domain value.

`std::expected` is what sets the C++23 floor. Below it, POL-0183 names a project
result type instead.

### Reading order

- `include/sampler/wire/frame.hpp` — decoding and encoding failure sets as `enum class`, the
  decoded value as an aggregate, and the wire size as one named constant
- `wire/frame.cpp` — unsigned arithmetic confined to the byte assembly,
  `std::bit_cast` where the wire's float has to be read out of four octets, and
  the narrowing back to `float` written out
- `wire/frame_test.cpp` — one frame per rejection, and `round_trips_semantically`
  comparing the decoded values rather than the bytes, plus rejection before an
  out-of-range floating-point conversion
- `include/sampler/core/temperature.hpp`, `core/temperature.cpp`,
  `core/temperature_test.cpp` — copied verbatim from EXM-0001

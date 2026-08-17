---
id: POL-0169
kind: standard
attribution:
  - source: standard-practice
    locator: "bit manipulation"
    upstream: ["CG ES.101"]
---

# Bit manipulation uses an unsigned type of stated width

```cpp
// Never. Shifting into or past the sign bit of a signed type is undefined.
int flags = 1 << 31;

// Right.
constexpr std::uint32_t kReadyFlag = std::uint32_t{1} << 31;
const auto masked = value & kReadyFlag;
```

`std::uint8_t`, `std::uint32_t`, `std::uint64_t` — the width is stated, because
a bit position only means something against a known width. A shift count is
always less than that width; shifting by the width or more is undefined, not
zero.

This is the one exception to POL-0101, which puts arithmetic in a signed type.
The reason POL-0101 gives — that unsigned wraps at zero — is exactly the
behaviour wanted here, where the value is a set of bits rather than a number.
Keep the two apart: a value being manipulated bitwise is not also used in
arithmetic, and if it must be, it converts at one named point.

On C++20 prefer `std::popcount`, `std::countl_zero`, `std::rotl`, and
`std::has_single_bit` to hand-written equivalents (POL-0109). Each of these is a
loop that is easy to write subtly wrong and that the standard already has
correct.

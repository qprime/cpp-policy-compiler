---
id: EXM-0004
demonstrates:
  - POL-0009
  - POL-0028
  - POL-0071
  - POL-0072
  - POL-0074
  - POL-0079
  - POL-0080
  - POL-0082
  - POL-0109
  - POL-0110
  - POL-0133
  - POL-0228
  - POL-0240
  - POL-0244
  - POL-0245
  - STD-0005
  - STD-0022
applicability:
  language_version: ["17", "20", "23"]
---

# A type that owns one descriptor and nothing else

`DeviceFile` acquires a POSIX descriptor in its constructor and releases it in its
destructor. It carries no path, no buffer, and no device state, so every future
change to what a device *does* leaves the release path alone. Declaring the
destructor forces the other four, and all five are written.

The two compile-time properties — not copyable, `noexcept`-movable — are asserted
beside the definition, because a test file is the wrong place for a question the
compiler already answered.

`std::is_copy_constructible_v` is what sets the C++17 floor.

## Reading order

- `include/sampler/device/device_file.hpp` — the whole set of five, the one
  comment the code cannot carry, and the two `static_assert`s at the definition
  site
- `device/device_file.cpp` — acquisition failing in the constructor, a destructor
  that cannot throw, move assignment handling `x = x`, and the platform headers in
  the third include block
- `device/device_file_test.cpp` — `moved_from_handle_closes_nothing` outlives the
  moved-from object and then asks the operating system whether the descriptor
  survived

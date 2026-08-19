---
id: EXM-0008
demonstrates:
  - POL-0035
  - POL-0057
  - POL-0066
  - POL-0105
  - POL-0106
  - POL-0107
  - POL-0108
  - POL-0143
  - POL-0144
  - POL-0145
  - POL-0228
  - POL-0240
  - POL-0244
  - POL-0245
  - STD-0009
  - STD-0010
applicability:
  language_version: ["17", "20", "23"]
---

# A closed set dispatched twice, so that adding an alternative breaks both sites

`DeviceState` is a `std::variant` of four alternatives and `Health` is an `enum
class` of three. Each is dispatched with no fallback: the two `std::visit` call
sites carry one lambda per alternative and no `[](auto&&)`, and the `switch` over
`Health` carries no `default`. Add an alternative and every site that must handle
it stops compiling.

Nothing here asserts the number of alternatives. A `std::variant_size_v` check
would fix an incidental count and establish nothing the dispatch sites do not
already enforce.

The `throw` after the `switch` is not dead: an `enum class` object can hold a value
no enumerator names, and the warning set requires the function to say what it does
with one.

`std::variant` is what sets the C++17 floor.

## Reading order

- `include/sampler/core/device_state.hpp` — four alternatives as their own types,
  the enumeration with neither an underlying type nor explicit values, and its
  operations declared beside it
- `core/device_state.cpp` — the overload-set helper in an anonymous namespace, two
  dispatch sites that each name every alternative, and a `default`-less `switch`
- `core/device_state_test.cpp` — one test per behaviour, including the formatted
  fault carrying the error it was constructed with

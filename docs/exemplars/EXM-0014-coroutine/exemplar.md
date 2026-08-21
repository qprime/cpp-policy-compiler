---
id: EXM-0014
situation: write a coroutine that suspends on a read and resumes with the value
demonstrates:
  - POL-0071
  - POL-0072
  - POL-0079
  - POL-0080
  - POL-0082
  - POL-0109
  - POL-0163
  - POL-0173
  - POL-0179
  - POL-0181
  - POL-0195
  - POL-0240
  - POL-0244
  - POL-0245
  - STD-0010
  - STD-0011
  - STD-0020
applicability:
  language_version: ["20", "23"]
---

# A coroutine that suspends on a device read and resumes with the value

`load_reading` takes its slot as a `std::shared_ptr` by value, so the frame owns a
share of the thing it suspends on and the slot cannot go away underneath it. That is
the whole reason a coroutine parameter is never a reference: a reference argument
outlives nothing, and the frame outlives the call.

Nothing is locked across the `co_await`. There is no lock in this exemplar at all,
which is how the property is carried — no test asserts it, because none could.

`ReadTask` owns one coroutine handle and nothing else, and its five special members
follow from that. It is a concrete type rather than a `Task<T>`, because one return
type is one return type.

### Reading order

- `include/sampler/device/async_read.hpp` — the awaitable's three functions, the
  promise type as a nested type ahead of the constructors, and a coroutine whose
  only parameter is a value
- `device/async_read.cpp` — the handle taken out of the slot before it is resumed,
  and the five special members of a handle owner
- `device/async_read_test.cpp` — resumption observed through the task, the
  already-ready path that never suspends, and the share count showing the frame
  took a copy
- `include/sampler/core/temperature.hpp`, `core/temperature.cpp`,
  `core/temperature_test.cpp` — copied verbatim from EXM-0001

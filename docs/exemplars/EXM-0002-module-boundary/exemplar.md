---
id: EXM-0002
situation: lay out a module's public header, its internal header, and the layer it depends on
demonstrates:
  - POL-0014
  - POL-0017
  - POL-0056
  - POL-0057
  - POL-0058
  - POL-0064
  - POL-0183
  - POL-0217
  - POL-0218
  - POL-0228
  - POL-0240
  - POL-0244
  - POL-0245
  - STD-0001
  - STD-0002
  - STD-0003
  - STD-0004
  - STD-0005
  - STD-0007
  - STD-0008
  - STD-0010
  - STD-0011
applicability:
  language_version: ["20", "23"]
---

# A public header over an internal one, with the layer dependency running one way

`device` reaches into `core` and `core` reaches nowhere. Inside `device`, the
public surface is one header under `include/`, and the endpoint resolution the
registry runs on the way in sits in a header beside its source, where nothing
outside the layer can name it.

`resolve_endpoint` has a header rather than an anonymous namespace because two
translation units use it: the registry and its own test.

### Reading order

- `include/sampler/device/registry.hpp` — what the layer publishes: an aggregate
  with no invariant, and a class whose constructor holds one
- `device/registry_impl.hpp` — the same declaration discipline applied to a name
  that is not published, placed where the include path cannot reach it from
  outside the layer
- `device/registry_impl.cpp` — file-scope constants in an anonymous namespace,
  which is where an entity goes when it has no second translation unit
- `device/registry.cpp` — the four include blocks with the project's own headers
  last, and the uniqueness invariant established over a container
- `device/registry_test.cpp` — the boundary exercised through the public header
  only
- `device/registry_impl_test.cpp` — the internal header's second consumer, which
  is what earns it its file
- `include/sampler/core/device_id.hpp`, `core/device_id.cpp`,
  `core/device_id_test.cpp` — copied verbatim from EXM-0001

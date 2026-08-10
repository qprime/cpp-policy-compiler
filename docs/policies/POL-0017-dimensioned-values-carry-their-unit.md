---
id: POL-0017
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #5"
    upstream: ["CG I.4", "CG NL.19"]
---

# Dimensioned values carry their unit in the name

A value with a physical or conventional dimension states that dimension as a
name suffix: `timeout_ms`, `size_bytes`, `rate_hz`, `angle_deg`, `width_px`. At
every interface, without exception.

The suffix names the unit, not the quantity: `_ms` and not `_time`. A parameter,
a member, a return value, and a constant naming the same quantity all carry the
same suffix, so a conversion is visible as a change of suffix rather than
inferred from arithmetic.

A ratio or a count has no unit and takes none. Where a value genuinely carries
two units, the name carries both in the order they divide: `rate_bytes_per_sec`.

The suffix is not a substitute for a strong type, and it is also not a step
toward one. POL-0038 states when a distinct type earns its cost; below that bar
the suffix is the whole mechanism.

A dimensioned quantity has no compiler-visible dimension, so a millisecond
assigned to a seconds parameter compiles, runs, and produces an answer that is
wrong by three orders of magnitude. Nothing downstream can detect it, because
every value involved is a legal instance of its type. The name is the only place
the unit can live, which is why it is required at the interface rather than
recommended inside it.

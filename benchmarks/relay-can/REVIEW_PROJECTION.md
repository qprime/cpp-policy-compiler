# Relay CAN review projection

This bundle is for review, not generation. Inspect the implementation against
the frozen task and report only observable correctness, invariant, and
review-enforced policy violations.

## Procedure

1. Trace each requirement through task-spec validation, generated ST, the Python
   runtime, resolved host input, the C++ transport, trace serialization, and the
   verifier. A test at one layer is not evidence for another.
2. Reconstruct simulated-time state across scan boundaries. Check simultaneous
   arbitration, non-preemption of an in-flight frame, idle-bus start, queued
   rounds, exact-boundary completion, and deterministic tie-breaking.
3. Compare Python and C++ frame construction field-for-field: base-format data
   bits, CRC-15/CAN coverage, bit stuffing, delimiters, ACK, EOF, and
   intermission. Compare duration arithmetic exactly.
4. Vary PLC/frame declaration order and consider coroutine interleavings. These
   must not change normalized traces or verdicts.
5. Check both validation boundaries, old trace compatibility, tag/address
   behavior, plant isolation, and one-publication/many-consumer sequencing.
6. Separate defects from preferences. Each finding must name a frozen
   requirement or stable identity, precise location, observable consequence,
   and minimal reproducer or repair direction.

## Relevant stable identities

- `POL-0007` — deterministic results are the default.
- `POL-0014` — interfaces state their dependencies.
- `POL-0017` — interfaces take the meaningful type.
- `POL-0236` — units convert at the outer boundary.
- `POL-0240` — test where the logic lives.
- `POL-0246` — structured output is golden-tested.
- `STD-0001`, `STD-0002`, `STD-0003`, `STD-0008` — file, module, namespace,
  and test placement.
- `STD-0010`, `STD-0011`, `STD-0012`, `STD-0013` — semantic naming, return
  contracts, unit suffixes, and scope-proportional names.
- `STD-0016`, `STD-0019`, `STD-0020`, `STD-0022` — const placement, literal
  readability, class layout, and intent-only comments.

## Relay invariants

Inspect `simclock_only_time_source`, `scan_phase_isolation`,
`comm_bus_only_inter_plc_channel`, `pluggable_subsystems`,
`wire_format_serialization`, `verification_path_purity`, and
`host_verification_path_purity` under `docs/invariants/`.

Tool success is supporting evidence only. It does not establish semantic
correctness, cross-runtime equivalence, order independence, or policy
conformance.

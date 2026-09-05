# Relay CAN Invariants

All inter-PLC state crosses CommBus. Scan phases are fixed and isolated. SimClock is
the only time source used for arbitration and delivery. CAN arbitration is logical and
deterministic: the lowest ready standard identifier wins and an active frame cannot be
preempted. Verification remains pure, resolved wire data is validated before use, and
Python remains the authoritative oracle while C++ independently corroborates it.

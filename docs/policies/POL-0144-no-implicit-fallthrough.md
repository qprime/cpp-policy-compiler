---
id: POL-0144
kind: standard
attribution:
  - source: standard-practice
    locator: "switch fallthrough"
    upstream: ["CG ES.78"]
---

# Every `switch` arm ends in a jump, or in `[[fallthrough]]`

End each arm with `break`, `return`, `throw`, or `[[fallthrough]]` where falling
through is intended.

```cpp
switch (motion) {
    case GCodeMotion::ArcCw:
        set_direction(Direction::Clockwise);
        [[fallthrough]];
    case GCodeMotion::ArcCcw:
        emit_arc(move);
        break;
    case GCodeMotion::Linear:
        emit_line(move);
        break;
}
```

An arm that falls through by accident and one that does it on purpose look
identical, so a missing `break` is invisible in review and silently runs the next
case's body. The attribute makes the intent explicit and lets the compiler warn
about the arms that lack it.

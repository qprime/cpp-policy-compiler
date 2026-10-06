---
id: POL-0144
kind: standard
trigger: "end a switch arm"
attribution:
  - source: standard-practice
    locator: "switch fallthrough"
    upstream: ["CG ES.78"]
---

# Every `switch` arm ends in a jump, or in `[[fallthrough]]`

End an arm that executes work with `break`, `return`, `throw`, or an explicit
fallthrough marker where falling through is intended. Stacked labels sharing one
body need no marker. Use standard `[[fallthrough]]` in C++17 and later; in C++14,
use the selected compiler's supported marker or a documented comment recognized
by the project's fallthrough diagnostic.

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

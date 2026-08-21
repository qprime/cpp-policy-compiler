---
id: POL-0194
kind: standard
trigger: "read data from outside the program"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #5"
    upstream: ["CG SL.io.1", "CG SL.io.2"]
---

# Reading from outside the program validates, and reads whole items where it can

Read a line, a record, or a token — not characters — and check the read succeeded
before using what it produced. Reject malformed input at the read site with a
message naming what failed.

```cpp
std::string line;
while (std::getline(input, line)) {
    const auto parsed = parse_move(line);
    if (!parsed) {
        throw ParseError("parse_move: line " + std::to_string(line_no) +
                         " is not a move, got \"" + line + "\"");
    }
    moves.push_back(*parsed);
}
```

An unchecked extraction leaves the target unmodified and the stream in a failed
state, so the loop keeps running on stale values. Character-level input additionally
puts the tokenizing burden on you, which is where the encoding and whitespace bugs
come from.

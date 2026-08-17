---
id: POL-0171
kind: guideline
attribution:
  - source: standard-practice
    locator: "reading input"
    upstream: ["CG SL.io.1"]
---

# Input is read in whole units, not character by character

```cpp
// Avoid. Reassembles a line the library already knows how to read.
std::string line;
for (char c{}; in.get(c) && c != '\n'; ) { line += c; }

// Prefer.
std::string line;
while (std::getline(in, line)) { parse_line(line); }
```

Read a line, a record, or the whole file, and parse from the result. Character
level is for a lexer that genuinely needs one character of lookahead, and there
it works over a buffer already in memory rather than over the stream.

Every read is checked. A stream in a failed state returns without assigning, so
an unchecked read leaves the previous value in place and the loop processes the
same record twice — which is a wrong answer rather than a diagnostic (POL-0002).

Input is the outer boundary, so it is where POL-0005 says validation happens and
where units get converted (POL-0061). Reading in whole units is what makes that
possible: a record is the thing that can be validated, where a character is not.

---
id: POL-0153
kind: standard
attribution:
  - source: standard-practice
    locator: "declaration form"
    upstream: ["CG ES.10", "CG NL.11", "CG NL.18", "CG NL.21", "CG NL.25"]
---

# One name per declaration, written in the C++ form

```cpp
// Never. Only p is a pointer, and the initializers are easy to misread.
int* p, q;
const long timeout = 3600000;
void reset(void);

// Right.
int* p{nullptr};
int q{0};
constexpr auto kTimeoutMs = 3'600'000L;
void reset();
```

The declarator binds to the type, not the name: `int* p` rather than `int *p`,
because the pointer is part of what `p` is. An empty parameter list is written
`()`, never `(void)`, which is the C spelling.

Long numeric literals use digit separators, and a literal whose type matters
carries its suffix — `3'600'000L`, `0.5F`, `1U`. A literal that means something
gets a name instead (POL-0010).

A multi-name declaration distributes the declarator across names unevenly, so
`int* p, q` declares one pointer and one `int` while reading as two pointers. It
also blocks the per-name initialization POL-0096 requires, since the natural
form initializes only the last one, and it makes every later edit that adds a
name inherit whichever declarator happened to be there.

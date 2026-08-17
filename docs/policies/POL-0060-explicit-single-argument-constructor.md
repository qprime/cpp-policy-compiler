---
id: POL-0060
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: value type with invariant"
    upstream: ["CG C.46"]
---

# A single-argument constructor is `explicit`

Write `explicit` on every constructor callable with one argument, including one
with defaults for the rest. Leave it off only where the implicit conversion is the
point of the type.

```cpp
class Feed {
 public:
    explicit Feed(double mm_per_min);
};

void set_feed(Feed feed);
set_feed(Feed{1200.0});
set_feed(1200.0);          // ill-formed, which is what we want
```

Without `explicit`, the constructor becomes an implicit conversion, so any
`double` in the program silently becomes a `Feed` at any call boundary. That
removes exactly the checking the named type was introduced to add.

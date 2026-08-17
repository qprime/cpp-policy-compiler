---
id: POL-0097
kind: standard
attribution:
  - source: standard-practice
    locator: "object slicing"
    upstream: ["CG C.145", "CG C.152", "CG ES.63"]
---

# A polymorphic object is only ever reached through a pointer or reference

Store and pass `std::unique_ptr<Base>`, `Base&`, or `Base*`. Never a `Base` by
value, never a container of `Base`, never an array of derived assigned to a base
pointer.

```cpp
void run(const PostProcessor& post);                       // yes
std::vector<std::unique_ptr<PostProcessor>> posts;         // yes

void run(PostProcessor post);                              // slices
std::vector<PostProcessor> posts;                          // will not compile, and shouldn't
GrblPost posts[4]; PostProcessor* p = posts;               // pointer arithmetic is wrong
```

A by-value base parameter copies the base part and discards the rest, so the
object arrives with the right static type and the wrong behaviour. Base-pointer
arithmetic over derived objects steps by the base's size and lands mid-object.

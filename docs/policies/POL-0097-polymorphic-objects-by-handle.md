---
id: POL-0097
kind: standard
trigger: "declare a variable, container element, or parameter of a polymorphic type"
attribution:
  - source: standard-practice
    locator: "object slicing"
    upstream: ["CG C.145", "CG C.152", "CG ES.63"]
---

# A polymorphic base is passed and stored through a pointer or reference

Store and pass a heterogeneous object as `std::unique_ptr<Base>`, `Base&`, or
`Base*`. Do not pass a derived object through `Base` by value, store heterogeneous
objects in a container of `Base`, or treat an array of derived objects as a base
array. A concrete derived object can still be created and used by value when no
base conversion is involved.

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

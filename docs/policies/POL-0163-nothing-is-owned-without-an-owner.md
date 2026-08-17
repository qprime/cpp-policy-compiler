---
id: POL-0163
kind: standard
attribution:
  - source: standard-practice
    locator: "exception safety, unowned resources"
    upstream: ["CG E.13", "CG E.19"]
---

# No code that can throw runs while holding something nothing will release

```cpp
// Never. If the second allocation throws, the first leaks.
void install(Widget* w) {
    Node* n = new Node(w);
    registry_.add(n);
}

// Right. Owned before anything else can fail.
void install(std::unique_ptr<Widget> w) {
    registry_.add(std::make_unique<Node>(std::move(w)));
}
```

Where the thing to release has no resource-owning type available — a C handle, a
registration that must be undone, a temporary state change — use a scope guard: a
small object whose destructor runs the cleanup, released explicitly on the
success path.

```cpp
auto guard = ScopeExit{[&] { ::freeaddrinfo(info); }};
```

This is POL-0127 stated as an invariant rather than a prohibition. A raw
allocation is one instance of holding something unowned; a file descriptor, a
lock taken by hand, and a half-finished registration are others, and all of them
leak on the same paths.

An exception makes every statement between acquisition and release into an exit
path, including ones nobody wrote. Ownership by a destructor covers all of them
at once, which is why POL-0003 makes it the default rather than a technique.

---
id: STD-0008
group: files-and-layout
enforced_by: review
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# A test lives beside what it tests, named `<unit>_test.cpp`

```
algo/plan_2d.cpp
algo/plan_2d_test.cpp

geom/convex_polygon.cpp
geom/convex_polygon_test.cpp
```

Integration tests, which cross module boundaries, live in `tests/` and are named
for the behaviour rather than for a unit.

Adjacency is what makes a missing test visible: a source file with no neighbour is
the whole report.

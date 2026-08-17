---
id: POL-0113
kind: guideline
attribution:
  - source: standard-practice
    locator: "reference cycles"
    upstream: ["CG R.24"]
---

# Where shared ownership can form a cycle, the back edge is a `weak_ptr`

Pick the direction that is the real ownership and make the other direction
`std::weak_ptr`, locked at the point of use.

```cpp
class Job {
    std::vector<std::shared_ptr<Operation>> operations_;
};

class Operation {
    std::weak_ptr<Job> job_;               // back edge: does not keep Job alive

    void report() {
        if (auto job = job_.lock()) { job->record(*this); }
    }
};
```

Two `shared_ptr`s pointing at each other never reach a refcount of zero, so
neither destructor runs. Nothing reports this — it is a leak that looks like
correct RAII.

Reaching for `weak_ptr` often means the ownership graph is wrong. Check whether one
side can hold a raw reference to a longer-lived owner first.

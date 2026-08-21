---
id: POL-0161
kind: standard
trigger: "allocate on a deadline-bound path"
applicability:
  domain: ["realtime"]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Real-Time Loops"
    upstream: ["CG Per.15"]
---

# A deadline-bound path allocates nothing

Pre-allocate every buffer before the loop starts. Inside it, `push_back`, string
building, and anything reaching `malloc` are defects unless proven otherwise.

```cpp
class ScanLoop {
 public:
    explicit ScanLoop(std::size_t max_events) { trace_.reserve(max_events); }

    void step() {
        if (trace_.size() < trace_.capacity()) { trace_.push_back(sample()); }
    }

 private:
    std::vector<Event> trace_;
};
```

The allocator's worst case is unbounded — it may take a lock, it may call the
kernel — so a single allocation converts a bounded loop into one with no stated
upper bound. A missed deadline in a scan loop or an audio callback is a physical
fault, not a slow frame.

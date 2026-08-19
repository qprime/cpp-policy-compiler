#ifndef SAMPLER_DEVICE_CLOCK_HPP
#define SAMPLER_DEVICE_CLOCK_HPP

#include <chrono>

namespace sampler::device {

class Clock {
 public:
    virtual ~Clock() = default;

    Clock(const Clock&) = delete;
    Clock& operator=(const Clock&) = delete;

    virtual std::chrono::steady_clock::time_point now() const = 0;

 protected:
    Clock() = default;
};

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_CLOCK_HPP

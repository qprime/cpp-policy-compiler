#ifndef SAMPLER_DEVICE_READING_SINK_HPP
#define SAMPLER_DEVICE_READING_SINK_HPP

#include <chrono>

#include "sampler/core/temperature.hpp"

namespace sampler::device {

struct StampedReading {
    std::chrono::steady_clock::time_point taken_at;
    core::Temperature reading;
};

class ReadingSink {
 public:
    virtual ~ReadingSink() = default;

    ReadingSink(const ReadingSink&) = delete;
    ReadingSink& operator=(const ReadingSink&) = delete;

    virtual void write_reading(const StampedReading& stamped) = 0;

 protected:
    ReadingSink() = default;
};

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_READING_SINK_HPP

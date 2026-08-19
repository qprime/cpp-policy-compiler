#ifndef SAMPLER_DEVICE_LATEST_READING_HPP
#define SAMPLER_DEVICE_LATEST_READING_HPP

#include <mutex>
#include <optional>

#include "sampler/core/temperature.hpp"

namespace sampler::device {

// Threading: safe to call from any thread. The mutex below guards the reading and
// nothing else reaches it. A LatestReading starts no threads of its own.
class LatestReading {
 public:
    void write_reading(core::Temperature reading);
    std::optional<core::Temperature> latest() const;

 private:
    mutable std::mutex mutex_;
    std::optional<core::Temperature> reading_;
};

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_LATEST_READING_HPP

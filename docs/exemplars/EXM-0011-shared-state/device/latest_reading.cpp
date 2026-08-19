#include "sampler/device/latest_reading.hpp"

#include <mutex>
#include <optional>

#include "sampler/core/temperature.hpp"

namespace sampler::device {

void LatestReading::write_reading(core::Temperature reading) {
    const std::scoped_lock lock{mutex_};
    reading_ = reading;
}

std::optional<core::Temperature> LatestReading::latest() const {
    const std::scoped_lock lock{mutex_};
    return reading_;
}

}  // namespace sampler::device

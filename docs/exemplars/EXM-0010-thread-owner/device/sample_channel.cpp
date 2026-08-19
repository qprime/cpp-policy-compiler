#include "sampler/device/sample_channel.hpp"

#include <chrono>
#include <cstddef>
#include <mutex>
#include <optional>
#include <stdexcept>

#include "sampler/core/temperature.hpp"

namespace sampler::device {

SampleChannel::SampleChannel(std::size_t capacity) : capacity_{capacity} {
    if (capacity == 0) {
        throw std::invalid_argument("SampleChannel: capacity must be > 0, got 0");
    }
}

bool SampleChannel::try_push(core::Temperature reading) {
    {
        const std::scoped_lock lock{mutex_};
        if (queue_.size() == capacity_) {
            return false;
        }
        queue_.push_back(reading);
    }
    filled_.notify_one();
    return true;
}

std::optional<core::Temperature> SampleChannel::try_pop(std::chrono::milliseconds timeout) {
    std::unique_lock lock{mutex_};
    if (!filled_.wait_for(lock, timeout, [this] { return !queue_.empty(); })) {
        return std::nullopt;
    }
    const core::Temperature reading = queue_.front();
    queue_.pop_front();
    return reading;
}

}  // namespace sampler::device

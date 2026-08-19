#ifndef SAMPLER_DEVICE_SAMPLE_CHANNEL_HPP
#define SAMPLER_DEVICE_SAMPLE_CHANNEL_HPP

#include <chrono>
#include <condition_variable>
#include <cstddef>
#include <deque>
#include <mutex>
#include <optional>

#include "sampler/core/temperature.hpp"

namespace sampler::device {

// Threading: every member is safe to call from any thread. The mutex below guards
// the deque and nothing else reaches it.
class SampleChannel {
 public:
    explicit SampleChannel(std::size_t capacity);

    bool try_push(core::Temperature reading);
    std::optional<core::Temperature> try_pop(std::chrono::milliseconds timeout);

 private:
    std::size_t capacity_;
    std::mutex mutex_;
    std::condition_variable filled_;
    std::deque<core::Temperature> queue_;
};

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_SAMPLE_CHANNEL_HPP

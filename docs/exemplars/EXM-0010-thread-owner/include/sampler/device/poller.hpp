#ifndef SAMPLER_DEVICE_POLLER_HPP
#define SAMPLER_DEVICE_POLLER_HPP

#include <atomic>
#include <condition_variable>
#include <memory>
#include <mutex>
#include <stop_token>
#include <thread>

#include "sampler/core/sample_interval.hpp"
#include "sampler/device/sample_channel.hpp"

namespace sampler::device {

// Threading: a Poller runs one thread of its own and owns everything that thread
// touches. Construct and destroy it from one thread; its channel is safe to drain
// from another.
class Poller {
 public:
    explicit Poller(core::SampleInterval interval);
    ~Poller() = default;

    Poller(const Poller&) = delete;
    Poller& operator=(const Poller&) = delete;
    Poller(Poller&&) = delete;
    Poller& operator=(Poller&&) = delete;

    void stop();

    SampleChannel& channel() { return channel_; }
    std::shared_ptr<const std::atomic<bool>> exit_flag() const { return exited_; }

 private:
    void run(std::stop_token token);

    core::SampleInterval interval_;
    SampleChannel channel_;
    std::shared_ptr<std::atomic<bool>> exited_;
    std::mutex tick_mutex_;
    std::condition_variable_any tick_;
    std::jthread worker_;
};

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_POLLER_HPP

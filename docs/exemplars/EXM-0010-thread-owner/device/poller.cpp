#include "sampler/device/poller.hpp"

#include <atomic>
#include <cstddef>
#include <format>
#include <memory>
#include <mutex>
#include <stop_token>
#include <utility>

#include "sampler/core/log.hpp"
#include "sampler/core/sample_interval.hpp"
#include "sampler/core/temperature.hpp"

namespace sampler::device {
namespace {

constexpr std::size_t kChannelCapacity = 8;
constexpr double kBaseCelsius = 20.0;
constexpr double kStepCelsius = 0.1;

core::Temperature nth_reading(std::size_t index) {
    return core::Temperature{kBaseCelsius + static_cast<double>(index) * kStepCelsius};
}

}  // namespace

Poller::Poller(core::SampleInterval interval)
    : interval_{interval},
      channel_{kChannelCapacity},
      exited_{std::make_shared<std::atomic<bool>>(false)},
      worker_{[this](std::stop_token token) { run(std::move(token)); }} {}

void Poller::stop() {
    if (!worker_.joinable()) {
        return;
    }
    worker_.request_stop();
    worker_.join();
}

void Poller::run(std::stop_token token) {
    core::write_log(core::LogLevel::Info,
                    std::format("Poller: started at {} ms", interval_.period().count()));

    std::size_t produced = 0;
    while (!token.stop_requested()) {
        {
            std::unique_lock lock{tick_mutex_};
            tick_.wait_for(lock, token, interval_.period(),
                           [&token] { return token.stop_requested(); });
        }
        if (token.stop_requested()) {
            continue;
        }
        if (!channel_.try_push(nth_reading(produced))) {
            core::write_log(core::LogLevel::Warn, "Poller: channel is full, dropped a sample");
        }
        ++produced;
    }

    core::write_log(core::LogLevel::Info,
                    std::format("Poller: stopped after {} samples", produced));
    exited_->store(true);
}

}  // namespace sampler::device

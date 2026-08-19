#include "sampler/core/sample_interval.hpp"

#include <chrono>
#include <stdexcept>
#include <string>

namespace sampler::core {
namespace {

constexpr double kMillisecondsPerSecond = 1000.0;

}  // namespace

SampleInterval::SampleInterval(std::chrono::milliseconds period) : period_{period} {
    if (period <= std::chrono::milliseconds::zero()) {
        throw std::invalid_argument("SampleInterval: period_ms must be > 0, got " +
                                    std::to_string(period.count()));
    }
}

double SampleInterval::rate_hz() const {
    return kMillisecondsPerSecond / static_cast<double>(period_.count());
}

}  // namespace sampler::core

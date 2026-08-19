#ifndef SAMPLER_CORE_SAMPLE_INTERVAL_HPP
#define SAMPLER_CORE_SAMPLE_INTERVAL_HPP

#include <chrono>

namespace sampler::core {

class SampleInterval {
 public:
    explicit SampleInterval(std::chrono::milliseconds period);

    std::chrono::milliseconds period() const { return period_; }
    double rate_hz() const;

    friend bool operator==(const SampleInterval&, const SampleInterval&) = default;

 private:
    std::chrono::milliseconds period_;
};

}  // namespace sampler::core

#endif  // SAMPLER_CORE_SAMPLE_INTERVAL_HPP

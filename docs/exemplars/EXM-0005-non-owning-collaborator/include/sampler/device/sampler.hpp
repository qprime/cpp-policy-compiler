#ifndef SAMPLER_DEVICE_SAMPLER_HPP
#define SAMPLER_DEVICE_SAMPLER_HPP

#include "sampler/core/temperature.hpp"
#include "sampler/device/clock.hpp"
#include "sampler/device/reading_sink.hpp"

namespace sampler::device {

// Lifetime: the clock and the sink outlive the Sampler, which owns neither and
// releases neither.
class Sampler {
 public:
    Sampler(const Clock& clock, ReadingSink& sink);

    void write_reading(core::Temperature reading);

 private:
    const Clock* clock_;
    ReadingSink* sink_;
};

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_SAMPLER_HPP

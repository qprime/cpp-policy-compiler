#include "sampler/device/sampler.hpp"

#include "sampler/core/temperature.hpp"
#include "sampler/device/reading_sink.hpp"

namespace sampler::device {

Sampler::Sampler(const Clock& clock, ReadingSink& sink) : clock_{&clock}, sink_{&sink} {}

void Sampler::write_reading(core::Temperature reading) {
    sink_->write_reading(StampedReading{clock_->now(), reading});
}

}  // namespace sampler::device

#ifndef SAMPLER_DEVICE_SAMPLE_LOOP_HPP
#define SAMPLER_DEVICE_SAMPLE_LOOP_HPP

#include <cstddef>
#include <span>
#include <vector>

#include "sampler/core/temperature.hpp"

namespace sampler::device {

// Threading: a SampleLoop is single-threaded. The scan thread constructs it, drives
// it, and reads it; nothing else touches it.
class SampleLoop {
 public:
    explicit SampleLoop(std::size_t capacity);

    void write_scan(std::span<const core::Temperature> scan) noexcept;

    std::span<const core::Temperature> recorded() const noexcept { return recorded_; }
    std::size_t dropped() const noexcept { return dropped_; }

 private:
    std::vector<core::Temperature> recorded_;
    std::size_t dropped_ = 0;
};

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_SAMPLE_LOOP_HPP

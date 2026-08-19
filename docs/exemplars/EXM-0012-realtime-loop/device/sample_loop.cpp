#include "sampler/device/sample_loop.hpp"

#include <cstddef>
#include <span>
#include <stdexcept>

#include "sampler/core/temperature.hpp"

namespace sampler::device {

SampleLoop::SampleLoop(std::size_t capacity) {
    if (capacity == 0) {
        throw std::invalid_argument("SampleLoop: capacity must be > 0, got 0");
    }
    recorded_.reserve(capacity);
}

void SampleLoop::write_scan(std::span<const core::Temperature> scan) noexcept {
    for (const core::Temperature& reading : scan) {
        if (recorded_.size() == recorded_.capacity()) {
            ++dropped_;
            continue;
        }
        recorded_.push_back(reading);
    }
}

}  // namespace sampler::device

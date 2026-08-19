#include "sampler/core/sample_buffer.hpp"

#include <cstddef>
#include <stdexcept>

namespace sampler::core {

SampleBuffer::SampleBuffer(std::size_t capacity) : capacity_{capacity} {
    if (capacity == 0) {
        throw std::invalid_argument("SampleBuffer: capacity must be > 0, got 0");
    }
    readings_.reserve(capacity);
}

void SampleBuffer::push_back(Temperature reading) {
    if (is_full()) {
        readings_.erase(readings_.begin());
    }
    readings_.push_back(reading);
}

}  // namespace sampler::core

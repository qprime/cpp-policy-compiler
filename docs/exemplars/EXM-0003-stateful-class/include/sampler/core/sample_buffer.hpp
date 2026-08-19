#ifndef SAMPLER_CORE_SAMPLE_BUFFER_HPP
#define SAMPLER_CORE_SAMPLE_BUFFER_HPP

#include <cstddef>
#include <vector>

#include "sampler/core/temperature.hpp"

namespace sampler::core {

class SampleBuffer {
 public:
    using value_type = Temperature;

    explicit SampleBuffer(std::size_t capacity);

    void push_back(Temperature reading);

    const std::vector<Temperature>& readings() const { return readings_; }
    std::size_t capacity() const { return capacity_; }
    std::size_t size() const { return readings_.size(); }
    bool is_empty() const { return readings_.empty(); }
    bool is_full() const { return readings_.size() == capacity_; }

 private:
    std::size_t capacity_;
    std::vector<Temperature> readings_;
};

}  // namespace sampler::core

#endif  // SAMPLER_CORE_SAMPLE_BUFFER_HPP

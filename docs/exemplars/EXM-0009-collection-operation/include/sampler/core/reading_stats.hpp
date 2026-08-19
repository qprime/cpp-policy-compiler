#ifndef SAMPLER_CORE_READING_STATS_HPP
#define SAMPLER_CORE_READING_STATS_HPP

#include <optional>
#include <span>

#include "sampler/core/temperature.hpp"

namespace sampler::core {

class SampleWindow {
 public:
    SampleWindow(double lowest_celsius, double highest_celsius);

    bool contains(double celsius) const {
        return celsius >= lowest_celsius_ && celsius <= highest_celsius_;
    }

 private:
    double lowest_celsius_;
    double highest_celsius_;
};

std::optional<Temperature> try_mean_temperature(std::span<const Temperature> readings,
                                                const SampleWindow& window);

}  // namespace sampler::core

#endif  // SAMPLER_CORE_READING_STATS_HPP

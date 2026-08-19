#ifndef SAMPLER_CORE_CALIBRATION_HPP
#define SAMPLER_CORE_CALIBRATION_HPP

#include <optional>
#include <span>

#include "sampler/core/temperature.hpp"

namespace sampler::core {

constexpr double kMaxStableSpreadCelsius = 0.5;

class Calibration {
 public:
    Calibration(double offset_celsius, double scale);

    double offset_celsius() const { return offset_celsius_; }
    double scale() const { return scale_; }

 private:
    double offset_celsius_;
    double scale_;
};

std::optional<Temperature> try_calibrated_temperature(std::span<const double> samples_celsius,
                                                      const Calibration& calibration);

}  // namespace sampler::core

#endif  // SAMPLER_CORE_CALIBRATION_HPP

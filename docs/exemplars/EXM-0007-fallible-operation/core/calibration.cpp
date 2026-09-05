#include "sampler/core/calibration.hpp"

#include <algorithm>
#include <cassert>
#include <cmath>
#include <numeric>
#include <optional>
#include <span>
#include <stdexcept>
#include <string>

#include "sampler/core/temperature.hpp"

namespace sampler::core {
namespace {

double mean_celsius(std::span<const double> samples_celsius) {
    const double total = std::accumulate(samples_celsius.begin(), samples_celsius.end(), 0.0);
    return total / static_cast<double>(samples_celsius.size());
}

double spread_celsius(std::span<const double> samples_celsius) {
    const auto bounds = std::ranges::minmax(samples_celsius);
    return bounds.max - bounds.min;
}

}  // namespace

Calibration::Calibration(double offset_celsius, double scale)
    : offset_celsius_{offset_celsius}, scale_{scale} {
    if (!std::isfinite(offset_celsius)) {
        throw std::invalid_argument("Calibration: offset_celsius must be finite");
    }
    if (!std::isfinite(scale) || scale <= 0.0) {
        throw std::invalid_argument("Calibration: scale must be finite and > 0, got " +
                                    std::to_string(scale));
    }
}

std::optional<Temperature> try_calibrated_temperature(std::span<const double> samples_celsius,
                                                      const Calibration& calibration) {
    assert(!samples_celsius.empty());

    if (spread_celsius(samples_celsius) > kMaxStableSpreadCelsius) {
        return std::nullopt;
    }
    return Temperature::try_from(mean_celsius(samples_celsius) * calibration.scale() +
                                 calibration.offset_celsius());
}

}  // namespace sampler::core

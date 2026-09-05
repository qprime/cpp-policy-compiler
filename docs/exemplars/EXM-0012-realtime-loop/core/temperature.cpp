#include "sampler/core/temperature.hpp"

#include <cmath>
#include <optional>
#include <stdexcept>
#include <string>

namespace sampler::core {
namespace {

bool is_valid_temperature(double celsius) {
    return std::isfinite(celsius) && celsius >= kAbsoluteZeroCelsius;
}

}  // namespace

Temperature::Temperature(double celsius) : celsius_{celsius} {
    if (!is_valid_temperature(celsius)) {
        throw std::invalid_argument("Temperature: celsius must be finite and >= -273.15, got " +
                                    std::to_string(celsius));
    }
}

std::optional<Temperature> Temperature::try_from(double celsius) {
    if (!is_valid_temperature(celsius)) {
        return std::nullopt;
    }
    return Temperature{celsius};
}

}  // namespace sampler::core

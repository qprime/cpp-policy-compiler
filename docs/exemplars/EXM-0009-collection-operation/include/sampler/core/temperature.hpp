#ifndef SAMPLER_CORE_TEMPERATURE_HPP
#define SAMPLER_CORE_TEMPERATURE_HPP

#include <optional>

namespace sampler::core {

constexpr double kAbsoluteZeroCelsius = -273.15;

class Temperature {
 public:
    explicit Temperature(double celsius);

    static std::optional<Temperature> try_from(double celsius);

    double celsius() const { return celsius_; }
    double kelvin() const { return celsius_ - kAbsoluteZeroCelsius; }

    friend bool operator==(const Temperature&, const Temperature&) = default;

 private:
    double celsius_;
};

}  // namespace sampler::core

#endif  // SAMPLER_CORE_TEMPERATURE_HPP

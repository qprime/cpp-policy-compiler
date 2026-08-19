#ifndef SAMPLER_CORE_DEVICE_STATE_HPP
#define SAMPLER_CORE_DEVICE_STATE_HPP

#include <chrono>
#include <string>
#include <string_view>
#include <variant>

namespace sampler::core {

struct Offline {};

struct Idle {};

struct Sampling {
    std::chrono::milliseconds period;
};

struct Faulted {
    std::string last_error;
};

using DeviceState = std::variant<Offline, Idle, Sampling, Faulted>;

enum class Health { Offline, Healthy, Faulted };

Health state_to_health(const DeviceState& state);

std::string format_state(const DeviceState& state);

std::string_view format_health(Health health);

}  // namespace sampler::core

#endif  // SAMPLER_CORE_DEVICE_STATE_HPP

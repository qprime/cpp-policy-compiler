#include "sampler/core/device_state.hpp"

#include <stdexcept>
#include <string>
#include <string_view>
#include <variant>

namespace sampler::core {
namespace {

template <class... Handlers>
struct Overloaded : Handlers... {
    using Handlers::operator()...;
};

template <class... Handlers>
Overloaded(Handlers...) -> Overloaded<Handlers...>;

}  // namespace

Health state_to_health(const DeviceState& state) {
    return std::visit(Overloaded{
                          [](const Offline&) { return Health::Offline; },
                          [](const Idle&) { return Health::Healthy; },
                          [](const Sampling&) { return Health::Healthy; },
                          [](const Faulted&) { return Health::Faulted; },
                      },
                      state);
}

std::string format_state(const DeviceState& state) {
    return std::visit(
        Overloaded{
            [](const Offline&) { return std::string{"offline"}; },
            [](const Idle&) { return std::string{"idle"}; },
            [](const Sampling& sampling) {
                return "sampling every " + std::to_string(sampling.period.count()) + " ms";
            },
            [](const Faulted& faulted) { return "faulted: " + faulted.last_error; },
        },
        state);
}

std::string_view format_health(Health health) {
    switch (health) {
        case Health::Offline:
            return "offline";
        case Health::Healthy:
            return "healthy";
        case Health::Faulted:
            return "faulted";
    }
    throw std::logic_error("format_health: health must be a declared enumerator, got " +
                           std::to_string(static_cast<int>(health)));
}

}  // namespace sampler::core

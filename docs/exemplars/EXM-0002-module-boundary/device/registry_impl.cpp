#include "device/registry_impl.hpp"

#include <stdexcept>
#include <string>
#include <string_view>

namespace sampler::device {
namespace {

constexpr std::string_view kSchemePrefix = "tcp://";
constexpr int kDefaultPort = 9000;

}  // namespace

std::string resolve_endpoint(std::string_view endpoint) {
    if (endpoint.empty()) {
        throw std::invalid_argument("Registry: endpoint must be non-empty, got \"\"");
    }
    if (endpoint.starts_with(kSchemePrefix)) {
        return std::string{endpoint};
    }
    return std::string{kSchemePrefix} + std::string{endpoint} + ":" + std::to_string(kDefaultPort);
}

}  // namespace sampler::device

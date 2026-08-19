#ifndef SAMPLER_DEVICE_REGISTRY_IMPL_HPP
#define SAMPLER_DEVICE_REGISTRY_IMPL_HPP

#include <string>
#include <string_view>

namespace sampler::device {

std::string resolve_endpoint(std::string_view endpoint);

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_REGISTRY_IMPL_HPP

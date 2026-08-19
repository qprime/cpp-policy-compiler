#ifndef SAMPLER_DEVICE_REGISTRY_HPP
#define SAMPLER_DEVICE_REGISTRY_HPP

#include <cstddef>
#include <map>
#include <optional>
#include <string>
#include <vector>

#include "sampler/core/device_id.hpp"

namespace sampler::device {

struct Registration {
    core::DeviceId id;
    std::string endpoint;
};

class Registry {
 public:
    explicit Registry(const std::vector<Registration>& declared);

    std::optional<Registration> find_device(const core::DeviceId& id) const;
    std::size_t size() const;

 private:
    std::map<core::DeviceId, Registration> by_id_;
};

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_REGISTRY_HPP

#include "sampler/device/registry.hpp"

#include <cstddef>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

#include "device/registry_impl.hpp"

namespace sampler::device {

Registry::Registry(const std::vector<Registration>& declared) {
    for (const Registration& registration : declared) {
        const Registration resolved{registration.id, resolve_endpoint(registration.endpoint)};
        const bool inserted = by_id_.emplace(registration.id, resolved).second;
        if (!inserted) {
            throw std::invalid_argument("Registry: id must be unique, got \"" +
                                        std::string{registration.id.text()} + "\"");
        }
    }
}

std::optional<Registration> Registry::find_device(const core::DeviceId& id) const {
    const auto found = by_id_.find(id);
    if (found == by_id_.end()) {
        return std::nullopt;
    }
    return found->second;
}

std::size_t Registry::size() const { return by_id_.size(); }

}  // namespace sampler::device

#include "sampler/device/registry.hpp"

#include <optional>
#include <stdexcept>
#include <vector>

#include <catch2/catch_test_macros.hpp>

#include "sampler/core/device_id.hpp"

namespace sampler::device {

TEST_CASE("finds_registered_device") {
    const Registry registry{{Registration{core::DeviceId{"probe-a"}, "tcp://10.0.0.4:9000"}}};

    const std::optional<Registration> found = registry.find_device(core::DeviceId{"probe-a"});

    REQUIRE(found.has_value());
    REQUIRE(found->endpoint == "tcp://10.0.0.4:9000");
}

TEST_CASE("reports_absent_device") {
    const Registry registry{{Registration{core::DeviceId{"probe-a"}, "tcp://10.0.0.4:9000"}}};

    REQUIRE(registry.find_device(core::DeviceId{"probe-b"}) == std::nullopt);
}

TEST_CASE("resolves_a_shorthand_endpoint_on_the_way_in") {
    const Registry registry{{Registration{core::DeviceId{"probe-a"}, "10.0.0.4"}}};

    REQUIRE(registry.find_device(core::DeviceId{"probe-a"})->endpoint == "tcp://10.0.0.4:9000");
}

TEST_CASE("rejects_a_duplicate_id") {
    const std::vector<Registration> declared{
        Registration{core::DeviceId{"probe-a"}, "10.0.0.4"},
        Registration{core::DeviceId{"probe-a"}, "10.0.0.5"},
    };

    REQUIRE_THROWS_AS(Registry{declared}, std::invalid_argument);
}

}  // namespace sampler::device

#include "sampler/core/device_id.hpp"

#include <stdexcept>

#include <catch2/catch_test_macros.hpp>

namespace sampler::core {

TEST_CASE("rejects_empty_identifier") {
    REQUIRE_THROWS_AS(DeviceId{""}, std::invalid_argument);
}

TEST_CASE("distinct_ids_do_not_compare_equal") {
    REQUIRE(DeviceId{"probe-a"} != DeviceId{"probe-b"});
    REQUIRE(DeviceId{"probe-a"} == DeviceId{"probe-a"});
}

TEST_CASE("orders_ids_by_text") {
    REQUIRE(DeviceId{"probe-a"} < DeviceId{"probe-b"});
}

}  // namespace sampler::core

#include "device/registry_impl.hpp"

#include <stdexcept>

#include <catch2/catch_test_macros.hpp>

namespace sampler::device {

TEST_CASE("expands_a_bare_host_to_the_default_endpoint") {
    REQUIRE(resolve_endpoint("10.0.0.4") == "tcp://10.0.0.4:9000");
}

TEST_CASE("leaves_a_full_endpoint_unchanged") {
    REQUIRE(resolve_endpoint("tcp://10.0.0.4:9100") == "tcp://10.0.0.4:9100");
}

TEST_CASE("rejects_an_empty_endpoint") {
    REQUIRE_THROWS_AS(resolve_endpoint(""), std::invalid_argument);
}

}  // namespace sampler::device

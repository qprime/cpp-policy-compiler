#include "sampler/device/device_file.hpp"

#include <stdexcept>
#include <utility>

#include <catch2/catch_test_macros.hpp>
#include <fcntl.h>

namespace sampler::device {
namespace {

bool is_open(int descriptor) { return ::fcntl(descriptor, F_GETFD) != -1; }

}  // namespace

TEST_CASE("acquisition_failure_throws") {
    REQUIRE_THROWS_AS(DeviceFile{"/dev/no-such-sampler-device"}, std::runtime_error);
}

TEST_CASE("moved_from_handle_closes_nothing") {
    DeviceFile owner{"/dev/null"};
    int descriptor = -1;
    {
        DeviceFile source{"/dev/null"};
        descriptor = source.descriptor();
        owner = std::move(source);
    }

    REQUIRE(owner.descriptor() == descriptor);
    REQUIRE(is_open(descriptor));
}

TEST_CASE("destruction_releases_the_descriptor") {
    int descriptor = -1;
    {
        const DeviceFile file{"/dev/null"};
        descriptor = file.descriptor();
        REQUIRE(is_open(descriptor));
    }

    REQUIRE_FALSE(is_open(descriptor));
}

}  // namespace sampler::device

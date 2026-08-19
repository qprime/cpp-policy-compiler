#include "sampler/ffi/driver_adapter.hpp"

#include <cassert>
#include <expected>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>

#include <catch2/catch_approx.hpp>
#include <catch2/catch_test_macros.hpp>

#include "sampler/core/temperature.hpp"
#include "sampler/ffi/driver.h"

struct sampler_driver_session {
    double celsius;
};

namespace {

struct FakeDriver {
    int opens = 0;
    int closes = 0;
    double celsius = 21.0;
    sampler_driver_status read_status = SAMPLER_DRIVER_OK;
};

// The C signatures carry no context parameter, so a fake implementation of them has
// nowhere to keep its counters. One function-local static, named, is the whole
// exception.
FakeDriver& fake_driver() {
    static FakeDriver driver;
    return driver;
}

sampler_driver_session& fake_session() {
    static sampler_driver_session session{};
    return session;
}

}  // namespace

extern "C" sampler_driver_status sampler_driver_open(const char* endpoint,
                                                     sampler_driver_session** out_session) {
    assert(endpoint != nullptr);
    assert(out_session != nullptr);

    if (std::string_view{endpoint}.empty()) {
        return SAMPLER_DRIVER_NOT_FOUND;
    }

    FakeDriver& driver = fake_driver();
    ++driver.opens;
    fake_session().celsius = driver.celsius;
    *out_session = &fake_session();
    return SAMPLER_DRIVER_OK;
}

extern "C" void sampler_driver_close(sampler_driver_session* session) {
    assert(session != nullptr);
    ++fake_driver().closes;
}

extern "C" sampler_driver_status sampler_driver_read(sampler_driver_session* session,
                                                     double* out_celsius) {
    assert(session != nullptr);
    assert(out_celsius != nullptr);

    const FakeDriver& driver = fake_driver();
    if (driver.read_status != SAMPLER_DRIVER_OK) {
        return driver.read_status;
    }
    *out_celsius = session->celsius;
    return SAMPLER_DRIVER_OK;
}

namespace sampler::ffi {
namespace {

constexpr std::string_view kGoldenPath = "ffi/testdata/frame.golden";
constexpr std::string_view kEndpoint = "tcp://10.0.0.4:9000";

std::string load_golden(std::string_view path) {
    std::ifstream input{std::string{path}};
    if (!input) {
        throw std::runtime_error("load_golden: path must name a readable golden, got \"" +
                                 std::string{path} + "\"");
    }
    std::ostringstream contents;
    contents << input.rdbuf();
    return contents.str();
}

}  // namespace

TEST_CASE("translates_foreign_error_codes") {
    REQUIRE(status_to_failure(SAMPLER_DRIVER_NOT_FOUND) == DriverFailure::NotFound);
    REQUIRE(status_to_failure(SAMPLER_DRIVER_BUSY) == DriverFailure::Busy);
    REQUIRE(status_to_failure(SAMPLER_DRIVER_FAULT) == DriverFailure::Fault);
    REQUIRE_THROWS_AS(status_to_failure(SAMPLER_DRIVER_OK), std::logic_error);
}

TEST_CASE("acquisition_failure_throws_a_domain_error") {
    REQUIRE_THROWS_AS(DriverSession{""}, DriverError);
}

TEST_CASE("releases_every_driver_allocation") {
    const int opens_before = fake_driver().opens;
    const int closes_before = fake_driver().closes;
    {
        const DriverSession session{std::string{kEndpoint}};
        REQUIRE(session.try_read()->celsius() == Catch::Approx(21.0));
    }

    REQUIRE(fake_driver().opens == opens_before + 1);
    REQUIRE(fake_driver().closes == closes_before + 1);
}

TEST_CASE("a_moved_from_session_releases_nothing") {
    const int closes_before = fake_driver().closes;
    {
        DriverSession source{std::string{kEndpoint}};
        const DriverSession target{std::move(source)};
    }

    REQUIRE(fake_driver().closes == closes_before + 1);
}

TEST_CASE("reports_a_read_failure_as_a_domain_failure") {
    const DriverSession session{std::string{kEndpoint}};
    fake_driver().read_status = SAMPLER_DRIVER_BUSY;

    const std::expected<core::Temperature, DriverFailure> reading = session.try_read();
    fake_driver().read_status = SAMPLER_DRIVER_OK;

    REQUIRE_FALSE(reading.has_value());
    REQUIRE(reading.error() == DriverFailure::Busy);
}

TEST_CASE("serialized_frame_matches_golden") {
    std::string produced;
    produced += format_frame(1, core::Temperature{20.0}) + '\n';
    produced += format_frame(2, core::Temperature{20.5}) + '\n';
    produced += format_frame(3, core::Temperature{-12.25}) + '\n';

    REQUIRE(produced == load_golden(kGoldenPath));
}

}  // namespace sampler::ffi

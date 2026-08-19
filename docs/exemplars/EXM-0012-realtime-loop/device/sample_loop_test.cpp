#include "sampler/device/sample_loop.hpp"

#include <array>
#include <atomic>
#include <cstddef>
#include <cstdlib>
#include <new>
#include <stdexcept>

#include <catch2/catch_test_macros.hpp>

#include "sampler/core/temperature.hpp"

namespace {

// Replacing the global allocator is what makes the no-allocation claim observable.
// The counter is a global because the replacement signatures take no context, and
// `malloc` is correct here because this function is the one that defines what `new`
// means for this binary.
std::atomic<std::size_t> g_allocation_count{0};

}  // namespace

void* operator new(std::size_t bytes) {
    g_allocation_count.fetch_add(1);
    void* const storage = std::malloc(bytes);
    if (storage == nullptr) {
        throw std::bad_alloc{};
    }
    return storage;
}

void operator delete(void* storage) noexcept { std::free(storage); }

void operator delete(void* storage, std::size_t) noexcept { std::free(storage); }

namespace sampler::device {
namespace {

constexpr std::size_t kCapacity = 4;

std::array<core::Temperature, 3> make_scan() {
    return {core::Temperature{20.0}, core::Temperature{20.5}, core::Temperature{21.0}};
}

}  // namespace

TEST_CASE("rejects_a_zero_capacity") {
    REQUIRE_THROWS_AS(SampleLoop{0}, std::invalid_argument);
}

TEST_CASE("loop_body_does_not_allocate_on_the_sampled_path") {
    SampleLoop loop{kCapacity};
    const std::array<core::Temperature, 3> scan = make_scan();

    const std::size_t before = g_allocation_count.load();
    loop.write_scan(scan);
    const std::size_t after = g_allocation_count.load();

    REQUIRE(after == before);
}

TEST_CASE("records_every_reading_that_fits") {
    SampleLoop loop{kCapacity};
    const std::array<core::Temperature, 3> scan = make_scan();

    loop.write_scan(scan);

    REQUIRE(loop.recorded().size() == 3);
    REQUIRE(loop.recorded()[0] == core::Temperature{20.0});
    REQUIRE(loop.recorded()[2] == core::Temperature{21.0});
}

TEST_CASE("counts_what_did_not_fit_instead_of_growing") {
    SampleLoop loop{2};
    const std::array<core::Temperature, 3> scan = make_scan();

    loop.write_scan(scan);

    REQUIRE(loop.recorded().size() == 2);
    REQUIRE(loop.dropped() == 1);
}

}  // namespace sampler::device

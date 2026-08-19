#include "sampler/device/sampler.hpp"

#include <chrono>
#include <vector>

#include <catch2/catch_test_macros.hpp>

#include "sampler/core/temperature.hpp"
#include "sampler/device/clock.hpp"
#include "sampler/device/reading_sink.hpp"

namespace sampler::device {
namespace {

class FixedClock final : public Clock {
 public:
    explicit FixedClock(std::chrono::steady_clock::time_point at) : at_{at} {}

    std::chrono::steady_clock::time_point now() const override { return at_; }

 private:
    std::chrono::steady_clock::time_point at_;
};

class RecordingSink final : public ReadingSink {
 public:
    void write_reading(const StampedReading& stamped) override { written_.push_back(stamped); }

    const std::vector<StampedReading>& written() const { return written_; }

 private:
    std::vector<StampedReading> written_;
};

constexpr std::chrono::steady_clock::time_point kTakenAt{std::chrono::seconds{42}};

}  // namespace

TEST_CASE("writes_each_reading_to_the_sink") {
    const FixedClock clock{kTakenAt};
    RecordingSink sink;
    Sampler sampler{clock, sink};

    sampler.write_reading(core::Temperature{20.0});
    sampler.write_reading(core::Temperature{21.0});

    REQUIRE(sink.written().size() == 2);
    REQUIRE(sink.written()[0].reading == core::Temperature{20.0});
    REQUIRE(sink.written()[1].reading == core::Temperature{21.0});
}

TEST_CASE("stamps_each_reading_with_the_clock") {
    const FixedClock clock{kTakenAt};
    RecordingSink sink;
    Sampler sampler{clock, sink};

    sampler.write_reading(core::Temperature{20.0});

    REQUIRE(sink.written()[0].taken_at == kTakenAt);
}

TEST_CASE("destruction_leaves_the_sink_untouched") {
    const FixedClock clock{kTakenAt};
    RecordingSink sink;
    {
        Sampler sampler{clock, sink};
        sampler.write_reading(core::Temperature{20.0});
    }

    REQUIRE(sink.written().size() == 1);
}

}  // namespace sampler::device

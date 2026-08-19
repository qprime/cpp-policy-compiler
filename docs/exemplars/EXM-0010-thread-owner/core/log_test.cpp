#include "sampler/core/log.hpp"

#include <iostream>
#include <sstream>
#include <streambuf>

#include <catch2/catch_test_macros.hpp>

namespace sampler::core {
namespace {

class CapturedLog {
 public:
    CapturedLog() : previous_{std::clog.rdbuf(captured_.rdbuf())} {}
    ~CapturedLog() { std::clog.rdbuf(previous_); }

    CapturedLog(const CapturedLog&) = delete;
    CapturedLog& operator=(const CapturedLog&) = delete;
    CapturedLog(CapturedLog&&) = delete;
    CapturedLog& operator=(CapturedLog&&) = delete;

    std::string text() const { return captured_.str(); }

 private:
    std::ostringstream captured_;
    std::streambuf* previous_;
};

}  // namespace

TEST_CASE("writes_the_level_and_the_message") {
    const CapturedLog captured;

    write_log(LogLevel::Warn, "Poller: channel is full, dropped a sample");

    REQUIRE(captured.text() == "WARN Poller: channel is full, dropped a sample\n");
}

}  // namespace sampler::core

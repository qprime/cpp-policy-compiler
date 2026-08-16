---
name: cpp23-gcc-realtime
language_version: 23
compiler: gcc
domain: realtime
---

# cpp23-gcc-realtime

The first realtime configuration, written for relay's C++ deployment host:
C++23 on gcc, scan-cycle code paced by the wall clock. The realtime domain
includes POL-0012 and POL-0076 through POL-0079, so all fifteen topics
render and nothing is excluded.

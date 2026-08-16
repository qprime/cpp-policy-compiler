---
name: cpp20-gcc-application
language_version: 20
compiler: gcc
domain: application
budgets:
  entry_chars: 10000
  topic_chars: 20000
---

# cpp20-gcc-application

The first projection configuration: C++20 on gcc, application domain. Chosen
so the Coroutines topic renders non-vacuously and the realtime domain gate
exercises exclusion. Budget numbers derive from measuring the corpus
(2026-08-15 ruling: numbers live in configuration, revisable): Tier 1 renders
at roughly 7,000 characters against a 10,000 budget, and the largest topic at
roughly 17,000 against 20,000.

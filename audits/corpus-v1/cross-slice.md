# Cross-slice findings

Record findings here when resolution belongs to another audit slice. Every row
must eventually link to a correction or state the accepted rationale.

| Finding | Reporter | Owner | Severity | Status | Resolution |
|---|---|---|---|---|---|
| Shared `Temperature` source admitted positive infinity despite claiming a validated domain value. | final integration | exemplars/integration | major | resolved | All 11 copies now require finite values and carry a non-finite regression test. |
| EXM-0007's `try_` operation could throw for an out-of-domain computed result. | final integration | exemplars/integration | major | resolved | The computed value now passes through `Temperature::try_from`, and the test covers absence. |
| EXM-0013 asserted pointer preconditions inside independently callable public C functions. | final integration | exemplars/integration | major | resolved | The C boundary now rejects invalid pointers and the test calls those failure paths. |
| EXM-0014 retained a continuation after an unfinished coroutine task destroyed its frame. | final integration | exemplars/integration | major | resolved | Task destruction unregisters the continuation before destroying the frame, with a cancellation regression test. |


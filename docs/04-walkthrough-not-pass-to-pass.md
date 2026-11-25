# Walkthrough: NOT_PASS, correction, PASS

One real run, anonymized. Timings, counts and outcomes are copied from the job receipts and verdicts of **run A**
(audit row K117, 30 October 2026, UTC). What the code does is deliberately generic: *a guard that must make the
whole run fail when a record has no identity field.* The original files, names and messages belong to a private
codebase and are not reproduced.

## The shape of the run

```
planner  ->  builder  ->  checker (RED on baseline, GREEN on candidate)  ->  reviewer
                                                                              |
                                              NOT_PASS: one blocker + exact fix text
                                                                              v
          builder (applies the fix)  ->  checker (again)  ->  reviewer (rechecks)  ->  PASS
                                                                              |
                                                       publisher: code commit, then closure commit
```

## Timeline (UTC, from the job receipts)

| Time | Role | Job | Result |
|---|---|---|---|
| 18:31:56 to 18:39:07 | Preparer | writes the contract for the row (7.2 min) | contract with claims, allowlist, RED/GREEN commands |
| 18:40:35 to 18:43:32 | Builder | round 1 build (3.0 min) | handover, paraphrased: built in the allowlisted files; shell access was denied, so the RED and GREEN commands were **not** run by the builder and must be run before any PASS |
| after the build | Checker | 5 verify jobs (31 s in total) | candidate GREEN: 3 passed. Baseline RED as required: guard tests 2 failed, wiring test 1 failed. Regression set 2 passed on both |
| 18:47:20 to 19:03:08 | Reviewer | round 1 review (15.8 min) | **NOT_PASS**, one blocker |
| 19:09:07 to 19:10:46 | Builder | round 2: applies the fix request (1.6 min) | handover, paraphrased: rebuilt on the same base with the fix applied; again no shell, so the checker must supply the commands on these bytes |
| after the build | Checker | 5 verify jobs again (25 s in total) | candidate GREEN: **9 passed**. Baseline RED: guard tests **8 failed**, wiring test 1 failed. Regression set 2 passed |
| 19:14:26 to 19:22:06 | Reviewer | round 2 recheck (7.7 min) | **PASS**, no blockers |
| after the recheck | Publisher | two deterministic commits | code commit, then closure commit, anchor check `[AUDIT_ANCHOR_OK]` |

Wall clock from the planner's start to the reviewer's last job: 50.2 minutes. Agent job time (preparer, builder,
reviewer): 35.2 minutes. The checker's jobs add 55.9 seconds.

## The interesting part: round 1 was green and wrong

After round 1 the checker reported exactly what a builder hopes for. The new tests failed on the old code (RED)
and passed on the new code (GREEN). Nothing in the machine's evidence was red.

The reviewer still returned NOT_PASS, with this blocker (class `failure-record`), paraphrased:

> The guard does raise, as required. But its error message omits three of the four fields the contract demands,
> and the new tests assert that incomplete message. So the tests prove the code matches *itself*, not the
> contract. None of six representations of "missing" can produce the required message.

Why the builder could not have caught this alone: the builder had no shell, and even a builder with one would
have seen green. The tests were written by the same agent as the code, from the same misreading of the contract.
A green result only proves what it ran. The reviewer's job is to compare that green result with what the
contract *required*.

The reviewer did not just object. It followed the rule that a blocker carries **evidence and the exact fix**:

1. the diff lines that raise and the lines that match the weak message,
2. the contract lines that state the required message,
3. the manifest entry showing the GREEN run exited 0 (so the green run is part of the proof, not an excuse),
4. the exact replacement text for the function, one comment, and the whole test file.

The machine copied that fix text unchanged into the next round's fix request. For this run, and for run C, I
compared the fix text in the round-1 verdict with the fix text in the round-2 fix request: they are identical.
The reviewer never edited a file. Nobody paraphrased the fix on its way to the builder.

## Round 2: what changed

* The builder applied the fix: the corrected message with all four fields, a changed comment, and a rewritten
  test file that checks the message and covers all six representations of "missing".
* The test set grew from 3 to 9 tests. On the old code, 8 of the 9 fail, so the tests are sensitive to the
  guard, not just present.
* The same reviewer role rechecked only what was new: the worktree hashes matched the candidate manifest, the
  diff against the base touched only the three allowlisted files, the guard sits before any output is written,
  and the contract's message is now what the code raises. It re-ran the candidate's GREEN and the regression
  set, and confirmed the baseline still fails the RED commands. PASS.

## What the reviewer left non-blocking

One residual was named and left alone: a related code path outside the contract's scope that a reader might
also want hardened. A residual has to name its exact correction or say why it is no weakness, and it stops
nothing. This keeps a reviewer from turning every observation into a blocker.

## The second case, briefly (run C, row K97)

Same loop, different failure. Round 1 was NOT_PASS with the class `CONTRACT_TEST_COVERAGE`: the contract
required a property to hold for every input size from 1 to 12, and the delivered test iterated a table that
only covered 0 to 8. The reviewer's fix was a small extension of the table plus the instruction to bind fresh
evidence to the corrected bytes. Round 2: PASS, with all five mutation probes failing as they should and the
unmutated control passing.

Two different blockers, found by the same mechanism: **compare the result with the requirement, not with the
tests.**

# How the method improves

The method is changed by evidence about its own failures, not by taste. Five mechanisms do the work; each
says where it is recorded.

## 1. The session digest

At the end of a session a protocol writes one frozen digest from the transcript and the git history. Its blocks
are fixed: the decisions and agreements of the session (each with where it now lives, or the words *no home*),
the orchestrator's own mistakes (each with who caught it and how it was fixed), the lessons, the findings and the
hand-over, and what carried over from the previous digest. The next session starts from files, not from
anyone's memory of the last one. A digest also lists what it left out and why, and which of its figures were
counted and which were not re-derived from the transcript.

## 2. The correction budget

A digest's lessons list the rules that were broken again. A rule that appears twice in a row is not allowed to
stay as it is: its cause is fixed, or it is removed from the active rules, and the two independent models
answer the question each alone. The digest also splits each count into breaks that were stopped before they left
the writer's turn (by a hook, the interpreter or the writer's own read-back) and breaks that left it. In the
digest of one three-hour session the repeated breaks were visible as a short list, which is the point of it.

## 3. The gate ledger

Every gate is measured from the receipts and transcripts: the real errors it caught, the false stops (a correct
action refused and redone with only its form changed), and whether it has a test that can fall. The first
ledger covered 27 gates and 662 transcripts since 28 September 2026. Its purpose is to make visible which gates
earn their place and which only stop correct work.

## 4. Reminders replaced by checks that can fail

An early version reminded the agent of its rules at every message. Those per-message reminders were removed on
1 November 2026 and no longer reach any session. What remains is a gate that asks, at the end of a turn that
claims to be finished, which exact command would have failed if the work were wrong, and whether it was run. The
gate's own message states the measurement it rests on: 31 defects were found by an exit code and none by a
reminder text. It fired while this repository was being built, and the answer was a command that could fail.

## 5. Rule changes are themselves reviewed

A change to a rule text or a hook is not committed until one independent agent that did not write it has read it
against the sources and the other rules. The review has three questions: does it duplicate another rule, does it
contradict one, and does a sweep of the removed terms, touched counts and the contract surface find anything
left behind. A rule has one home; the rest points to it. In October 2026 a clean-up moved 19 rule files to
history and folded 22 working-method entries into one, keeping my quoted words in place.

## What the improvement does not do

* It does not prove that the method is good. It makes its failures cheap to see and costly to leave in place.
* A rule that has been fixed twice and still breaks is information about the rule, not only about the agent.
* The mechanisms depend on a human reading the digest. Without that, they are records and nothing more.

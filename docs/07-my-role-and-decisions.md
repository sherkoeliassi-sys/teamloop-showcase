# My role and the decisions I made

## My role

I own the method and I am the only human in it. I set the goals and the standing orders, read the outcomes,
correct the orchestrating AI session when it errs, and perform the few acts that are reserved to me and that no
agent may do (entering credentials or keys, and starting parts of the system that I have frozen). Everything
between a goal and its outcome follows the chain and the decision route in
[00-how-it-works.md](00-how-it-works.md): the agents decide within my standing orders, and what they cannot
settle goes to two independent models, not to me.

That is itself a decision, and the list below records it with the others. Each row is a decision I gave, with
its date. The wording in the rule files is checked against my words in the session transcripts; I give the
effect in my own summary here.

## Decisions that shaped the method

The "reason on record" column says only what the rule files or the session records state. Where no reason was
written down, it says so, instead of my supplying one afterwards.

| Date | What I decided | Reason on record | What changed |
|---|---|---|---|
| 2026-09-16 | Every constant, format and count an agent writes must have a run behind it in the same turn, or be marked UNVERIFIED. | Three review rounds in a row found the same class of error: values written from memory and never run. | A written-from-memory value is a defect. It is the first rule in the rule index and it applies to code, briefs and reports alike. |
| 2026-09-30 | Never write from memory, only from an open source. | The errors came from compressing a source into a summary and then writing against the summary. | A quoted line or a read field is required at the moment of writing, not a recollection of one read earlier. |
| 2026-11-08 | Every cap in the process may be exceeded, and no question about it comes to me. | None written down beyond the order. | An overrun is counted and reported (`OVER_CAP`, `OVER_WALL_CLOCK`), and the work continues. |
| 2026-11-10 | A test exercises today's code against an event that can occur in our work. It calls the function directly, it builds no repository or child process of its own unless that is the boundary it proves, and no code-mutation proof is written, run or required. | The rule text says a test's subject is an event that can occur in our work, not a later code edit or a threat outside it. | A new test is short and direct. The share of time spent on tests is measured. |
| 2026-11-10 | The loop's driver is not started without my word. | None written down beyond the order. | A standing order that every agent observes. It is not part of the list of delegated decisions. |
| 2026-11-12 | The principle applies to everything: every decision is the orchestrator's, and a real doubt goes to the two independent models. I keep only the reserved acts. | None written down beyond the order. | Nothing is put to me as a decision. What reaches me is a request for a reserved act, or a fact only I have. |
| 2026-11-19 | When the two models disagree they must agree: further rounds until they do, for now and for the future. | None written down beyond the order. | A disagreement ends only in agreement. A run settles what a run can settle. |
| 2026-11-21 | The silent process observer is switched off, and its redesign stopped. | I said we would focus on the audit rows instead. | The observer has no owner and nothing starts before one exists. |
| 2026-11-25 | While the loop takes on rows, nobody touches any chain. The loop and its driver, which takes the orchestrator's place, own the path from planning to an approved, published candidate (the code commit and the closure commit). Merging that candidate into the main line is a separate step, taken by the orchestrator. | I am not involved when the loop runs, because it is autonomous (my reason, given in the session on 25 November 2026). | A standing order for the next time the loop runs. The loop is frozen now, so it has not yet been exercised. |
| 2026-11-24 | Run several rows in parallel, and write the session-end protocol at 93 percent of the context. | None written down beyond the order. | The next start can run independent rows side by side. Whether 93 percent replaced the default of 90 or applied to one session was left open in that session's digest. |

## Architecture choices that follow from them

* **Process in proportion to risk.** A change gets the chain its risk class calls for, not the longest chain
  available ([01-roles.md](01-roles.md)). The orchestrator moves a class; doubt alone never does.
* **Roles that cannot judge their own work.** The builder in the sandbox has no shell, so it cannot certify its
  own result; a checker runs the commands and a reviewer compares the result with the contract.
* **Evidence tied to bytes.** A verdict names the candidate it judged, and publication requires a PASS on exactly
  the bytes that are committed ([03-receipts.md](03-receipts.md)).
* **One home per rule.** A rule lives once, in one file, and everything else points to it, so that a change
  cannot leave two contradicting copies.

## What I did not decide

I did not decide what the agents' code should be. I decided how it is planned, checked and recorded, and what
counts as done. The code behind the evidence in this repository is private and was written by the agents under
that method.

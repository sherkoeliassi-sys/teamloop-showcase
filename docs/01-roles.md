# Roles

The roles exist to enforce one rule: **whoever builds never judges.** A fresh agent checks the work without
seeing the author's reasoning, and the orchestrator writes no code.

## The four working roles

| Role | Job | What it must not do |
|---|---|---|
| **Preparer** (`planner` in the loop) | Reads one audit row and writes the contract for it: the claims, the rules that apply, the files the builder may touch, the commands that must fail on the old code (RED) and pass on the new code (GREEN), and the done criteria. | Write code. Touch anything outside the row. |
| **Builder** (`builder_writer`) | Implements exactly the contract in the allowlisted files. | Certify its own work. In the loop's sandbox the builder had no shell: in run A its handover says plainly that the RED/GREEN commands were *not* run by it and must be run before any PASS. |
| **Reviewer** (`review_a`, `review_codex`) | Tries to get the change to let through what it should stop, given one named attack task. Returns a binary verdict, PASS or NOT_PASS. A blocker needs evidence: a violated requirement, a trigger reachable today, and a reproduction or trace, plus the *exact* replacement text that fixes it. Anything weaker is a one-line `RESIDUAL` that stops nothing. | Edit files. Say "PASS, but". |
| **Checker** | In the loop: deterministic verify jobs that run the contract's commands on the baseline and on the candidate and record exit codes, plus mutation probes in the earlier runs. Outside the loop, for rule and text changes: one independent agent that reads the change against the rules and the sources. | Have an opinion. It records what ran and what the exit code was. |

## Around them

* **Orchestrator** (the main AI session that I direct): classifies the change, starts the chain, relays and
  stamps. The orchestrator selects or rewrites nothing in a brief it relays, and writes no code.
* **Deciders**: when a decision is uncertain it goes to two independent models. A disagreement is settled by a
  run if a run can settle it; otherwise by further rounds on the conditions that still differ, until they agree.
  It never ends as "both positions recorded" and never as a question to the human.
* **Writers**: agents that write only the files their brief names (records, digests) and decide nothing.

## Risk classes: process in proportion to risk

How much of the chain a change gets is decided by what it can break, not by how big it looks.

| Class | Typical content | Chain |
|---|---|---|
| K0a | a record, a pointer, a receipt, a history move | writer, sweep, commit. No agents, no runs. |
| K0b | rule wording: no code change, but an operative sentence changes meaning | writer, sweep, one independent checker, one correction, recheck, commit |
| K1 | small code change, three or fewer implementation files, no guarded path | builder with RED then GREEN, sweep, one independent checker, one correction, recheck |
| K2 | code on a guarded path, or a value that reaches commits, retention, permissions or run selection | builder, one adversarial reviewer with one named attack task, one correction, recheck, commit |
| K3 | an unresolved interface between components, a state migration, a changed trust boundary | a contract with a per-clause map reviewed before any builder starts, then one row per step |

Two details that matter:

* **Doubt never raises a class.** Only the orchestrator's decision moves one.
* **Proven bytes are not re-run.** Evidence is reused only if it is bound to the same bytes and the same
  inputs; otherwise the affected checks run again.

In the recorded runs the reviewers classified run A as K1 and runs B and C as K2. Runs A and B are the same audit
row, K117, on different bases: A was judged K1, B was judged K2 "on effect" because the change decides whether
the run's output files are written at all. The class is a judgment on the bytes in front of the reviewer, and
it was allowed to differ.

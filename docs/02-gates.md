# Gates

A gate is a mechanical refusal. The point of a gate is that it does not depend on anyone remembering a rule.
Each gate below says what it blocks and where the claim comes from.

| Gate | Blocks | Source of the claim |
|---|---|---|
| **Chain gate (row)** | Starting an agent whose start text carries no chain line. | Fired in the logged session below. |
| **Chain gate (preflight)** | Starting an agent without the stamp that the preflight check writes. | Fired in the logged session below. |
| **Commit gate** | A commit that breaks a rule about where a file may live. In the logged session it stopped a build that had put a configuration file in a directory where that kind of file is not allowed; the file was moved and the build continued. | Session digest. |
| **Heredoc guard** | A shell command that would silently halve a double backslash inside a heredoc. The agent is told to write the script to a file and run the file. | Fired in the logged session below, and again while this repository was being built. |
| **Claim gate (turn end)** | Ending a turn on an unsourced claim, or by pushing a decision to the human that the rules say the orchestrator makes. | Fired in the logged session below. |
| **Publication gate** | A closure that is not tied to exactly the bytes that were reviewed. Publication is two deterministic commits (code, then closure) on a private copy with a compare-and-swap ref update; the commit environment is pinned (git config, encoding, line endings) and the commit date is derived from the base commit, so the same input produces the same commit. | The publisher's header comment; the closure records in [examples/](../examples/). |
| **Audit anchor check** | A register whose rows carry anchor cells that do not resolve: each address must point to a named symbol on disk with the exact content hash it claims. It answers only that question. Whether the anchor is the *right* symbol for the row stays a human review question, and the tool's own header says so. Every recorded closure carries `[AUDIT_ANCHOR_OK]`. | The check's header comment; closure records of all three runs with receipts. |
| **Binding of the reviewed subject** | A verdict that does not name the candidate it judged. In all three runs with receipts the reviewer's `subject_id`, the candidate manifest and the closure record carry the same identity. | `evidence/runs.json`, fields `reviewed_subject_equals_candidate` and `closure_candidate_equals_candidate`. |

## What gates did in one session

The session digest of a three-hour session on 24 November 2026 records seven mechanical stops:

| Stop | Count |
|---|---|
| Heredoc guard | 2 |
| Chain gate, missing chain line | 1 |
| Chain gate, missing preflight stamp | 1 |
| Claim gate | 2 |
| Turn-end gate (decision pushed to the human) | 1 |

Next to them the digest lists the orchestrator's own logged mistakes: 19 entries in the session. By who caught
them: 7 by a hook, 6 by the orchestrator itself, 4 by the human, 1 agent's rule breach seen in the agent's own
reply, and 1 left unresolved with the reason written down. I counted these from the digest; I did not re-derive
them from the transcript.

The gates did not make the orchestrator right. They made a class of errors expensive to leave in place. The
digest exists so that the *repeated* breaks are visible: a rule that is broken twice in a row is escalated, and
its cause is fixed or it is moved out of the active rules.

## What the gates do not cover

* A gate checks the form it was written for. A reviewer who looks at the wrong thing still produces a
  well-formed PASS; that is why a verdict records which attack task it ran and which receipts it reused.
* Some acts stay human-only by rule (for example entering credentials, or deciding to publish outside the
  sandbox). No agent is allowed to do those, and a human's approval for one act does not extend to another.

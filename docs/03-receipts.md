# Receipts

A decision without a receipt does not exist. A receipt is a saved file written by the machine (or stamped
from an agent's answer by a tool), never typed up afterwards from memory.

## What each receipt answers

| Receipt | Written by | Answers | Example |
|---|---|---|---|
| **Job receipt** | the job runner | what ran, when, for how long, with which exit code, and the hashes of its stdout and stderr | [job_receipt.json](../examples/job_receipt.json) |
| **Evidence entry** | the checker | which contract command ran, on baseline or candidate, whether the outcome was the expected RED or GREEN, with the raw output hashes | [evidence_entry.json](../examples/evidence_entry.json) |
| **Verdict** | the reviewer | PASS or NOT_PASS for one named candidate; each blocker with its class, proof and exact fix | [verdict_round1_not_pass.json](../examples/verdict_round1_not_pass.json) |
| **Fix request** | the machine | the blockers of the previous round, with the reviewer's fix text copied unchanged | [fix_request.json](../examples/fix_request.json) |
| **Closure record** | the publisher | which code commit and closure commit belong to which contract and candidate, and that the anchor check passed | [closure_record.json](../examples/closure_record.json) |

## Why the shapes look the way they do

* **Identity by hash.** A verdict carries `subject_id`, the identity of the candidate it judged. The candidate
  manifest lists every file with its SHA-256. The closure record repeats the candidate identity. That chain is
  what makes it possible to check afterwards that the bytes that were reviewed are the bytes that were
  committed (see [05-evidence-four-closures.md](05-evidence-four-closures.md): this holds for all three runs
  with receipts).
* **RED before GREEN.** The contract's commands must *fail* on the baseline and *pass* on the candidate. A test
  that passes on both proves nothing, so the evidence entry records the expected and the observed outcome side
  by side (`expect: RED`, `classified: RED_OBSERVED`).
* **Reuse is explicit.** A reviewer may reuse earlier evidence only if it names the receipt and the bytes it
  applies to. In the recorded verdicts the reviewers say which receipts they reused and which they re-ran.
* **A green result proves only what it ran.** In the walkthrough the builder's tests were green and wrong at
  the same time. The reviewer compares the green result with what the contract required before trusting it.

## What is in the examples

The files in [examples/](../examples/) are **sanitized**: field names, structure, outcomes, durations and exit
codes are the real ones from run A; identifiers are shortened to 8 characters; every free-text field and every
path was rewritten or removed because the originals describe a private codebase. Each file carries a
`_sanitized` marker saying so. They show the form of a receipt, not the content of the work.

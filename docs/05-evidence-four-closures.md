# Evidence: four closures by the loop

The claim: **in sandbox clones of a repository, the loop closed audit row K117 three times and audit row K97
once, with no human edit between the reviewer's PASS and the commit.** This page says where each part of that
claim comes from, how I checked it, and which part I could not check.

## What "closed" means here

The audit register is a table of rows, one per known defect. A row is `OPEN` or closed. The loop's publisher
makes two commits on a private branch: a *code commit* with the change, then a *closure commit* that changes
only the register. The closure commit flips the closing row from open to closed and records which code commit
closed it. It also re-stamps the code anchors of other rows that point into the files the change touched, so
it changes more than one row: 38 rows in run A, 44 in run B and 11 in run C (38 in run D). I counted those from
the closure commits' diffs. The author of both commits is the loop's own identity, not a person.

These runs happened in **sandbox clones** created for proving the loop (sandbox 5, 7 and 13). The branch they
wrote to is the loop's own branch in the clone. They are not commits to the production repository. See
[06-limits.md](06-limits.md) for what that means for the claim.

## The four runs

Data: [../evidence/runs.json](../evidence/runs.json).

| Run | Sandbox | Row | Date (UTC) | Rounds | Reviewer seat | Agent time | Wall clock |
|---|---|---|---|---|---|---|---|
| A | 5 | K117 | 2026-10-30 | NOT_PASS, PASS | `review_a` | 35.2 min | 50.2 min |
| B | 13 | K117 | 2026-11-02 | PASS | `review_a` | 25.0 min | 87.9 min |
| C | 13 | K97 | 2026-11-03 | NOT_PASS, PASS | `review_codex` | 21.1 min | 148.6 min |
| D | 7 | K117 | after 2026-10-31 | not recoverable | not recoverable | not recoverable | not recoverable |

Agent time is the sum of the planner, builder and reviewer job durations in the job receipts. Wall clock runs
from the first job's start to the last job's end and includes waiting between jobs, so it is not a measure of
work. In run C the code commit's parent is run B's closure commit: the second row was built on top of the first.

Commit dates in the sandboxes are **not** run times. The publisher pins the commit date to the base commit's
time plus one second (two for the closure), so the same input yields the same commit. I took run times from
the job receipts and nowhere else.

## What I checked, and how

The checks below were run on 25 November 2026 by an AI assistant working for me, against the private receipts
and the sandbox repositories, and I have read the results. They are the same kind of check the loop's own
roles make, which is the point: a claim about the process is itself checked against the artifacts, not
written from memory.

For each run with receipts (A, B, C):

1. **Verdicts.** Read every `verdict.json` in the post's rounds. A: NOT_PASS then PASS. B: PASS. C: NOT_PASS then
   PASS. The final round's verdict was PASS in all three.
2. **Reviewed bytes equal committed bytes.** The final round's candidate manifest lists each changed file with
   its SHA-256. I ran `git show <code commit>:<path>` for every file and hashed the output. All files matched
   (A 3 of 3, B 4 of 4, C 2 of 2).
3. **Same candidate throughout.** The reviewer's `subject_id`, the candidate's `candidate_id` and the closure
   record's `candidate_id` are equal in all three.
4. **Code commit sits on the declared base.** The parent of the code commit is the base commit recorded in the
   candidate (A and B on a human-made commit, C on run B's closure).
5. **Anchor check.** Every closure record carries `[AUDIT_ANCHOR_OK]`.
6. **Evidence at the right polarity.** Final-round checker jobs: the RED commands fail on the baseline, the
   GREEN commands pass on the candidate. Run B's four mutation probes and run C's five were all killed
   (non-zero exit), and each run's unmutated control passed.

| Run | Final-round tests on the candidate | RED commands on the baseline | Mutation probes killed |
|---|---|---|---|
| A | 9 passed (regression set: 2 passed) | guard: 8 failed; wiring: 1 failed | none used in this run |
| B | 26 passed (regression set: 8 passed) | 25 failed | 4 of 4 |
| C | 5 passed | three RED commands, 1 failed each | 5 of 5 |

## What I could not check: run D

For run D the control root with the receipts is no longer on disk. What remains is the pair of commits: both
authored by the loop identity, both carrying the same contract, candidate and operation identifiers, the code
commit touching three files and the closure commit changing the register (the closing row from open to
closed, plus anchor re-stamps, 38 rows in all). That shows a
loop closure was published. It does **not** show the reviewer's verdict, and I cannot re-run the byte check.
So D is listed, and it is excluded from every statement above that starts with "I checked".

Run D is the reason this page says "four closures" in the first line and "three with receipts" everywhere a
number depends on receipts.

## Reproducing the checks

The receipts live in private control directories that I do not publish, so the checks above cannot be re-run
from this repository. What *can* be re-run is the consistency of the published data:

```
python tools/check_repo.py
```

That asserts, from `evidence/runs.json`, that every run with receipts ends in PASS, that reviewed bytes equal
committed bytes, that subject and candidate identities match, that the anchor check passed, and that D is
flagged as having no receipts. It also scans the repository for terms that must not appear.

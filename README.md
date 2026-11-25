# The teamloop: how I work with AI agents

*Kort på svenska:* det här repot visar hur jag arbetar med AI-agenter i ett arbetssätt jag kallar teamloopen:
fasta roller (förberedare, byggare, granskare, kontrollant), kvitton för varje steg, grindar som stoppar fel
mekaniskt, och ett förlopp där en granskare säger NOT_PASS, byggaren rättar och granskaren säger PASS.
Allt är anonymiserat: inget innehåll från mitt underliggande projekt finns här. Gränserna för vad beläggen visar
står i [docs/06-limits.md](docs/06-limits.md) och är med avsikt inte gömda.

---

This repository is a small, public showcase of a way of working with AI coding agents that I use and maintain:
**the teamloop**. It is about the *process*, not about any particular codebase. The codebase the process was
used on is private and nothing from it is included.

## The idea in four sentences

1. Work is split into roles that never judge their own output: a **preparer** writes the contract, a **builder**
   implements exactly that contract, a **reviewer** tries to break the result, and a **checker** runs the
   commands and records what happened ([docs/01-roles.md](docs/01-roles.md)).
2. Every step leaves a **receipt**: a file with the role, the verdict, the evidence and the byte identity of what
   was judged ([docs/03-receipts.md](docs/03-receipts.md)).
3. **Gates** refuse to continue when a rule is broken: an agent cannot start without a registered chain, a
   closure cannot be published without a PASS on exactly the bytes being committed
   ([docs/02-gates.md](docs/02-gates.md)).
4. How much process a change gets depends on its **risk class**, so a one-line text fix is not run through the
   chain built for an architecture change.

## How it works, in one picture

Read [docs/00-how-it-works.md](docs/00-how-it-works.md) first. In short:

```
BUILDING   classify -> preparer (contract) -> builder -> checker (RED on old, GREEN on new)
                    -> reviewer (PASS, or NOT_PASS + exact fix) -> one correction + recheck -> publish

DECIDING   a question no builder may answer -> two independent models answer alone
                    -> a run settles what a run can settle -> otherwise rounds until they agree
                    -> the orchestrator relays, settles nothing, and checks the answer against the owner's wishes
```

Every step leaves a receipt, gates refuse to continue when a rule is broken, and the owner keeps only the few
acts no agent may perform.

## What is demonstrated

| | |
|---|---|
| A complete rejected-then-accepted run | [docs/04-walkthrough-not-pass-to-pass.md](docs/04-walkthrough-not-pass-to-pass.md): reviewer says NOT_PASS, the fix is applied, the same reviewer rechecks and says PASS. Anonymized, with the real timings. |
| Four closures made by the loop itself | [docs/05-evidence-four-closures.md](docs/05-evidence-four-closures.md) and [evidence/runs.json](evidence/runs.json): audit rows K117 (three times) and K97 (once) were closed by the loop in sandbox clones. |
| Sanitized receipts | [examples/](examples/): verdict, fix request, job receipt, evidence entry, closure record. |
| What the evidence does *not* show | [docs/06-limits.md](docs/06-limits.md). Read this before drawing conclusions. |
| My role and the decisions I made | [docs/07-my-role-and-decisions.md](docs/07-my-role-and-decisions.md): dated decisions, with the reason where one was written down. |
| How the method improves | [docs/08-how-the-method-improves.md](docs/08-how-the-method-improves.md): digests, correction budget, gate ledger, reviewed rule changes. |
| Stack and integrations | [docs/09-stack-and-integrations.md](docs/09-stack-and-integrations.md): the tooling of the method, not of the private codebase. |

## The four loop closures at a glance

"Closed" means: the loop planned, built, verified, reviewed, corrected where needed and published two commits
(code, then closure) that flip one row of an internal audit register from open to closed (and re-stamp the code
anchors of other rows that point into the changed files), **in a throw-away clone of the repository**, not in
the production repository.

| Run | Row | Rounds | Reviewer verdicts | Agent time¹ | Reviewed bytes = committed bytes² | Receipts on disk |
|---|---|---|---|---|---|---|
| A | K117 | 2 | NOT_PASS, then PASS | 35.2 min | yes (3 of 3 files) | yes |
| B | K117 | 1 | PASS | 25.0 min | yes (4 of 4 files) | yes |
| C | K97 | 2 | NOT_PASS, then PASS | 21.1 min | yes (2 of 2 files) | yes |
| D | K117 | n/a | n/a | n/a | not checkable | **no** (only the two commits remain) |

¹ planner + builder + reviewer job time from the job receipts. Wall-clock is longer (A 50.2, B 87.9, C 148.6
minutes) because it includes waiting between jobs.
² I recomputed SHA-256 of every file in the reviewed candidate manifest and compared it with the same file in
the code commit.

Three of the four closures were re-checked end to end against private receipts; the fourth could not be, and
the table says so. The receipts themselves are not published, so a reader of this repository can inspect the
data and the method but cannot re-run those checks.

## What this is not

* It is not a claim that the loop replaces human judgment. People chose the rows, started the runs, set the
  rules and read the outcomes. The loop did the plan, build, verify, review, correct and publish cycle inside a
  single post.
* It is not a proof that the code changes were *right*, only that the process's checks passed on them and that
  in two runs the reviewer found departures from the contract that the builder's own green tests had not caught
  (see the walkthrough).
* It is not a product. It is a record of a working method, including where it was frozen or still wrong.

## Repository map

```
README.md                      this file
docs/00-how-it-works.md        the whole flow: building chain and decision route
docs/01-roles.md               the four roles, plus orchestrator and deciders
docs/02-gates.md               gates and what each one blocks
docs/03-receipts.md            what a receipt contains and why
docs/04-walkthrough-...md      NOT_PASS -> correction -> PASS, anonymized
docs/05-evidence-four-...md    the four closures, how each number was obtained
docs/06-limits.md              honest limits
docs/07-my-role-and-...md      my role and my dated decisions
docs/08-how-the-method-...md   how the method improves itself
docs/09-stack-and-...md        stack and integrations of the method
evidence/runs.json             machine-readable data behind the tables
examples/                      sanitized receipt examples
tools/check_repo.py            leak scan + consistency check of this repo
```

Run `python tools/check_repo.py` to scan every file for leaked terms and to re-check the invariants stated in
the tables against `evidence/runs.json`.

# Limits

What the evidence in this repository does not show. These are listed because a reader who finds them alone
would reasonably distrust everything else.

## 1. The closures happened in sandboxes

The four closures were made in throw-away clones of the repository, created to prove the loop. In the production
repository the same two rows, K117 and K97, were later closed through **manually run chains** with the same roles
(the production register names a manual chain for each). So the claim is not "the loop closed these defects in
production". It is "in sandboxes, the loop closed these two rows end to end, with checkable receipts for three of
the four runs."

K117 appears three times because three separate sandboxes each started with that row open. It is evidence that
the loop can repeat the work, not evidence of three different defects.

## 2. Four runs is a small sample, and it was not random

The rows were picked by people and by two independent deciders as code-only rows, to test the loop on the
least risky kind of work first. Three runs have receipts and one does not (run D, see
[05-evidence-four-closures.md](05-evidence-four-closures.md)). Nothing here shows how the loop behaves on
harder rows.

## 3. "On its own" has a precise meaning

People chose the rows, started each run, wrote the rules the loop followed, and read the outcome afterwards.
Within a run, the cycle plan, build, verify, review, correct, publish was done by the loop, and I checked that
no byte changed between the final PASS and the commit. I did not and could not show that no human ever looked at
a run while it was going. Since 25 November 2026 a standing order says nobody touches any chain while the loop
works on rows; it came after these runs and has not been exercised, because the loop is frozen.

## 4. The reviewers' model identity is not in the artifacts I read

The runs record the reviewer's *seat* (`review_a` in runs A and B, `review_codex` in run C), not which model
filled it. I therefore make no claim about reviewer model families, and I do not claim independence between
builder and reviewer beyond what the role separation and the recorded evidence show.

## 5. Whether K117 was fully closed was itself disputed

When two independent deciders were asked, after these runs, whether K117 counted as closed, they agreed on
several points and **disagreed** on that one (yes against partly) and on whether it should have been classed K1
or K2. I have not traced how that was resolved. I kept the word "closed" for what the register row and the
receipts show, and no more.

## 6. The process has changed since these runs

Runs B and C used mutation probes: the contract's tests were run against deliberately broken versions of the
code to prove they notice. Since 10 November 2026 the rules say no code-mutation proof is written, run or
required, and that tests exercise today's code against events that can occur in the work. A reader who wants
the method as it stands today should not copy the probes from runs B and C.

## 7. The loop is frozen

The loop's driver is currently frozen: starting it needs the owner's explicit word. The method documented here
is how it worked and how the manual chains work now, not a running automatic service.

## 8. The orchestrator still makes mistakes

[02-gates.md](02-gates.md) lists 19 logged orchestrator mistakes in one three-hour session. Hooks caught seven,
the orchestrator itself six, the human four, one came from an agent's own reply, and one is unresolved. This is
why the gates exist. Hooks stopped 7 of the 19 and the orchestrator's own checks caught 6 more, so 13 of the 19
were caught without a human (14 counting the agent's breach, which was seen in the agent's own reply). Four
reached the human before anyone caught them and one is unresolved. Hooks alone did not catch a majority; the
claim here is that most were caught by the system itself, and that the ones it missed are listed. The gates
reduce the cost of this class of error; they do not remove it.

## 9. Process checks are not proof of correctness

A PASS means a reviewer who tried to break the change could not, on the bytes in front of it, within its named
attack task. The code behind these runs is private and not shown here. This repository demonstrates a method for
finding defects such as an incomplete failure message or a test table that does not cover the required range. It
does not demonstrate that the resulting code is free of defects.

## 10. What was removed

Everything that describes the codebase's purpose or content was removed or rewritten: file and function names,
paths, message texts, domain terms, data, configuration, keys. Receipts in [examples/](../examples/) keep their
structure and their numbers (durations, exit codes, counts) and nothing else.

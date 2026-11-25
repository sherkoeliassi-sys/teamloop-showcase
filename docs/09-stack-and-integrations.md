# Stack and integrations

The stack of the *method*, not of the private codebase it was used on. Nothing here describes what that
codebase is or does.

| Layer | What is used | What it does in the method |
|---|---|---|
| Orchestrator | Claude Code (desktop app) | The main session: classifies, opens chains, relays briefs, stamps receipts. Writes no code. |
| Agent seats | Claude, Codex CLI, Cursor agent CLI, and Gemini through the Antigravity CLI | Preparer, builder, reviewer and decider seats are filled from these. The same model in two different harnesses counts as two different colleagues, and a test result belongs to the pair of model and harness. |
| Driver | A Python queue driver | Takes the place of the orchestrator in the autonomous loop: selects the next row, runs the loop's post command, writes a receipt line and one log commit, notifies, and stops on errors. |
| Memory | An MCP memory server | Holds the startup text, the live status, the frozen digests and the decision records that a session reads at its start. |
| Hooks | Python scripts on tool calls and on the end of a turn | Refuse a start without a registered chain, refuse risky shell forms, refuse a commit that breaks a rule, and ask at turn end which command could have failed. |
| Version control | git, with commit hooks, private worktrees and deterministic publication | Two commits per closure with pinned environment and date; a compare-and-swap ref update; recovery. |
| Checks | Python and pytest | The contract's RED, GREEN and regression commands, run by the checker and recorded with exit codes. |
| Workers | Separate Windows accounts for agent jobs | A job runs under its own account with restricted write rights, so a worker's writes are denied outside what its job needs. |
| Receipts | Plain JSON and Markdown files in a control directory | One file per job, verdict, fix request and closure ([03-receipts.md](03-receipts.md)). |

## Where each one meets the method

* The **orchestrator** (or, in the autonomous loop, the driver) and the **seats** meet in the chain: the orchestrator starts a role, the role's output
  comes back as a receipt, and nothing in a brief is rewritten on the way.
* The **memory server** is read at the start of a session and written at its end. It is how the next session
  knows what is open and where each open item lives ([08-how-the-method-improves.md](08-how-the-method-improves.md)).
* The **hooks** are the gates in [02-gates.md](02-gates.md). They run outside the model, so an agent cannot
  talk its way past them.
* **git** is what makes closure checkable: the closure record names the code commit, and the reviewed bytes can
  be hashed against it ([05-evidence-four-closures.md](05-evidence-four-closures.md)).

## What I do not claim

* That these specific tools are the method. The method is the roles, the receipts and the gates; a different
  set of tools could carry it.
* That every seat has been compared with every other. The records name the reviewer's *seat* in each run, not
  which model filled it, and make no claim about model families
  ([06-limits.md](06-limits.md), section 4).

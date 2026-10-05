# Unattended Agent Harness

An operational substrate for running many long-running agent tasks without a human
in the loop. Extracted from a working single-operator harness.

This is not a new agent architecture. The architecture is settled. What is missing
is the part that makes it survive contact with reality: durable ownership across
process death, automatic recovery, and instructions that do not change midway
through a task.

---

## The problem

Running agents unattended fails in ways that are not reasoning failures.

You start a task. You walk away. The task stops and waits for you, and you cannot
tell which of your sessions is waiting. A new task queues behind work already in
progress. Several tasks share one context window and compete for it. A new session
starts from zero, or drags the previous task's context along. The agent hands you a
list of options instead of deciding.

None of these are model-capability problems. A better model does not fix a task
that died while you were away.

## What the research already establishes

Two failure modes are documented by Anthropic in
[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
and
[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps):

- **Context exhaustion.** Agents lose coherence as the window fills, and some
  exhibit "context anxiety" — wrapping up prematurely near a perceived limit.
  Their finding: context *resets* with a structured handoff beat compaction,
  because a reset gives a clean slate while compaction preserves the anxiety.
- **Unreliable self-evaluation.** Agents "confidently praise" their own work.
  Separating the agent doing the work from the agent judging it is a strong lever.

The industry has converged on the corresponding topology: **one context-owning
orchestrator spawning ephemeral subagents that each run in a fresh window and
return a bounded artifact.** Anthropic, Cognition, OpenAI, and LangChain all ship
this shape. Peer-to-peer agent meshes lost ground because their coordination cost
scales quadratically.

So the architecture is not the contribution here.

## What this repository addresses

The published work describes architectures and ships quickstarts. The published
handoff is a progress file in a repository; recovery is a human noticing. This
repository is about the layer underneath:

| Concern | Mechanism here |
| --- | --- |
| Ownership must outlive the process | A worklist claim, not a conversation |
| Work must resume without a human | Leases, timers, and owner restart |
| Instructions must not shift mid-task | Per-task version pinning |
| Context must not leak between tasks | Fresh context per specialist call |
| Corrections must not arrive from nowhere | Evidence-gated updates with independent evaluation |

Each is a coordination or durability mechanism. None is solved by a stronger model.

## Contents

```
docs/
  00-problem.md             six failure modes, each with a symptom to self-diagnose
  01-three-levels.md        dispatcher / owners / specialists: roles and invariants
  02-self-evolving-loop.md  evidence -> propose -> refute -> version -> monitor -> roll back
  03-tradeoffs.md           what this costs, when not to use it
  04-adoption.md            incremental migration
patterns/                   one file per pattern, vendor-neutral
skills/                     packaged as Agent Skills for any compatible client
reference/                  minimal implementation to copy
diagrams/                   source-rendered diagrams
bench/                      the empirical tests behind the claims above
```

`bench/` is not a library. It is the sandbox that produced the numbers cited in
[02-self-evolving-loop.md](docs/02-self-evolving-loop.md) and
[03-tradeoffs.md](docs/03-tradeoffs.md), kept in the repository so a reader can
re-run it or check the raw output in `bench/results/`.

## When not to use this

This costs concurrency, tokens, and orchestration complexity. Do not adopt it for
a single task that fits in one context window — a single trajectory is simpler and
strictly cheaper there, and the research is consistent that multi-agent designs do
not beat a single agent at equal budget on bounded reasoning tasks.

Adopt it when the constraint is coordination: many independent long-running tasks,
work that must survive process death, and human attention as the bottleneck.

## Status

Extracted from one operator's working harness. The patterns are described as
invariants so they can be checked, not as a framework to install.

**Some invariants have been tested; others have not.** [`bench/`](bench/) exercises
these claims under fault injection and records what held. Rather than repeat its
numbers here, where they would drift out of sync:

| Claim | Status there |
| --- | --- |
| Ownership survives process death | Supported — tested under `SIGKILL` |
| Leases enable recovery without a human | Supported, with a negative control |
| Concurrent claiming is safe | Supported — 5-way process race |
| Running tasks keep their version | Supported, with a negative control |
| Isolation bounds peak context | Supported — context flat vs linearly growing |
| Specs plus artifacts beat paraphrase relaying | Supported — 3/3 vs 0/3, mechanism verified |
| A firmly-worded boundary beats a softly-worded one | Supported — 0/20 vs 7/20, with the no-rule control also at 7/20 |
| The failure is induced by low-stakes framing, not context depth | Supported — violations concentrated on "it's only one line" |
| A different vendor catches what the producer misses | **Not established** — six vendors spanned the full range; vendor and model moved together, so neither is isolated |
| Reviewer model quality drives detection | Supported — recall varied 0/4 to 3/4 on identical code |
| Refuters must be validated on known-correct work | **Supported** — 4 of 6 models rejected correct code every time |

Two of these are negative or qualified results, and they are stated here rather than
buried. Treat any claim not in that table as **argued, not measured**.

## License

MIT.

# 03 — Tradeoffs

What this costs, when it pays, and when it is the wrong choice. Read this before
adopting anything else here.

The short version: this is a coordination structure. It buys durability and
concurrency isolation, and it charges orchestration complexity, tokens, and latency.
If coordination is not your constraint, you are paying for nothing.

---

## What it costs

**Tokens.** Every level is a model call with its own context. A dispatcher that
triages, an owner that plans and integrates, specialists that execute, and an
evaluator that judges is several times the token cost of one trajectory doing the
same work.

**Latency.** Each handoff is a round trip. A task that a single agent performs in
one continuous pass takes longer when it is decomposed, triaged, and reassembled.

**Orchestration complexity.** Durable state, leases, recovery, version pinning, and
an evaluation path all need to exist and be correct. Anthropic's account of context
resets names the same price directly: this "adds orchestration complexity, token
overhead, and latency to each harness run."

**Attribution difficulty.** When a task fails, the cause may be in any level. A
single trajectory fails in one place.

**The refuter is genuinely expensive.** A different-provider evaluator is slower and
costlier than a same-model check. Measured directly: cross-provider refutation took
**42.3s against 5.0s** for the same seven reviews, roughly 8× slower. That cost is
verified. The accuracy benefit is supported by a small sample and is confounded with
reviewer strength — see [02-self-evolving-loop.md](02-self-evolving-loop.md). Pay the
cost for independence, and do not expect a measured multiplier on quality.

## When it pays

**Many independent long-running tasks.** The constraint is coordination, not
reasoning. N owners run concurrently; a single session is one lane.

**Human attention is the bottleneck.** Work completes without a person at every
step, and what reaches the human is finished work rather than questions.

**Work must survive process death.** A crashed owner resumes from durable state
instead of restarting. This is the failure no model improvement fixes.

**Context must not leak between tasks.** Unrelated tasks in one window interfere;
separate windows with fresh contexts do not.

**Corrections must hold.** A behavior you fix should not recur on a different task
days later, and knowledge that has aged must be revisable from evidence.

## When it does not pay

**A single task that fits in one context window.** Here a single trajectory is
simpler, cheaper, and at least as effective. This is not a matter of taste: on
bounded multi-hop reasoning at matched token budgets, single-agent systems match or
outperform multi-agent designs, and sweeping across model generations did not
produce a regime where the multi-agent ordering became superior.

**You are present throughout.** If you are watching every step anyway, the
dispatcher is an extra hop, the worklist is overhead, and the loop's evidence is
just you.

**The work is strictly sequential with judgment between steps.** Where each step
depends on a judgment about the last, decomposition adds handoffs without adding
parallelism.

**Tasks share mutable state tightly.** Where tasks cannot be isolated, separate
contexts do not help, because the coordination has to happen inside the work.

**You need the answer in one pass.** Latency across levels is real. For interactive
work, it dominates.

## The honest counter-evidence

Two results worth knowing, and they are not weak:

**Single-agent parity.** Under matched reasoning-token budgets, single-agent systems
consistently match or outperform multi-agent systems on multi-hop reasoning
(Tran & Kiela, arXiv 2604.02460). The theoretical argument is the data-processing
inequality: passing information through more agents can only lose information, never
add it. The authors state the condition under which multi-agent becomes competitive —
when a single agent's effective context utilization is degraded.

**Multi-agent cost.** Anthropic's widely cited figure is that multi-agent systems
use roughly 15× the tokens of chat interactions. Any adoption argument has to
justify that premium.

Neither result speaks to the coordination failures above, because neither measures
them — both are single-task benchmarks, and neither induces concurrency load or
process death. But they are the reason this document leads with "when it does not
pay" rather than with benefits. The burden of proof sits with the more complex
design.

Worth stating plainly: the strongest counter-evidence tests *sequential relay*
topologies, where each agent passes a summary to the next and meaning degrades once
per hop. That is a different graph from a hub with durable state and bounded,
spec-driven delegation. The results do not transfer, in either direction — which is
why your own measurements matter more than the argument here.

## A decision rule

Adopt this when **both** hold:

1. You have more concurrent long-running work than one session can hold.
2. You cannot be present for every step.

Start with the single cheapest mechanism that fixes your actual failure mode
([04-adoption.md](04-adoption.md)) rather than the whole structure. Measure whether
it helped. If a single trajectory handles your work, stop — that is the correct
answer, not a compromise.

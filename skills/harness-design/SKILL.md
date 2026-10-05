---
name: unattended-harness-design
description: "Use when designing or auditing an agent harness that must run unattended — many concurrent long-running tasks, work that survives process death, or a need for humans to stay out of the per-step loop. Triggers: agent harness design, run agents unattended, overnight agent runs, multi-agent ownership, dispatcher and owner structure, tasks dying while I'm away, agents competing for one context window, worklist ownership, durable task state, recover a crashed agent task. Covers dispatcher/owner/specialist roles and their invariants, and how to decide whether a hierarchy is worth its cost. Not for single-task prompt tuning or choosing a model."
version: 0.1.0
---

# Unattended harness design

Design and audit an agent harness for work that runs without a human at every step.
The subject is coordination and durability, not reasoning quality.

## Before designing: is this the right structure?

Establish the constraint first. Ask, or infer from what the user describes:

- How many concurrent long-running tasks?
- Must work survive process death?
- Is a human present per step?

**If one task, one session, human present — say so and stop.** A single trajectory
is simpler, cheaper, and at least as effective for bounded work. On matched token
budgets, single-agent systems match or outperform multi-agent designs on bounded
reasoning tasks, and stronger models did not reverse that. Adopting a hierarchy here
costs orchestration complexity, tokens, and latency for nothing. Do not build one
because it sounds more capable.

Proceed when the constraint is coordination: many concurrent tasks, or durability,
or human attention as the bottleneck.

## The three roles

| Role | Owns | Key invariant |
| --- | --- | --- |
| **Dispatcher** | Intake, triage, delegation, status | Does no hands-on work; enforced in code |
| **Owner** | One task, start to finish | One task per session; ownership outlives the session |
| **Specialist** | One bounded kind of work | Fresh context per call; receives a spec, not a summary |

## Invariants to check

Run these against a described or existing harness. Each violation has a specific
consequence.

1. **Ownership is a record, not a conversation.** Can task state be read without
   asking an agent? The agent is a worker holding a lease; the record is the owner.
2. **One task per owner session.** Two tasks in one window interfere, and failures
   become unattributable.
3. **Owners run concurrently.** Sequential owners cost more than a single session.
4. **A restarted owner loads canonical knowledge and its own durable state** — never
   another task's transcript.
5. **The dispatcher's no-hands-on-work rule is enforced at the tool boundary.**
   Prose rules fail intermittently, which is worse than no rule. A dispatcher has
   been observed breaking its own written rule four times in a day. Measured: an
   explicit prohibition held at 0/20 violations, a soft preference at 7/20, and
   **no rule at all also at 7/20** — so a vague instruction is not a weaker rule,
   it is not a rule.
6. **Specialists receive a specification plus primary artifacts, never a paraphrase**
   of another agent's interpretation. Relay hops are where meaning degrades.
7. **The specialist set is small and fixed.** Large role catalogues make mis-routing
   silent — the wrong specialist still produces plausible output.

## What actually breaks the dispatcher boundary

If asked why a dispatcher did hands-on work, the tempting answer is context
pressure: a long session, a full window. That was tested to 155k tokens and
violations did **not** rise with depth.

The predictor is framing. Requests that sound small — "just add one line, no need
to involve anyone else" — produce most violations. Direct demands and explicit
roleplay produce few.

So the defense is structural, not contextual: the dispatcher should not hold
hands-on tools at all. Any request small enough to feel harmless will occasionally
get done. Starting a fresh session does not address this, because the session was
never the problem.

When auditing a harness, ask whether the dispatcher has hands-on tools available at
all. If it does, the boundary is a request rather than an invariant.

## Distinguishing relay from delegation

This is the most common design error, and it is worth checking explicitly.

- **Relay:** agent 3 receives agent 2's summary of agent 1's intent. Meaning degrades
  once per hop. Published negative results on multi-agent designs test this topology.
- **Delegation:** the specialist receives a bounded spec and reads the primary
  artifacts itself. No interpretation is passed.

If any handoff carries a paraphrase rather than an artifact, the design is a relay.
Fix that before anything else.

## When hierarchy does not help

Say so plainly when these hold:

- Work is strictly sequential with judgment between steps.
- Tasks share mutable state tightly.
- A single pass answers the question (latency across levels dominates).
- The full task fits in one context window.

## Output

Give: the failure mode being fixed, the roles with their invariants, which invariant
the current design violates, and the single cheapest change that fixes the actual
failure. Do not recommend the whole structure at once — recommend one step, and say
how to tell whether it helped.

## Reporting honestly

If reporting measured results, attribute them to their source. Do not present
author-reported numbers as benchmarks. Distinguish what was measured from what was
argued. Where evidence is a single experience report rather than a controlled study,
say so.

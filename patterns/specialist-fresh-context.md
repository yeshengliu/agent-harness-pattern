# Pattern — Specialist fresh context

**Problem:** an owner's context fills with the detail of work that is bounded and
repeatable, leaving less room for the task itself.

**Solution:** delegate bounded work to a specialist that starts with a fresh context
every call, executes against a specification, and returns a bounded artifact.

## Invariants

- Fresh context for every call. No state carried between invocations.
- The specialist receives a **specification plus the primary artifacts**, never a
  summary of a previous agent's interpretation.
- Specialists are a **fixed, small set of roles**. Owners share them; several owners
  may use one role concurrently.
- The return is a bounded artifact — a diff, a review, a validation result — not a
  transcript.

## Why fresh context is the point

This is the mechanism that keeps the owner's window usable. The specialist burns its
own context and returns something small. Measured on a comparable design (NLAH,
arXiv 2603.25723), approximately 90% of prompt tokens, completion tokens, tool
calls, and model calls occurred in delegated children rather than the parent thread.
The parent stays clean by design, not by luck.

## Specification, not summary

The distinction between these two is the difference between delegation that works
and relay chains that are measured to fail:

| | Relay | Delegation |
| --- | --- | --- |
| Input | Previous agent's paraphrase of intent | Bounded spec + primary artifacts |
| Degradation | Once per hop | None — reads ground truth |
| Failure mode | Meaning drifts, plausibly | Specialist lacks needed scope |

In a relay, agent 3 can only work from agent 2's interpretation. Errors do not just
accumulate, they compound, because each layer re-derives meaning from a lossy
artifact. A specialist reading the primary artifact does not have this problem.

## Why a small fixed set

Routing over a large open-ended role catalogue becomes a many-way classification
problem, and mis-routing is **silent**: the wrong specialist still produces
plausible output. A small fixed set keeps routing decidable and mis-routing
detectable.

## Checks

- Does any specialist receive a paraphrase rather than an artifact?
- Does any specialist retain state across calls?
- Can you enumerate the roles from memory? If not, the set is too large.
- Is the parent's context growth bounded across a long task?

## Failure if omitted

The owner's context fills with bounded-work detail. Long tasks degrade as the window
fills, which is one of the two documented failure modes for long-running agents.

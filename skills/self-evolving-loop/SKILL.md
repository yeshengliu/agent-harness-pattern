---
name: self-evolving-loop
description: "Use when an agent harness must maintain its own knowledge, rules, and skills from evidence produced by real work — recurring corrections, lessons that go stale, or a need for the harness to improve without human-authored edits. Triggers: self-evolving harness, self-improving agent, agent learns from corrections, knowledge goes stale, same mistake recurs, maintain agent rules automatically, evidence-gated updates, versioned agent instructions, rollback an agent update, better model for evaluation. Covers evidence gating, independent refutation, per-task version pinning, and conditional rollback. Not for one-off prompt edits or manual skill authoring."
version: 0.1.0
---

# Self-evolving loop

Maintain what agents load — knowledge, rules, and skills — from evidence that real
work produced.

**The loop is the easy part. The guardrails are what make it trustworthy.** A loop
implemented without them is an unsupervised self-modifying system. Implement the
guardrails before the loop, not after.

## Two-sided failure to diagnose

- **Knowledge ages.** Rules were right when written; nothing revisits them. They are
  still loaded, just older than the work.
- **Knowledge does not accumulate.** The harness runs a hundred more tasks and knows
  what it knew after the first ten. Corrections are absorbed by the human, not the
  system.

The asymmetry is why this goes unnoticed: a harness that stopped learning looks
exactly like a harness with nothing to learn.

## The loop

```
evidence -> propose -> refute -> version -> monitor -> (roll back if it recurs)
```

### 1. Evidence — traces to a recorded event

Collect from real work: the operator's corrections, resolved tickets, job failures,
repeated mistakes across sessions.

**Invariant:** every candidate lesson traces to something that happened, not a
summary of it. An agent's explanation of its own mistake may aid diagnosis; it is not
proof. This invariant is what separates this loop from "an agent reflects on its
performance."

### 2. Propose — a small edit

Small enough to attribute when it misbehaves and to roll back cleanly. State the
expected effect and the cases that could reveal a regression.

Target by cause: stale fact → shared knowledge; violated constraint → rules; missing
or wrong procedure → skills.

### 3. Refute — independent, aligned, protected

Three invariants, and all three are load-bearing:

- **A different agent from the producer, validated to discriminate.** Independence
  is the goal; a different provider is one route to it, not the mechanism. Measured:
  different models on the SAME endpoint as the producer spanned the full detection
  range, matching the cross-provider result — so the model matters, not the vendor.
- **Validate on known-correct work first.** Measured: 4 of 6 models rejected correct
  code 3/3. An indiscriminate refuter inflates detection without detecting anything,
  so always report the false-positive rate alongside detection.
- **The criterion matches the real acceptance condition.** The known failure mode of
  verifier stages is not that checking corrupts work but that verifier acceptance
  diverges from the actual gate.
- **The loop cannot edit or weaken its own tests or criteria.** A self-improving
  system that can relax its own bar has no bar. Hold-out protected tests.

Rejected proposals may be revised within a retry limit, then discarded.

### 4. Version — pin per task

**Invariant:** a running task keeps the version it started with. The next task picks
up the new one. Without this, behavior depends on scheduling relative to updates, and
failures stop being reproducible.

### 5. Monitor — conditional rollback

**Invariant:** rollback triggers on recurrence of the update's own failure mode, not
automatically per update. Otherwise the loop cannot keep anything.

Missing evidence stays unknown. "No failures observed" is not "the change worked."

## Guardrail-to-failure map

| Unguarded | Fails by | Guardrail |
| --- | --- | --- |
| Lessons from summaries | Learning plausible fiction | Trace to recorded events |
| Same-model evaluation | Correlated errors pass | A validated, independent model |
| Unvalidated refuter | Rejects everything, detects nothing | Test on known-correct work |
| Loop edits its tests | Bar ratchets down | Protected held-out tests |
| Immediate application | Mid-task behavior shifts | Per-task version pinning |
| Rollback on any doubt | Nothing survives | Conditional on recurrence |

## Measured support and its limits

A third-party ablation of a comparable module found self-evolution the strongest
single addition tested (+4.8 on SWE Verified), characterizing the mechanism as "a
more disciplined acceptance-gated attempt loop," not open-ended reflection.

The same ablation found a verifier stage scoring −0.8 / −8.4, with the authors
reading it as verifier acceptance diverging from benchmark acceptance — the alignment
problem above, not evidence against verification. Report this correctly rather than
citing the verifier result as proof that review hurts.

## Scope

The loop maintains what agents load. It does not make product decisions, resolve
incompatible requirements, or decide which world is worth building. Those stay with
the human.

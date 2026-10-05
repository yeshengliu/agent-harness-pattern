# 02 — The self-evolving loop

A harness that cannot update itself decays in two directions at once. It keeps
knowledge that has gone out of date, and it fails to absorb knowledge the work
makes available. Both are failures of maintenance, not of capability.

This document specifies a loop that maintains what agents load. The loop is the
easy part. The guardrails are what make it trustworthy, and a loop implemented
without them is an unsupervised self-modifying system.

---

## The two-sided failure

**Knowledge ages.** Rules and lessons were right when written. Nothing revisits
them as the work changes. They are still loaded, just older than the work in front
of the agent.

**Knowledge does not accumulate.** The harness runs a hundred more tasks and knows
what it knew after the first ten. Corrections you make are absorbed by you, not by
the system. You correct something once, see it recur on a different task two days
later, and realize you never left the loop.

The asymmetry is what makes this hard to notice: the harness looks stable. A stable
harness that has stopped learning looks exactly like a stable harness that has
nothing to learn.

---

## The loop

```
   evidence  ->  propose  ->  refute  ->  version  ->  monitor
   (real work)   (small edit) (independent)  (pin)      (recurrence?)
                                  |                        |
                                  +---- reject/revise      +--> roll back
```

### 1. Collect evidence

Sources are real work: the operator's corrections, resolved tickets, job failures,
repeated mistakes across sessions.

**Invariant — every candidate lesson traces to something that happened.** Not a
summary of it. An agent's explanation of its own mistake can help diagnosis, but an
explanation is not proof. If a proposed lesson cannot be traced to a specific
recorded event, it does not enter the loop.

This is the invariant that separates this from "an agent reflects on its
performance."

### 2. Propose a small edit

A proposer turns evidence into a **small** change, with the expected effect and the
cases that could reveal a regression. Small matters: a large edit cannot be
attributed when it misbehaves, and cannot be rolled back cleanly.

The target depends on what needs to change:

| What is wrong | Where the change goes |
| --- | --- |
| A fact or context is stale | Shared knowledge |
| A behavior or constraint is violated | Rules |
| A procedure is missing or wrong | Skills |

### 3. Refute

A separate evaluator judges the proposal. It must be a different agent from the
producer, and it must be a model shown to discriminate.

**Invariant — the evaluator is a different agent from the producer, and it has been
shown to discriminate.** Two conditions, and the second is the one people skip.

Independence comes from a genuinely different model, not the same weights with a
different prompt. The usual route is a different provider, on the theory that
different weights produce uncorrelated errors. That theory is sound.

**But a different provider is not sufficient and not a guarantee.** In testing, six
models from six different vendors spanned the full range of detection on the same
defect: two caught it every time, two never did, two were inconsistent. A different
vendor gives you a *candidate* evaluator, which then has to be measured.

**Invariant — validate the evaluator against known-correct work first.** This is the
condition with the most practical value, and the one most easily skipped. A refuter
that rejects almost everything looks vigilant while measuring nothing. In the same
test, **four of six models rejected a correct implementation every single time** —
and one of them scored perfect detection, so its apparent skill was indiscriminate
rejection.

Report detection and false positives together, always. One without the other is not a
measurement, and a high detection rate from an indiscriminate refuter is worse than
no refuter, because it rejects good changes.

**Invariant — the evaluator's success criterion is aligned with the real one.**
A measured failure mode of verifier stages is not that checking corrupts work but
that the verifier's notion of success diverges from the actual acceptance
condition. Align them, or the refuter rejects good changes and accepts bad ones.

**Invariant — the loop cannot edit or weaken its own tests.** The evaluator runs
execution tests and protected held-out tests. The learning process must not be able
to modify either those tests or its own acceptance criteria. A self-improving
system that can relax its own bar has no bar.

Rejected proposals may be revised within a retry limit, then discarded.

#### What was measured

A producer model wrote code, a hidden test suite graded it by execution, and
refuters judged the producer's own output without being told a defect existed. The
defect was real: `set()`-based deduplication conflates `0` with `False`.

Seven models, each from a distinct vendor, judging identical defective code. Model A
is the producer; Model B is a different vendor; C through G are five further vendors:

| Refuter | Found the defect |
| --- | --- |
| Model A (the producer) | 0 of 2 |
| Model C | 0 of 2 |
| Model D | 0 of 2 |
| Model E | 1 of 2 |
| Model F | 1 of 2 |
| Model G | 2 of 2 |
| Model B | 2 of 2 |

A second probe repeated the judgement four times per model on identical code, and
detection ranged from 0 of 4 to 3 of 4. **Repeated judgements of the same code
disagreed with each other**, so this is a noisy signal rather than a stable rate.

**The false-positive control is the finding worth acting on.** Reviewing a *correct*
implementation:

| Model | Rejected correct code |
| --- | --- |
| Model A | 0 of 3 |
| Model D | 0 of 3 |
| Model C | **3 of 3** |
| Model G | **3 of 3** |
| Model F | **3 of 3** |
| Model E | **3 of 3** |

Four of six models rejected correct code every time.

**What this does not show.** The test cannot separate "different vendor" from
"different model," because both changed together across the panel — sharing an API
gateway is not sharing a provider. So the evidence does not establish that vendor
diversity helps or hurts. It establishes something narrower: picking a different
vendor gives you a candidate evaluator, and only measurement tells you whether it
discriminates.

**Limits.** Two defects from one task; four judgements per model; one producer
model; the author of the harness wrote the test. Treat the numbers as signals.

**The cost is not confounded.** Cross-provider refutation was roughly 8× slower on
identical work. That is the price of the invariant, and it is real.

### 4. Version

Accepted changes are versioned and applied.

**Invariant — a running task keeps the version it started with.** Instructions must
not change midway through work. The task that is running completes under the
version it began with; the next task picks up the new one. Without this, a task's
behavior depends on when it happened to be scheduled relative to an update, and
failures become unreproducible.

### 5. Monitor and roll back

Subsequent tasks run under the new version, and their **actual** results are checked
for failures and regressions.

**Invariant — rollback is conditional on recurrence, not automatic per edit.** An
accepted update is not rolled back merely because it was an update. Rollback
happens when the update's own failure mode reappears in later work. Missing
evidence stays unknown — absence of a regression report is not proof of
improvement.

The loop's output feeds the next collection cycle.

---

## Why this shape

Each guardrail answers a specific way an unguarded loop fails:

| Unguarded loop | Failure | Guardrail |
| --- | --- | --- |
| Lessons from summaries | Learns plausible fiction | Trace to recorded events |
| Same-model evaluation | Correlated errors pass | A validated, independent model |
| Unvalidated refuter | Rejects everything, detects nothing | Test on known-correct work |
| Loop edits its tests | Bar ratchets down | Protected held-out tests |
| Edits apply immediately | Mid-task behavior shifts | Per-task version pinning |
| Any update rolled back on any doubt | Nothing survives | Conditional on recurrence |

## Measured support

Third-party ablation of a comparable harness module found self-evolution to be the
strongest single addition tested: **+4.8** on SWE Verified, the largest positive
change in that ablation table. The same work characterizes the mechanism precisely —
not open-ended reflection, but "a more disciplined acceptance-gated attempt loop
that keeps the search narrow until failure signals justify another pass."

The same ablation found a verifier stage scoring **−0.8 / −8.4**, with the authors'
own reading being that verifier-level acceptance diverged from benchmark-level
acceptance. That is the alignment problem named above, not evidence against
verification — and it is why the alignment invariant is stated explicitly.

## Scope

The loop maintains what agents load: knowledge, rules, and skills. It does not make
product decisions, resolve incompatible requirements, or decide which world is worth
building. Those stay with the human.

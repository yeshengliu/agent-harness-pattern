# Pattern — Independent refuter

**Problem:** agents confidently praise their own work, including mediocre work, and
a confident wrong answer is indistinguishable from a confident right one from the
inside.

**Solution:** separate the agent doing the work from the agent judging it, and
**validate the judge before trusting it**. The refuter's job is to disprove the
proposal, not to endorse it.

## Invariants

- The refuter is a **different agent** from the producer, with no stake in the work.
- The refuter has been **shown to discriminate**: it finds real defects and clears
  correct work. Both must be measured.
- The refuter attempts disproof. It is not asked whether the work is acceptable.
- The refuter's success criterion is aligned with the real acceptance condition.
- The refuter cannot edit the tests it runs against, or its own criteria.
- Uncertainty routes to the refuter. Confidence acts.

## Independence, and what actually provides it

A same-model reviewer shares the producer's blind spots, so its errors correlate
with the producer's. Independence is the goal; a different provider is one route to
it, on the theory that different weights produce uncorrelated errors.

**A different provider is not sufficient, and the test could not establish whether
it helps.** Six models from six different vendors spanned the full range of detection
on the same defect: two caught it every time, two never did, two were inconsistent.
So a different vendor gives you a *candidate* evaluator, not a competent one.

Note what that test does and does not separate: vendor and model changed together
across the panel, so it isolates neither. Pick a different provider as a starting
point, then measure the model you actually intend to use.

## Validate before trusting

This is the invariant with the most practical value, and it is easy to skip.

A refuter that rejects almost everything looks vigilant while measuring nothing.
In a test, **four of six models rejected a correct implementation every single
time**. Their apparent "detection rate" was an artifact of indiscriminate rejection.

So: run the refuter against work you know is correct, and count the rejections. A
refuter with a high false-positive rate on known-good work is worse than no refuter,
because it rejects good changes and its approvals carry no information either.

Report detection and false positives together, always. One without the other is not
a measurement.

Anthropic's finding on the mechanism: agents reliably skew positive when grading
their own work, and while a separate evaluator is also inclined to be generous,
"tuning a standalone evaluator to be skeptical turns out to be far more tractable
than making a generator critical of its own work."

## Align the criterion

A measured failure mode of verifier stages is not that checking corrupts work. It is
that the verifier's notion of acceptance diverges from the real one — the verifier
approves work the real gate rejects. That produces a negative result for the verifier
that says nothing about verification and everything about alignment.

State the acceptance condition once and give it to both the producer and the
refuter. Keep the held-out tests outside the refuter's reach.

## Checks

- Different agent from the producer? Verify the actual model, not the label.
- Has the refuter been run against known-correct work? What was the rejection rate?
- Is the detection rate reported together with its false-positive rate?
- Does the refuter's criterion match the gate that ultimately accepts the work?
- Can the refuter or the loop it belongs to modify the tests or the criteria?
- What fraction of refutations are "looks good"? A refuter that mostly approves is
  not refuting.

## Failure if omitted

Self-evaluation passes mediocre work. The failure is not random: it is biased toward
approval, so it is invisible in aggregate success rates until something downstream
rejects the work — usually a human.

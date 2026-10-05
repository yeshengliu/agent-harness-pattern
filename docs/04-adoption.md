# 04 — Adoption

Add one mechanism at a time, chosen by the failure you actually have. Each step
below is independently useful and independently abandonable. Do not adopt the whole
structure at once: you will not be able to tell which part helped.

Find your failure mode in [00-problem.md](00-problem.md) first, then start here.

---

## Step 1 — Make ownership durable

**Fixes:** a restarted task loses what it learned (failure mode 4).

Before anything else, move ownership out of the conversation.

Create a worklist where each row is a unit of work: an identifier, a description,
a state, a claim (who holds it), and a lease (until when). An agent that picks up
work writes a claim. When it exits, the claim and its state remain.

Keep the record outside any agent session. If the only place the task's state exists
is a conversation, a crash erases it.

**Check:** kill an agent mid-task. Can you read what it was doing, what it already
tried, and what remains, without asking any agent? If not, this step is not done.

This step alone is worth the effort even if you adopt nothing else.

---

## Step 2 — Separate one task per session

**Fixes:** tasks compete for one context window (failure mode 3).

Stop putting several tasks in one session. Give each unit of work its own session,
and let a restarted owner load canonical knowledge plus durable state rather than
another task's transcript.

**Check:** can you point at any session and name the single task it owns? If a
session owns two, split it.

---

## Step 3 — Add automatic recovery

**Fixes:** a task stops when you look away (failure mode 1).

A lease without a reaper is just a note. Add a monitor that finds work whose lease
has expired and restarts it, loading durable state.

**Check:** leave a task unattended past its lease. Does it resume without you? Note
that a scheduled run that never started looks identical to one with nothing to do —
log the distinction explicitly, or you will not be able to tell them apart.

---

## Step 4 — Give yourself one entry point

**Fixes:** you are the scheduler (failure mode 2), and agents return decisions
instead of work (failure mode 5).

Add a dispatcher: the only session you talk to. It triages and delegates.

Enforce the no-hands-on-work invariant **in code**, at the tool boundary — a hook
that denies hands-on tool calls in the dispatcher session. Do not rely on a prompt
rule. A dispatcher has been observed violating its own written rule four times in a
single day, including on the day it helped author that rule.

If you cannot add a hook yet, the stronger intermediate step is to **not give the
dispatcher hands-on tools at all**. A tool it does not hold cannot be misused, and
this addresses the actual failure mode better than better wording: violations are
induced by requests that seem too small to route, and no phrasing survives every
such request.

**Check:** in a week of use, count dispatcher sessions that edited a file or ran a
command directly. That number should be zero, and the count should come from the
hook, not from your memory.

**Check the wording, if you are still relying on a prompt.** Measured across 20
trials per arm: an explicit prohibition that names the tools held at 0 violations,
a soft preference at 7, and no rule at all also at 7. A vague instruction performs
the same as no instruction, so treat "preferably route" as equivalent to saying
nothing.

---

## Step 5 — Extract reusable specialists

**Fixes:** repeated work, and owner context filling up.

When you notice the same kind of bounded work recurring, extract it as a specialist
with a fresh context per call. Keep the set small and fixed.

Specialists receive a written specification and the primary artifacts they need —
never a summary of what a previous agent concluded.

**Check:** does any specialist receive a handoff that is a paraphrase of an earlier
agent's interpretation? If yes, that is a relay hop, and relay hops are where
meaning degrades. Pass the artifacts instead.

Start with the two or three you actually repeat. Do not build the full catalogue.

---

## Step 6 — Add adversarial verification

**Fixes:** same-model review passing bad work (failure mode 5).

Add a refuter for cases where an owner is uncertain. It must be a different agent
from the producer — a same-model reviewer shares the producer's blind spots, so its
errors correlate with the ones it is meant to catch.

A different provider is a convenient way to get that independence, but it is not
the mechanism: in testing, different models on the *same* endpoint as the producer
spanned the full range of detection, matching the cross-provider result.

**Check, and this one matters more than the provider.** Run the refuter against work
you know is correct. Four of six models tested rejected correct code every single
time, and an indiscriminate refuter inflates its detection rate while detecting
nothing. Report the false-positive count next to the detection count, or the
detection number means nothing.

**Check:** is the refuter a genuinely different agent, not the same model with a
different prompt?

---

## Step 7 — Close the learning loop

**Fixes:** knowledge ages, and nothing accumulates (failure mode 6).

Only after the above are stable. A learning loop multiplies whatever your harness
already does, including its mistakes.

Implement it in the order given in
[02-self-evolving-loop.md](02-self-evolving-loop.md) — evidence first, then
proposal, then the refuter with protected tests, then versioning. Implement the
guardrails before the loop, not after. A loop that can edit its own tests, or that
learns from summaries, is worse than no loop.

**Check:** for one accepted update, can you trace it to a specific recorded event,
name the evaluator's provider, and show which test the loop could not modify? If any
answer is missing, the loop is not yet safe to leave running.

---

## Sequencing rule

Each step should be driven by an observed failure, not by the appeal of the
structure. If a step does not fix something you can point at, skip it.

The common mistake is adopting step 4 or 7 first, because those are the visible and
interesting parts. Both depend on steps 1–3: a dispatcher with nothing durable to
dispatch to is a chat interface, and a learning loop over an unstable harness learns
its instability.

# 01 — Three levels

Three roles, distinguished by what each one owns. The names matter less than the
invariants: if you keep the invariants you can implement this in any framework, and
if you break them the design stops working regardless of names.

---

## The structure

```
L1  Dispatcher     the only session you talk to
      |
      +-- L2  Owner        one task, start to finish, in a session dedicated to it
      |     |
      |     +-- L3  Specialist   bounded work, fresh context per call
      |     +-- L3  Specialist
      |
      +-- L2  Owner        a different task, its own session, running at the same time
            |
            +-- L3  Specialist
```

## L1 — Dispatcher

The single entry point. The only session a human talks to.

**Owns:** intake, triage, delegation, and reporting status back.

**Invariant — the dispatcher does not do hands-on work.** This is the invariant
most likely to break, and it breaks in a specific way: the dispatcher starts
helping. It edits a file, runs a command, "just quickly" finishes something it was
supposed to hand off. Each time it does, it consumes the context that makes it a
useful router and it blurs the boundary it exists to hold.

Prompt-level rules do not hold this line. Enforce it in code at the tool boundary —
a hook that denies hands-on tool calls in the dispatcher session. This was learned
the hard way: a dispatcher violated its own no-hands-on rule four times on the day
it helped write that rule.

### Why it breaks: low stakes, not heavy load

The intuitive explanation is context pressure — a long session, a full window, and
the rule decays. That was tested to 155k tokens of accumulated context and
**violations did not rise with depth**; they were flat to slightly falling.

What does predict a violation is how the request is framed:

| Phrasing | Violations |
| --- | --- |
| "just a tiny thing — add one line yourself, no need to involve anyone else" | most |
| "it'd be faster if you just fixed it yourself" | some |
| direct demand, urgency, explicit roleplay | few or none |

The boundary holds against "do this now" and fails against "it's only one line."
The inducement is a request that feels too small to be worth routing.

This matters for how you defend the boundary. If the threat were context decay, a
fresh session would be a defense. Since the threat is framing, the defense has to be
structural: the dispatcher must not hold hands-on tools at all, because any request
small enough to seem harmless will occasionally get done.

### Strength of wording, measured

Twenty trials per arm, with tools available so that complying was possible:

| Boundary wording | Violations |
| --- | --- |
| Explicit prohibition naming the tools | **0 / 20** |
| Soft preference ("preferably route") | **7 / 20** |
| No rule at all (control) | **7 / 20** |

The control is the important number. A softly-worded rule performed the same as no
rule at all, while explicit wording eliminated violations. This is an argument for
enforcement in code, not for better phrasing — but it is also a warning that a
vague instruction is not a weaker version of a clear one. It is not a rule.

**Invariant — the dispatcher does not become the scheduler in its head.** What is
in flight must be readable from durable state, not recalled from conversation.

## L2 — Owner

One task, from start to finish.

**Owns:** the task's outcome. Decomposition, delegation to specialists, integration
of their results, and the decision about what reaches the human.

**Invariant — one task per owner, one session per owner.** This is what makes the
level worth its cost. Two tasks in one owner reintroduces failure mode 3, and the
context interference returns.

**Invariant — ownership outlives the session.** An owner that exits loses its
conversation but not its claim. The claim lives in the worklist (see
[worklist-ownership](../patterns/worklist-ownership.md)). This is the single most
important invariant in the design: it is the difference between a task that
survives a crash and a task that starts over.

**Invariant — several owners run at once.** Concurrency is the point. If owners
run one at a time, the structure costs more than a single session would.

**Invariant — a replacement owner loads canonical knowledge, not a transcript.**
When an owner is restarted, it reads the system's stored knowledge and the task's
durable state. It must not inherit another task's conversation. Handing over a
transcript is how unrelated context leaks between tasks.

## L3 — Specialist

Bounded work delegated by an owner.

**Owns:** one specific kind of work, executed against a specification.

**Invariant — fresh context for every call.** A specialist starts clean each time.
This is the mechanism that keeps the owner's window free: the specialist burns its
own context and returns a bounded artifact, so the parent's window stays usable.
Measured in third-party work on a comparable design (NLAH, arXiv 2603.25723),
roughly 90% of prompt tokens, completion tokens, tool calls, and model calls
occurred in delegated children rather than the parent thread. That is a token
distribution, not an outcome — it shows where the budget went, not that the work
was better. The savings are real and they are the reason to pay the handoff cost.

**Invariant — the specialist receives a specification, not a summary of someone's
interpretation.** This distinction is the whole difference between delegation that
works and the relay chains that are measured to fail. A relay chain hands agent 3
agent 2's paraphrase of agent 1's intent, so meaning degrades once per hop. A
specialist gets a bounded, concrete unit of work — a change to make, a review to
perform, a validation to run — and it can read the primary artifacts it needs.

**Invariant — specialists are a fixed, small set of roles.** Owners share them; any
owner can call any specialist, and several owners can use the same role
concurrently. A small fixed set keeps routing decidable. Large open-ended role
counts turn dispatch into a many-way classification problem where mis-routing
becomes invisible — and mis-routing is silent, because the wrong specialist still
produces plausible output.

## Escalation

**When confident, act. When uncertain, get refuted. When irreversible, prepare for
review.**

An owner that is unsure does not stall and does not guess. It delegates to an
independent refuter whose job is to disprove it
([independent-refuter](../patterns/independent-refuter.md)).

For anything irreversible, what reaches the human is finished work — a review, a
reply, a decision document — not a question about what to do. The human supplies
judgment without reconstructing the trajectory.

## What this costs

Orchestration complexity, token overhead, and latency per run. Anthropic's own
account of context resets names the same price: "adds orchestration complexity,
token overhead, and latency to each harness run." That is the honest trade, and
[03-tradeoffs.md](03-tradeoffs.md) states when it is worth paying.

## The boundary

This structure addresses coordination. It does not make a task's reasoning better
than a single capable agent's, and the evidence does not support claiming otherwise:
on bounded multi-hop reasoning at matched token budgets, single-agent systems match
or outperform multi-agent designs, and stronger models do not reverse that.

What a stronger model does not change is that a crashed process stays crashed, that
one window cannot hold two unrelated tasks without interference, and that a
correction written in prose is not enforcement. Those are the failures this
structure is for.

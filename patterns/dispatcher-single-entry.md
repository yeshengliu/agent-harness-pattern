# Pattern — Dispatcher as single entry

**Problem:** with many concurrent sessions, the human becomes the scheduler —
deciding what runs where and remembering what is in flight.

**Solution:** one session the human talks to. It triages, delegates to owners, and
reports status back.

## Invariants

- The dispatcher is the only session a human addresses.
- **The dispatcher does not do hands-on work.** Enforced in code at the tool
  boundary, not stated in a prompt.
- The dispatcher reads what is in flight from durable state. It does not track it
  in its own context.
- The dispatcher's context stays small. It is a router, and routing quality depends
  on that context staying clean.

## Enforce the boundary in code

This invariant fails in a specific way: the dispatcher starts helping. It edits a
file or runs a command, "just quickly," on work it was meant to hand off.

Observed directly: a dispatcher violated its own no-hands-on-work rule four times in
one day, including on the day it helped write that rule. The rule was correct and
useless. What worked was a hook denying hands-on tool calls in that session.

The general principle: **a rule that matters at a boundary belongs in code at that
boundary.** Prose rules are suggestions, and a suggestion that is violated
intermittently is worse than no rule, because you cannot tell when it held.

### What was measured

The wording claim was tested with the model given real tools, so that complying was
physically possible. Twenty trials per arm:

| Boundary wording | Violations |
| --- | --- |
| Explicit prohibition naming the tools | **0 / 20** |
| Soft preference ("preferably route") | **7 / 20** |
| No rule at all (control) | **7 / 20** |

The control is the important one. With **no rule**, violations were as high as with
the soft rule — so a softly-worded instruction bought nothing measurable over saying
nothing, while explicit wording eliminated violations entirely.

### How it fails: the small favor, not the full context

Violations concentrated on one kind of request:

| Phrasing | Violations |
| --- | --- |
| "just a tiny thing — add one line yourself, no need to involve anyone else" | **most** |
| "it'd be faster if you just fixed it yourself" | some |
| direct demand, urgency, roleplay | few or none |

The boundary held against "do this now" and failed against "it's only one line."
Low stakes, not heavy load, is the inducement.

Context depth was tested to 155k tokens and violations did **not** rise with depth;
they were flat to slightly falling. The intuition that a full context erodes rule
adherence was not supported here. The pressure comes from framing.

### A caution about testing this

Two earlier versions of that test reported zero violations everywhere and looked
like clean nulls. Both were broken, in ways worth remembering:

- **No tools were offered**, so the model could not comply even if it wanted to.
  Every "refusal" was the model reporting it had no filesystem.
- **Every arm ended with "Reply with ROUTE or REFUSE only"**, which forced a refusal
  register and suppressed tool calls in all three arms, including the control.

A test of a boundary must permit the violation it is trying to detect. A probe that
makes the wrong action impossible will report perfect compliance forever, and it
will look like evidence.

## Checks

- Count dispatcher sessions that performed hands-on work. Should be zero.
- Is the count produced by the hook, rather than by the dispatcher's own report? A
  dispatcher reporting its own compliance is not evidence of compliance.
- Can you list in-flight work without reading the dispatcher's conversation?

## Failure if omitted

You remain the scheduler. The dispatcher becomes an extra conversational hop that
adds latency without removing you from the loop.

# 00 — The problem

Six failure modes that appear when agents are run unattended. Each has a symptom
you can check against your own setup. They are listed in the order they usually
appear: the first two are visible on day one, the rest show up as concurrency and
duration increase.

These are coordination and durability failures. None is fixed by a more capable
model, because none is a reasoning failure.

---

## 1. A task stops when you look away

**Symptom:** you have several agent sessions open. You return to one and its task
is sitting exactly where you left it. You cannot tell which of the sessions needs
you without opening each one.

The task was never autonomous. It was interactive, and you were the loop.

**What this is not:** a prompting problem. The agent stopped because the turn
ended, and nothing was there to start the next turn.

---

## 2. New work queues behind running work

**Symptom:** you want to start a second task and cannot, because the session is
busy. You open another session, and now you are the scheduler — deciding what runs
where, and remembering what is in flight.

**What this is not:** a throughput problem. A single session is a single lane. More
work does not fit in it.

---

## 3. Tasks compete for one context window

**Symptom:** several tasks in one session. Answers about task B start reflecting
details from task A. Quality drops as the session fills, and an unrelated earlier
task is blamed for something it had nothing to do with.

Anthropic documents the underlying effect: models lose coherence as the window
fills, and some wrap up prematurely near a perceived limit. Compaction does not
fully fix it, because the same agent keeps its history and its anxiety. A **fresh
context with a structured handoff** does.

**What this is not:** a capacity problem. Making the window bigger moves the
threshold; it does not remove the interference between unrelated tasks.

---

## 4. A restarted task loses what it learned

**Symptom:** a task dies — process exit, crash, machine restart. You start it
again and it repeats work it already did, or asks a question it already answered.

The task's knowledge lived in a conversation, and the conversation is gone.

**What this is not:** a memory-feature problem. Recall of facts is not the same as
knowing which unit of work is in progress, what was already attempted, and what
remains.

---

## 5. Agents return decisions instead of work

**Symptom:** you asked for a change and got a list of options. You asked for a
review and got questions. The agent is confident when it should ask and asks when
it should act.

**What this is not:** something instructions alone fix. A rule written in a prompt
is a suggestion. In one recorded run the dispatcher broke the "no option lists"
rule four times on the day it helped write that same rule. The rule needed to be
enforced in code at the boundary, not restated in prose.

---

## 6. Knowledge ages, and nothing notices

**Symptom:** two halves of the same failure.

The harness keeps rules and lessons that were right when written and are now
out of date, and nothing revisits them as the work changes. Meanwhile it runs a
hundred more tasks and knows what it knew after the first ten — the work keeps
producing evidence, and none of it comes back.

You correct something, and it recurs two days later on a different task.

**What this is not:** a bigger-rules problem. Adding instructions whenever
something goes wrong grows the rule set without making any of it current. The
missing piece is a loop that maintains what agents load, from evidence the work
actually produced.

---

## Diagnosing your own setup

| If this is true | The relevant pattern |
| --- | --- |
| You cannot leave a task and have it continue | [Owner per task](../patterns/owner-per-task.md) |
| You are choosing what runs where | [Dispatcher as single entry](../patterns/dispatcher-single-entry.md) |
| Tasks in one session interfere | [Specialist fresh context](../patterns/specialist-fresh-context.md) |
| A restart loses progress | [Worklist ownership](../patterns/worklist-ownership.md) |
| Agents ask instead of acting | [Independent refuter](../patterns/independent-refuter.md) |
| Corrections recur on new tasks | [Self-evolving loop](02-self-evolving-loop.md) |
| Instructions change mid-task | [Versioned instructions](../patterns/versioned-instructions.md) |

If none of these is true — one task, one session, you present throughout — stop
here. See [03-tradeoffs.md](03-tradeoffs.md) for why adopting this would cost you
more than it returns.

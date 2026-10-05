# Pattern — Owner per task

**Problem:** several tasks in one session compete for one context window, and
because they share a transcript, they interfere.

**Solution:** one task per session. The owner holds that task from start to finish —
decomposition, delegation, integration, and the decision about what reaches the
human. Several owners run concurrently.

## Invariants

- Exactly one task per owner session.
- The owner holds the task end to end; it is not a pass-through to a sub-session.
- Owners run concurrently. Sequential owners cost more than a single session.
- Owners are short-lived. A session ending is normal, not a failure; the worklist
  claim is what persists.

## Why one task

Anthropic's account of long-running agents identifies the mechanism: models lose
coherence as the window fills, and some exhibit "context anxiety," wrapping up
prematurely near a perceived limit. Compaction helps but preserves the history and
the anxiety. A fresh context with a structured handoff gives a clean slate.

Two unrelated tasks in one window is not a capacity problem. Enlarging the window
moves the threshold at which interference starts; it does not remove it.

## Checks

- Can you name the single task each session owns?
- Do any two owners hold overlapping work?
- Does an owner receive another task's context on restart? It should receive
  canonical knowledge and its own durable state only.

## Failure if omitted

Cross-task contamination: answers about one task reflect details of another, and
quality degrades as the session fills. Attribution becomes impossible — a failure
cannot be traced to a task when both lived in one context.

# Pattern — Worklist ownership

**Problem:** an agent's knowledge of a task lives in its conversation, so a crash or
an exit erases the task's state.

**Solution:** ownership is a row in a worklist, not a conversation. An agent holds a
claim with a lease while it works. When it exits, the claim and the state remain.

## Invariants

- The worklist record is outside any agent session.
- A claim has an owner and an expiry (a lease).
- Task state — what was attempted, what remains — is written to the record, not
  held in the conversation.
- A replacement worker reads the record and canonical knowledge. It does not read
  another task's transcript.

## Why a record and not a conversation

A conversation is a poor ownership record: it is unbounded, unqueryable, coupled to
one process, and mixes the task's state with everything else that was discussed.
A record is bounded, queryable, survives process death, and holds exactly one task.

The consequence worth naming: **the agent is not the owner.** The agent is a worker
holding a lease. All the properties you want from ownership — that it persists, that
it is exclusive, that it can be inspected — come from the record, not the agent.

## Checks

- Kill a task mid-run. Is its state readable without asking an agent?
- Is any session's task state recoverable only from its chat history?
- Can you list everything currently claimed, and by what?

## Failure if omitted

Tasks restart from zero. Work is repeated or silently abandoned, and abandoned work
is indistinguishable from work never started unless you log the difference.

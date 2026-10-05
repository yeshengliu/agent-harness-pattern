# Reference implementation

A minimal, copyable implementation of the durable-orchestration core: worklist
ownership, leases, and owner restart. It is deliberately small.

**This is a reference, not a framework.** It is not installable, versioned, or
supported. Copy it, adapt it, delete what you do not need. The value is in the shape,
and the shape is about forty lines.

## What it demonstrates

The one mechanism that everything else depends on: **ownership as a record, not a
conversation.**

| File | Shows |
| --- | --- |
| `worklist.py` | Durable claims with leases, and the restart decision |

## The core idea

```python
claim = worklist.claim(task_id, owner="owner-7", lease_seconds=900)
```

A claim is a row with an owner and an expiry. Three properties follow from that,
and none of them come from the agent:

- **It persists.** The agent can die; the row does not.
- **It is exclusive.** Two owners cannot hold the same task at once.
- **It is inspectable.** You can list what is in flight without asking any agent.

The agent working the task is a worker holding a lease, not the owner of the record.
Naming this distinction correctly is most of the design.

## What this does not implement

Stated plainly so the boundary is clear:

- **No dispatcher.** Routing is a separate concern; add it when you have more work
  than one lane (see `docs/04-adoption.md`, step 4).
- **No specialists.** Delegation is per-harness and depends on your tool surface.
- **No refuter.** Independent evaluation needs a second provider configured.
- **No learning loop.** Implementation order matters; see
  `docs/02-self-evolving-loop.md`.
- **No scheduler process.** `expired()` returns what needs restarting; you decide
  what wakes the reaper.

Those omissions are intentional. Steps 1–3 of the adoption guide are the foundation,
and a foundation is what this file is.

## Using it

```bash
python3 worklist.py
```

The script runs a short demonstration: claim a task, simulate an owner dying
mid-lease, and recover it. Read the printed output to see the state transitions.

## Adapting it

Replace the JSON file with your database. The only requirements are that the record
survives process death and that claims are atomic — a claim that two owners can win
simultaneously is worse than no claim, because it is a correctness bug that appears
only under concurrency.

If you use Postgres, `SELECT ... FOR UPDATE SKIP LOCKED` gives you both properties
directly and replaces most of this file.

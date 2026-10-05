#!/usr/bin/env python3
"""Reference: durable worklist ownership with leases.

Demonstrates the one mechanism everything else in this repository depends on:
ownership is a record that outlives the agent holding it.

Run: python3 worklist.py
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

DEFAULT_PATH = Path(__file__).with_name("worklist.json")


@dataclass
class Claim:
    """A unit of work and whoever currently holds it.

    The record is the owner. `owner` names the worker, which is disposable.
    """

    task_id: str
    description: str
    state: str = "pending"          # pending | in_progress | done | failed
    owner: Optional[str] = None
    lease_expires: float = 0.0      # epoch seconds; 0 means unclaimed
    attempts: int = 0
    notes: str = ""                 # what was tried; survives the worker

    @property
    def claimed(self) -> bool:
        return self.owner is not None and self.state == "in_progress"


class Worklist:
    """A file-backed worklist.

    Deliberately minimal: a JSON file. The properties that matter are that the
    record survives process death and that claiming is atomic within a process.
    Replace with a database for real concurrency (see reference/README.md).
    """

    def __init__(self, path: Path = DEFAULT_PATH):
        self.path = path
        self._items: dict[str, Claim] = {}
        self._load()

    # ---- persistence -------------------------------------------------

    def _load(self) -> None:
        if self.path.exists():
            raw = json.loads(self.path.read_text())
            self._items = {k: Claim(**v) for k, v in raw.items()}

    def _save(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({k: asdict(v) for k, v in self._items.items()},
                                  indent=2))
        os.replace(tmp, self.path)   # atomic; never leave a half-written worklist

    # ---- the interface -----------------------------------------------

    def add(self, task_id: str, description: str) -> Claim:
        item = Claim(task_id=task_id, description=description)
        self._items[task_id] = item
        self._save()
        return item

    def claim(self, task_id: str, owner: str, lease_seconds: float = 900) -> bool:
        """Take a lease. Returns False if held elsewhere.

        A claim that two owners can win at once is worse than no claim: it is a
        correctness bug visible only under concurrency.
        """
        item = self._items.get(task_id)
        if item is None:
            raise KeyError(task_id)
        if item.claimed and item.lease_expires > time.time() and item.owner != owner:
            return False
        item.owner = owner
        item.state = "in_progress"
        item.lease_expires = time.time() + lease_seconds
        item.attempts += 1
        self._save()
        return True

    def renew(self, task_id: str, owner: str, lease_seconds: float = 900) -> bool:
        """Extend a lease. Callers must do this or long work expires mid-run."""
        item = self._items.get(task_id)
        if item is None or item.owner != owner or not item.claimed:
            return False
        item.lease_expires = time.time() + lease_seconds
        self._save()
        return True

    def release(self, task_id: str, owner: str, state: str, notes: str = "") -> None:
        """Finish or hand back. Records notes so a restart is not from zero."""
        item = self._items.get(task_id)
        if item is None:
            raise KeyError(task_id)
        item.state = state
        item.owner = None
        item.lease_expires = 0.0
        if notes:
            item.notes = (item.notes + "\n" + notes).strip()
        self._save()

    def expired(self) -> list[Claim]:
        """Work whose lease lapsed: the input to a restart decision.

        An expired claim does not mean the worker died. It may mean the lease was
        too short. Distinguish the two before restarting, or you will run work twice.
        """
        now = time.time()
        return [c for c in self._items.values()
                if c.claimed and c.lease_expires <= now]

    def inflight(self) -> list[Claim]:
        """Everything currently claimed. Readable without asking any agent."""
        return [c for c in self._items.values() if c.claimed]

    def show(self) -> str:
        if not self._items:
            return "(empty)"
        rows = [f"{'task':<12} {'state':<12} {'owner':<10} {'tries':<6} notes"]
        for c in self._items.values():
            owner = c.owner or "-"
            note = (c.notes.splitlines()[-1][:34] if c.notes else "")
            rows.append(f"{c.task_id:<12} {c.state:<12} {owner:<10} {c.attempts:<6} {note}")
        return "\n".join(rows)


def _demo() -> None:
    """Claim a task, lose the worker, recover from the record."""
    path = Path(__file__).with_name("worklist.demo.json")
    if path.exists():
        path.unlink()
    wl = Worklist(path)

    print("1. Add a task")
    wl.add("T-1", "Tailor resume for the backend role")
    print(wl.show())

    print("\n2. owner-7 claims it (short lease, for the demo)")
    wl.claim("T-1", owner="owner-7", lease_seconds=1)
    print(wl.show())

    print("\n3. owner-7 records partial progress, then dies")
    wl._items["T-1"].notes = "parsed JD; shortlisted 3 bullets"
    wl._save()
    print("   note persisted:", wl._items["T-1"].notes)

    print("\n4. A second owner tries to claim while the lease is live")
    got = wl.claim("T-1", owner="owner-9")
    print(f"   claim granted: {got}   <- False is correct; it is not available")

    print("\n5. Lease lapses (waiting)")
    time.sleep(1.1)
    expired = wl.expired()
    print(f"   expired: {[c.task_id for c in expired]}")

    print("\n6. owner-9 recovers, and reads what owner-7 learned")
    wl.claim("T-1", owner="owner-9", lease_seconds=900)
    print("   carried notes:", wl._items["T-1"].notes)
    print("   attempts:", wl._items["T-1"].attempts, "  <- attempt count survives too")
    print()
    print(wl.show())

    print("\n7. Done. The record, not the conversation, held the state.")
    path.unlink()


if __name__ == "__main__":
    _demo()

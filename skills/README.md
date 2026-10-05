# Skills

The same guidance, packaged as [Agent Skills](https://agentskills.io/) so it loads
in any compatible client — Claude Code, Codex, Cursor, and others — without cloning
this repository into the agent's working directory.

| Skill | Use when |
| --- | --- |
| `harness-design/` | Designing or auditing a harness that runs unattended |
| `self-evolving-loop/` | A harness must maintain its own knowledge and rules |

Each is a folder with a `SKILL.md` holding metadata and instructions. The agent loads
only the name and description until a task matches, then reads the full file. That
keeps many skills available with a small context footprint.

## Installing

Copy a folder into your client's skills directory, or point the client at this
directory if it supports a skills root.

Because the format is an open standard, the same folder works across clients. If
your client does not support skills, the equivalent content is in `docs/` as prose.

## Relationship to the docs

These are not summaries of the docs and do not replace them. Each skill is scoped to
a decision an agent makes mid-task — whether a hierarchy is warranted, whether a
handoff is a relay, whether a learning loop's guardrails are in place — and is
written to be actionable in that moment.

The documents are the arguments. The skills are the checks.

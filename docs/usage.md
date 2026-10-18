# Using the library

Install only what the task needs. Agent hosts normally read the name and
description first, then load `SKILL.md` when relevant. The entrypoint routes to
specific references. Ask for a skill by name if automatic selection misses it.
Do not load every reference for every task.

## Choose the entrypoint

| Task | Start here | Add if needed |
| --- | --- | --- |
| Duplicate charges after message replay | distributed-systems | production-reliability for deadlines and retry traffic |
| High Linux p99 | linux-performance | systems-profiling after selecting the event/time basis |
| Split a service | architecture-tradeoffs | architecture-patterns for measurable quality scenarios |
| Database write stalls | database-internals | linux-performance for host/device evidence |
| Race or unsafe publication | concurrent-programming | systems-programming for memory/I/O ownership |
| Too many network round trips | network-engineering | architecture-tradeoffs for boundary changes |
| Class hierarchy is hard to change | design-patterns | architecture-patterns if the issue spans deployment/module boundaries |

Each skill is independently installable. Related skills are optional; all required
references are inside the selected folder.

## Ask for a reviewable result

Provide the real code/configuration and relevant constraints, then ask for an
artifact you can inspect:

```text
Use production-reliability on this client wrapper. Our request deadline is
800 ms; payments may time out after committing. Show the retry ownership,
unknown-outcome behavior, resource limits, and tests for each failure window.
```

```text
Use database-internals. Compare our B-tree and LSM candidates for the attached
workload. Include sustained compaction/checkpoint costs, range-query behavior,
durability settings, and the benchmark that would change your recommendation.
```

```text
Use concurrent-programming. Find a concrete failing schedule for this code.
Separate visibility, atomicity, linearizability, and progress. Recommend the
smallest correct mechanism, with platform assumptions and meaningful checks.
```

Ask the agent to cite the reference it used and label unknowns. The library
cannot supply facts about your database version, kernel, deployment, or workload
that you have not measured or provided.

## Project-local installation

From outside the library checkout, choose an agent project root and run:

```sh
python3 /path/to/skills/scripts/install.py --dest /path/to/project/.agents/skills --skill network-engineering
```

For Claude Code use `.claude/skills`; for Copilot use `.github/skills`; for OpenCode
use `.opencode/skills`. Commit those copied folders if the project should share
them. Restart the agent session and verify the skill appears through that host's
skill discovery UI/command. Installation roots and trust settings can change;
consult the host's current documentation if discovery differs.

The local installer intentionally refuses existing targets. Review updates in a
separate destination, then merge the desired changes through your normal source
control process. It does not synchronize or delete a user's existing library.

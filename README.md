# Engineering skills

Practical engineering knowledge for coding agents: review a message-processing
contract, investigate Linux latency, choose a storage engine, or test an
architecture decision.

Each skill starts with a short decision procedure. Deeper mechanisms, original
examples, failure cases, and exercises live in references loaded only when needed.
The library follows the [Agent Skills format](https://agentskills.io/specification).

## Install

Pick the skills you need:

```sh
npx skills add karlem/skills --skill distributed-systems linux-performance
```

Or browse the available skills:

```sh
npx skills add karlem/skills --list
```

For a local install without Node.js:

```sh
git clone https://github.com/karlem/skills.git
cd skills
python3 scripts/install.py --dest ~/.agents/skills --skill distributed-systems linux-performance
```

Use `--all` instead of `--skill …` to install the library. The installer copies
complete skill folders into a flat agent root and refuses to overwrite existing
skills. Add `--dry-run` to preview. If the repository is private, authenticate
GitHub before cloning.

| Agent | Personal skill root |
| --- | --- |
| Codex | `~/.agents/skills` |
| Claude Code | `~/.claude/skills` |
| GitHub Copilot CLI | `~/.copilot/skills` |
| OpenCode | `~/.config/opencode/skills` |

Pass the matching root to `--dest`, then start a new agent session. These are
portable Markdown skills: no agent plug-in, background service, model key, or
runtime package is required. Format checks cover these hosts; a live discovery
test in every host has not been performed. See [usage](docs/usage.md) for
project-local installation and examples.

## Library

| Skill | Use it for |
| --- | --- |
| [distributed-systems](architecture/distributed-systems/SKILL.md) | Replication, consistency, crash windows, ordering, deduplication |
| [linux-performance](performance/linux-performance/SKILL.md) | p99 investigations, USE, pressure, quotas, benchmark design |
| [systems-profiling](performance/systems-profiling/SKILL.md) | CPU versus waiting time, flame graphs, profile interpretation |
| [architecture-tradeoffs](architecture/architecture-tradeoffs/SKILL.md) | Service boundaries, transaction placement, migration decisions |
| [database-internals](databases/database-internals/SKILL.md) | B-tree/LSM trade-offs, amplification, WAL and checkpoints |
| [systems-programming](engineering/systems-programming/SKILL.md) | C arithmetic, memory lifetime, partial I/O, locality |
| [production-reliability](reliability/production-reliability/SKILL.md) | Deadlines, retries, bulkheads, backpressure, recovery |
| [concurrent-programming](concurrency/concurrent-programming/SKILL.md) | Races, histories, publication, progress, reclamation |
| [architecture-patterns](architecture/architecture-patterns/SKILL.md) | Quality scenarios, architecture selection, fitness checks |
| [design-patterns](engineering/design-patterns/SKILL.md) | Variation, behavioral contracts, compatible product families |
| [network-engineering](networking/network-engineering/SKILL.md) | RTT/BDP budgets, transport contracts, forwarding and path diagnosis |

Ask your agent, for example:

> Use distributed-systems to review this consumer. Show crash windows, the exact
> invariant, and a replay-safe implementation before recommending changes.

> Use linux-performance to investigate these p99 spikes. Give competing
> hypotheses, the next measurements, and a controlled validation plan.

## Sources and coverage

All ten requested books have a coverage record. **Coverage is partial for every
book.** No authorized full edition was available; the skills use official samples,
author materials, research papers, standards, and implementation documentation.
They contain original engineering procedures rather than chapter reproductions.

- [Book coverage](sources/README.md): editions, available material, precise gaps.
- [Source manifest](sources/manifest.json): URLs, access status, dates, hashes,
  extraction methods, and acquisition issues.
- [Conversion workflow](docs/conversion.md): verified use of
  [book-to-skill](https://github.com/virgiliojr94/book-to-skill), its limits, and the
  supplementary extraction path.

## Validation

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The checks cover structure, local links, provenance, installation behavior, and
selected engineering mechanisms. [Evaluation scenarios](evaluations/README.md)
include prompts, acceptance criteria, reviewed responses, and executable checks.
They do not establish a measured improvement in model performance.

See the [completion report](docs/report.md) and [execution log](docs/execution-log.md)
for results and remaining limits. Contributions are welcome through pull requests;
read [CONTRIBUTING.md](CONTRIBUTING.md).

[MIT](LICENSE) applies to original repository content. Source books and linked
materials retain their own rights and licenses. No books, extracted source text,
slides, or publisher diagrams are included.

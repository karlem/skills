# Contributing

Start with a real engineering decision or debugging problem. Add a small skill
or improve an existing procedure; move detailed mechanisms and worked examples
into `references/`. Keep each skill independently usable after installation.

1. Add authoritative source URLs and access/coverage details to
   `sources/manifest.json`. A publisher listing verifies a title, not a technical claim.
2. Write in your own words. Do not submit books, extracted text, copied diagrams,
   publisher examples, or close chapter-by-chapter reproductions. Public access
   does not grant redistribution rights. The repository's MIT license applies
   to original contributions only.
3. Add a realistic scenario, expected decisions, and disqualifying mistakes to
   `evaluations/cases.json`. Tie any executable check to a meaningful invariant.
4. Run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`.
5. Open a pull request with the problem, change, evidence, and coverage limits.

Frontmatter uses only `name` and `description`; names match their directories.
Write descriptions with concrete trigger conditions. Keep `SKILL.md` below
2,000 words and 150 lines. Link every supporting reference from that entrypoint.
Do not require another installed skill to understand a core procedure.

Mark recommendations as heuristics when they depend on workload or operating
conditions. State the system model for guarantees. Benchmarks need units, load,
measurement boundaries, and a reproducible method. Never present a checklist
or a deterministic exercise as evidence of improved model performance.

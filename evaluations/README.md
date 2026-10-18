# Evaluation scenarios

Every skill has a realistic scenario in [cases.json](cases.json), with acceptance
criteria, disqualifying mistakes, an original reviewed response, and links by
name to executable exercises. [Reviewed responses](reviewed-responses.md) show
the reasoning used during development.

[Claim audit](claim-audit.json) records primary-source checks for significant
mechanisms. [Discovery results](discovery-results.json) record external CLI discovery.

## What was evaluated

- Structure, routing links, source/coverage completeness, and self-contained installs.
- Selected mechanisms with deterministic exercises: transaction/replay windows,
  quota exhaustion, profile normalization, dependency failure propagation,
  Bloom filters, a real SQLite WAL checkpoint pinned by a reader, C arithmetic
  and partial writes, retry budgets, bounded interleavings, dependency rules,
  compatible product bundles, and network budget/prefix calculations.
- Single-author editorial review of all 11 responses against the stated criteria.

The exercises include flawed-design counterexamples so they can detect meaningful
mistakes. They do not simulate full production systems. Closing an uncommitted
SQLite transaction models a crash window, not power loss. The quota and dependency
models are deliberately small. The dependency fixture tests rule semantics, not
an actual codebase scanner.

## What was not measured

No independent or blinded agent evaluation, baseline-versus-skill experiment,
statistical uplift, or live incident outcome is claimed. The current session was
the author and reviewer; a second model was not invoked. Rubric coverage is useful
review evidence but cannot establish that an agent becomes more accurate.

## Reproduce checks

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Python 3.10+ is sufficient for library validation and most exercises. C example
checks need a C11 compiler (`cc`). Optional HTML cleanup tests need
`beautifulsoup4`; absent optional tools are reported as skipped tests. Research
reproduction uses the separate pinned requirements in `sources/requirements.txt`.

## Run a future paired agent evaluation

1. Freeze repository commit, cases, model/version, system prompt, tool policy,
   run count, and maximum cost before starting.
2. Give the baseline only the case prompt and the same project artifacts. Give
   the assisted condition the selected skill and only references it requests.
   Keep tools, runtime budget, and external evidence availability equal.
3. Run cases in fresh contexts, randomize condition order, and retain outputs and
   actual loaded paths. Do not let the baseline read the library through tools.
4. Have an independent reviewer score each criterion 0 (wrong/missing), 1
   (partial), or 2 (correct and applied). Any disqualifying mistake fails the case.
5. Report correctness, decision quality, technical depth, unnecessary assumptions,
   token/time cost, and variability across repeated runs. Include regressions.
6. Refine the smallest weak procedure, then rerun affected cases. Do not publish
   cherry-picked wins or compare different source/tool access as a skill-only effect.

Store future model outputs separately from the current editorial records and label
their exact provenance. Do not replace observed results with intended outcomes.

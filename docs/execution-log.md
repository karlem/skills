# Execution log

Work date: 2026-10-18. Target: `karlem/skills`; starting commit `7356d2f`.
Work branch: `feat/engineering-knowledge-library`.

## Repository and tool inspection

- GitHub CLI authenticated as `karlem`; selected that account's `skills` repository.
- Repository contained only its initial README, with no existing skills or local
  contribution instructions. Preserved the initial history and repository visibility.
- Cloned `virgiliojr94/book-to-skill`, inspected README/docs/generator/parsers/
  validation code, and installed version 1.4.0 at the pinned commit in an isolated
  virtual environment. Verified the CLI is extraction-only.
- Verified PDF/EPUB/HTML capabilities with `--check`. Used available Poppler and
  optional pypdf/BeautifulSoup; did not install heavyweight Docling/OCR/Calibre.

## Source acquisition

- Searched publisher and author sites for all ten books. No authorized full book
  was present locally or found for unrestricted processing. Did not use unauthorized
  mirrors, bypass access controls, purchase books, or start subscription trials.
- Retrieved official performance/architecture/reliability samples, author course
  notes, author interviews/pages, official networking slides, research papers,
  standards, and implementation documentation.
- Recorded public evidence with original/final URLs, observed access, byte hashes,
  dates, exact topic coverage, license/access notes, and failed acquisition attempts.
- Direct Elsevier/ScienceDirect requests were denied; used public publisher catalogue
  metadata and author papers. CS:APP guessed sample URL returned 404; some linked
  preface/code requests were denied. No restricted instructor files were requested.

## Extraction findings and refinements

- Ran book-to-skill on public PDF/HTML sources and checked actual source identity.
- Detected JavaScript/navigation residue in HTML; supplied a cleanup pass rather
  than treating an HTTP success or parser success as technical coverage.
- Corrected the performance sample from an assumed CPU chapter to the actually
  retrieved Operating Systems chapter. Detected 80 spurious chapter headings from
  page headers/contents/index; omitted auto-counts from coverage claims.
- Tested that PPTX is rejected. Added ZIP/XML slide text in numeric order, then
  processed all eight ninth-edition decks as Markdown through book-to-skill.
  Do not infer diagram/animation fidelity from successful extraction.
- Restricted Design Patterns claims to the actual Abstract Factory excerpt and
  author discussion; other patterns receive explicitly limited orientation.
- Kept distributed effect atomicity separate from reliability's retry/resource
  policy, and performance triage separate from profile interpretation.

## Implementation and review

- Created 11 independently installable skills, each with focused technical
  references and an attribution/coverage file.
- Added a no-overwrite selective installer, offline validator, research helper,
  pinned upstream-check wrapper, and CI workflow.
- Added 11 realistic scenarios, disqualifying mistakes, and original reviewed
  responses. Review was performed by the author in this session, not independently.
- Added executable mechanisms/counterexamples and compile-and-run checks for
  original C examples. See evaluation artifacts for actual final results.
- An initial test run passed mechanism checks and identified four not-yet-written
  documentation links; those documents were then completed before final validation.

## Validation and publication

- Relevant upstream tests: 94 passed (format validator, content scanner, HTML
  boundaries, PDF page numbers, chapter samples).
- Upstream host checks and full Markdown scans: recorded in
  `evaluations/upstream-results.json`.
- Local final checks and environment details: recorded in `evaluations/results.json`.
- Installation/discovery evidence and remaining limitations: see `report.md`.
- Logical commits preserve the source foundation with priority skills, remaining
  subjects, and final tooling/evaluations/docs. Publication uses a branch and pull request;
  no force push or existing-skill overwrite.

## Unresolved issues

- Full authorized editions are absent for all ten books; every conversion is partial.
- Source URLs may change. Some dynamic metadata contains future-dated listings;
  no future lesson content is used as evidence.
- Diagrams, animations, speaker notes, unread chapters and embedded videos are
  outside verified extraction coverage.
- No baseline/assisted live-model comparison or independent review was performed.
- Format compatibility does not establish live discovery in every supported host.

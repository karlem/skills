# Conversion and editorial workflow

## Primary tool

The library uses [book-to-skill](https://github.com/virgiliojr94/book-to-skill) at
commit `a24e62f4d8caf2ee433f6e48d9073800f56f906e` (package version 1.4.0).
Its README, generator skill, architecture/install/how-it-works documentation,
format parsers, CLI/configuration, validation tools, and relevant tests were
inspected before conversion.

The project has two parts:

1. A deterministic Python extractor writes `full_text.txt` and `metadata.json`.
2. An agent follows the generation specification to create decision-oriented
   content with selective supporting files. There is no automatic LLM generation
   API in the standalone CLI.

Supported inputs include EPUB, PDF, HTML, DOCX, RTF, plain text/Markdown/RST/AsciiDoc,
and MOBI/AZW/AZW3 through Calibre. Text formats need no external extractor. EPUB
supports ebooklib/BeautifulSoup and a ZIP fallback. PDFs can use `pdftotext`, pypdf,
pdfminer, or optional structure-aware Docling. The tool also sanitizes extracted
text and can scan generated content for suspicious instructions.

## Verified behavior and limits

| Observation | Effect on this library |
| --- | --- |
| Official PDF samples extract selectable text through `pdftotext` | Used local text extraction with explicit source fingerprints |
| HTML metadata reports `html-parser`; output can retain scripts and navigation | Added a BeautifulSoup cleanup pass; inspected the technical sections |
| The performance sample's metadata reports 80 “chapters” from one chapter plus front matter/index | Did not use auto-detected headings as coverage evidence |
| Search/author overview wording suggested a CPU sample, but retrieved PDF contains Chapter 3 Operating Systems | Corrected attribution and supplemented profiling from author documentation |
| PPTX is rejected as unsupported | Added ordered slide-XML extraction, then fed Markdown to book-to-skill |
| PDF `images_dropped` can be unknown at source level while aggregate output says zero | No claim of diagram fidelity from those counters |
| Upstream scan covers `chapters/` and named support files, not `references/` | Scan every reference through a temporary `chapters/` mirror |
| CLI extraction does not produce a finished skill | Original editorial generation/review follows extraction |

Docling and OCR were not installed. The acquired PDFs already had selectable
text. Text extraction was sufficient for the selected mechanisms, with formulas
checked against independent definitions/calculations. Code examples and decision
tables in this repository are original; no extracted code/table/diagram is copied.
Images, slide animation order, speaker notes, and layout-dependent equations are
not treated as faithfully converted.

## Reproduce source extraction locally

Research dependencies are separate from skill usage:

```sh
python3 -m venv .venv
.venv/bin/pip install -r sources/requirements.txt
.venv/bin/python -m book_to_skill --check
.venv/bin/python scripts/research.py hardparts-sample --extract
.venv/bin/python scripts/research.py network-ch3 --extract
```

PDF reproduction uses `pdftotext` from Poppler when available and pypdf as a
fallback. The installed capabilities are reported by `--check`. Extraction
explicitly disables automatic dependency installation.

The source ID must be an observed public entry in `sources/manifest.json`.
Downloads and extracted text stay in ignored `.cache/research/`. Existing files
are not overwritten. Byte hashes are compared with the recorded snapshot; dynamic
HTML often changes, so a mismatch needs inspection rather than an assumption that
the source is identical. Access may change or disappear. The helper neither logs
in nor handles paywalls/DRM, and it cannot confer processing or publication rights.

PPTX extraction reads slide XML in numeric order and extracts visible text only.
HTML cleanup chooses an article/main region when available, removes scripts and
page chrome, then passes prepared Markdown into the primary extractor. Both
supplements have synthetic fixture checks. Inspect the prepared text and raw
source before using a formula, table, or code sample.

## Editorial generation

The book-to-skill generation specification supplies the principles: extract
mechanisms and decision rules, retain technical precision, and load depth only
when relevant. The requested public library determines the destination and shape:
short `SKILL.md`, focused `references/`, original worked examples, and explicit
coverage limits. Per-chapter reproductions, glossary duplication, copied code,
and publisher case studies are omitted.

For each topic:

1. Verify title/edition against the publisher or author.
2. Find a legitimate public excerpt, author material, or primary supplement.
3. Extract locally; check source identity and technical sections manually.
4. Write an original procedure around a real engineering decision.
5. Map significant claims to source IDs/locators and distinguish implementation
   behavior, mathematical model, guarantee, and workload-dependent heuristic.
6. Add a realistic evaluation case and meaningful counterexample/check.
7. Review and revise weak attribution or overly broad claims.
8. Validate formats, links, standalone installation, and all skill Markdown.

Public availability does not mean open licensing. All ten full-book conversions
remain incomplete; the source manifest explains each case. The repository's MIT
license covers its original content, not linked source material.

## Reproduce upstream checks

```sh
git clone https://github.com/virgiliojr94/book-to-skill.git /tmp/book-to-skill
git -C /tmp/book-to-skill checkout a24e62f4d8caf2ee433f6e48d9073800f56f906e
python3 scripts/upstream_checks.py /tmp/book-to-skill
```

This runs four host format lenses and one whole-skill content scan per skill.
The script checks the converter commit and writes
`evaluations/upstream-results.json`. These are syntax/advisory scans, not proofs
of technical accuracy or absence of all malicious instructions.

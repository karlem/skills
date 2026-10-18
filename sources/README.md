# Book coverage

All ten books are processed to explicitly partial coverage. No full authorized
edition was available. Each skill is original source-backed engineering guidance,
not a reproduction or a substitute for its source book.

| Priority / book | Edition | Skill | Public material used |
| --- | --- | --- | --- |
| 1. Designing Data-Intensive Applications | 2nd edition (2026) | [distributed-systems](../architecture/distributed-systems/SKILL.md) | Publisher contents; Kleppmann course notes and fencing article; PostgreSQL/outbox docs |
| 2. Systems Performance: Enterprise and the Cloud | 2nd edition (2020; copyright 2021) | [linux-performance](../performance/linux-performance/SKILL.md), [systems-profiling](../performance/systems-profiling/SKILL.md) | Official Operating Systems sample; author USE/profiling/benchmark docs; kernel PSI docs |
| 3. Software Architecture: The Hard Parts | 1st edition (2021) | [architecture-tradeoffs](../architecture/architecture-tradeoffs/SKILL.md) | Official Chapter 7; author companion; primary architecture/outbox articles |
| 4. Database Internals | 1st edition (2019) | [database-internals](../databases/database-internals/SKILL.md) | Publisher/author metadata; SQLite and RocksDB implementation docs |
| 5. Computer Systems: A Programmer’s Perspective | 3rd edition (2016) | [systems-programming](../engineering/systems-programming/SKILL.md) | Author companion/lab descriptions; POSIX read/write; SEI CERT C |
| 6. Release It! Design and Deploy Production-Ready Software | 2nd edition (2018) | [production-reliability](../reliability/production-reliability/SKILL.md) | Official Stability Antipatterns/Hosts excerpts; Amazon retry guidance |
| 7. The Art of Multiprocessor Programming | 2nd edition (2020) | [concurrent-programming](../concurrency/concurrent-programming/SKILL.md) | Publisher catalogue; Herlihy progress/linearizability papers; Java specification and reclamation docs |
| 8. Fundamentals of Software Architecture | 2nd edition (2025) | [architecture-patterns](../architecture/architecture-patterns/SKILL.md) | Author companion and interview; lesson-page descriptions; ArchUnit docs |
| 9. Design Patterns: Elements of Reusable Object-Oriented Software | 1st edition (1994) | [design-patterns](../engineering/design-patterns/SKILL.md) | Official Abstract Factory excerpt; Gamma interview |
| 10. Computer Networking: A Top-Down Approach | 9th edition (2025) | [network-engineering](../networking/network-engineering/SKILL.md) | All eight official ninth-edition slide decks; TCP and QUIC RFCs |

## Exact limits by book

### 1. Designing Data-Intensive Applications

Authors: Martin Kleppmann, Chris Riccomini.

Publisher offers commercial/full-access reading; no authorized full ebook was available in the environment or found for unrestricted processing. Used publisher contents for identity and public author course notes plus listed primary supplements for mechanisms.

Covered: Failure/ack boundaries, replication, consistency contracts, quorum caveats, ordering, fencing, replay-safe effects and outbox review.

Not covered: Full second-edition chapter text, analytics, encoding/schema evolution, stream processing and complete consensus algorithms.

### 2. Systems Performance: Enterprise and the Cloud

Authors: Brendan Gregg.

Commercial full edition not available; official sample contains Chapter 3 Operating Systems plus front matter/index. Author web documentation supplies performance methods and profiling details. Sample TOC/index entries are not treated as chapter coverage.

Covered: USE investigation, OS context, CPU/waiting profiles, benchmark design, resource pressure and original container scenarios.

Not covered: Full book, CPU chapter prose, BPF/Ftrace chapters, exhaustive hardware/storage tuning.

### 3. Software Architecture: The Hard Parts

Authors: Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani.

No authorized full edition available; used official Thoughtworks-hosted Chapter 7 and primary architecture/outbox articles. Migration procedures are original supplemental guidance, not claimed book content.

Covered: Chapter 7 service granularity forces; original boundary/migration worksheets with primary supplements.

Not covered: Other book chapters, book case studies, full data architecture and saga taxonomy.

### 4. Database Internals

Authors: Alex Petrov.

Commercial publisher edition not available; author landing page and publisher contents do not provide full text. Technical coverage comes from SQLite and RocksDB primary documentation, clearly labeled as implementations rather than a book conversion.

Covered: B-tree/LSM selection, amplification, Bloom filtering, WAL/checkpoint and recovery review.

Not covered: Full book, engine implementation, complete distributed algorithms and recovery algorithms.

### 5. Computer Systems: A Programmer’s Perspective

Authors: Randal E. Bryant, David R. O’Hallaron.

No authorized full edition available. Public author companion pages were accessible; guessed 3e sample URL returned 404 and preface/code-file requests were denied. Used public resource descriptions, POSIX and SEI CERT; no restricted instructor files acquired.

Covered: Allocation arithmetic, ownership/lifetime, cache locality, partial I/O and process/descriptor review.

Not covered: Full book, processor design, detailed assembly, linking and virtual memory; lab solutions.

### 6. Release It! Design and Deploy Production-Ready Software

Authors: Michael T. Nygard.

Publisher offers paid full edition; official Stability Antipatterns and Hosts excerpts are public. Retry details supplemented by Amazon primary guidance. No complete-book conversion claimed.

Covered: Failure propagation, resource containment, deadlines, retry budgets, idempotency, breaker/bulkhead review and recovery drills.

Not covered: Full book, complete stability pattern catalogue and case histories.

### 7. The Art of Multiprocessor Programming

Authors: Maurice Herlihy, Nir Shavit, Victor Luchangco, Michael Spear.

No authorized full edition available. Direct Elsevier title and ScienceDirect endpoints were denied; publisher catalogue and search metadata confirm edition. Used author-hosted Herlihy/Wing paper and official Java/reclamation documentation; this is original subject coverage.

Covered: Linearizable histories, happens-before, races, progress distinctions, ABA and reclamation review.

Not covered: Full second-edition text, complete algorithms/proofs, transactional memory and language-specific lock-free implementations.

### 8. Fundamentals of Software Architecture

Authors: Mark Richards, Neal Ford.

Full publisher edition requires commercial access. Used author companion/pages, a public first-edition-era interview transcript, and ArchUnit docs. Lesson page descriptions were read; videos were not watched/transcribed. Second-edition-specific details beyond contents are not claimed.

Covered: Measurable quality scenarios, conditional style selection, coupling and fitness checks.

Not covered: Full second-edition chapters, complete style catalogue and leadership/negotiation treatment.

### 9. Design Patterns: Elements of Reusable Object-Oriented Software

Authors: Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

No authorized full edition available; official Abstract Factory excerpt and author interview were accessible. Other pattern names receive limited orientation, not a complete book conversion.

Covered: Abstract Factory applicability/trade-offs, behavioral interfaces/composition, original small family-construction example.

Not covered: Full 23-pattern treatment, publisher examples/diagrams, complete pattern relationships.

### 10. Computer Networking: A Top-Down Approach

Authors: James F. Kurose, Keith W. Ross.

No authorized full textbook available; official ninth-edition slides are public. PPTX unsupported by book-to-skill, so ordered XML slide text was converted to Markdown then passed through its extractor. Current TCP/QUIC RFCs supplement transport semantics.

Covered: All eight author slide decks processed; selected original procedures on delay/BDP, application/transport contracts, forwarding/routing, LAN/wireless and network security diagnosis.

Not covered: Full textbook prose/exercises, diagrams/animations and complete routing/wireless/security implementations.

## Records and reproduction

[manifest.json](manifest.json) records URLs, access dates/status, byte fingerprints,
extraction methods, and acquisition failures. Each installed skill carries its
own `references/sources.md` so attribution survives selective installation.

Only original notes, procedures, examples, and metadata are committed. Raw books,
excerpts, slide decks, and extracted text remain outside Git. Source licenses do
not become the repository license. See [conversion](../docs/conversion.md) for
the exact workflow and [requirements.txt](requirements.txt) for optional research dependencies.

# Scenario review records

Date: 2026-10-18. Method: single-author, skill-assisted editorial review.
These are original responses produced while developing the skills and checked
against the listed criteria and primary sources. They are not independent model
runs, blinded scores, or a baseline comparison. Executable evidence checks
selected mechanisms only; it does not score response quality.

## D1 — distributed-systems

**Scenario:** A broker redelivers invoices. The worker inserts a processed-event marker, commits it, charges a provider, then acknowledges. It can crash after any step. The provider may commit but lose its response. Propose a correctness contract and recovery plan.

**Reviewed response:** The early marker can suppress a charge that never happened. Reversing the two commits permits duplicate charges. For a local ledger, put its unique consumer/event marker and effect in one transaction, then acknowledge. For the provider, persist an intended operation key and pending status, use the provider’s durable idempotency contract, and reconcile a timeout before changing identity. Test crashes after every durable boundary, two workers receiving the same event, and replay beyond a deployment/restore. If the provider cannot deduplicate or reveal prior outcomes, state that arbitrary-crash completion plus at-most-one external charge cannot be guaranteed by the local database. Retention and restore policies must preserve operation identity.

**Review checks:**

- Covered: Find marker-before-effect loss and effect-before-marker duplication windows
- Covered: Keep database effect and dedup marker atomic where they share a transaction
- Covered: Do not claim local transaction makes provider charge atomic
- Covered: Reuse stable provider operation key and reconcile unknown outcomes
- Covered: Include concurrent duplicate delivery and retention/replay horizon

**Disqualifying mistakes checked:**

- Absent in this response: Claims broker exactly-once covers provider
- Absent in this response: Acknowledges before durable effect without an explicit loss policy

## P1 — linux-performance

**Scenario:** A Linux container on an eight-CPU host has p99 spikes, 60% host idle CPU, quota 100000 µs per 100000 µs period, and rising throttling counters. Offered rate is 1000/s and mean response time is 80 ms. Explain next measurements and what can be inferred.

**Reviewed response:** The quota permits one CPU on average across a period, even while the host has spare CPU. Several threads may spend that budget early and wait for replenishment. Correlate quota/stat deltas, runnable delay, request spans, and pressure with the spike; also check pool and downstream waiting before claiming causality. At a stable matched boundary the mean in-flight work is 1000 × 0.080 = 80. This is neither a p99 estimate nor a sufficient worker count. Compare reduced CPU work/concurrency or additional quota under the same offered load, with queue growth, errors, useful throughput, and tail latency recorded. The executable quota model demonstrates plausibility, not diagnosis of a real host.

**Review checks:**

- Covered: Inspect cgroup quota and interval throttling counters rather than host averages
- Covered: Check runnable delay, pool/downstream waits, and per-CPU skew
- Covered: Infer one CPU average quota, not eight CPUs of guaranteed capacity
- Covered: Use Little’s law only for means and matched steady-state boundary
- Covered: Propose matched-load before/after validation including errors and queue growth

**Disqualifying mistakes checked:**

- Absent in this response: Rules out CPU limitation because host is idle
- Absent in this response: Uses p99 in Little’s law as an exact sizing rule

## P2 — systems-profiling

**Scenario:** At 400 useful requests/s a baseline uses 2 CPU-seconds/s, 40% in encoding. A candidate uses 1.2 CPU-seconds/s, 60% in encoding. An engineer wants to revert because encoding grew. A request also waits 180 ms for a pool. Review the claim.

**Reviewed response:** Encoding’s approximate CPU demand fell from 2 × 0.40 = 0.8 to 1.2 × 0.60 = 0.72 CPU-seconds/s; its relative share rose because other work shrank more. Verify comparable capture events, symbols, duration/rate, and lost samples before relying on that estimate. Flame-graph width is aggregate event weight; height is call depth. The 180 ms pool wait needs acquisition histograms, queue/occupancy evidence, request spans, and possibly off-CPU data. Optimize the mechanism dominating the user-facing target, then compare latency and useful throughput at the original offered load. A compositional CPU percentage alone does not justify reverting.

**Review checks:**

- Covered: Normalize profile proportions to absolute CPU at matched load
- Covered: Calculate 0.8 versus 0.72 CPU-seconds/s
- Covered: Do not interpret stack height as duration
- Covered: Select waiting-time/pool evidence for the 180 ms wait
- Covered: Check event, symbols, sample loss, and configuration comparability

**Disqualifying mistakes checked:**

- Absent in this response: Treats higher percentage as higher absolute CPU
- Absent in this response: Expects CPU profile to account for all blocked request time

## A1 — architecture-tradeoffs

**Scenario:** Checkout reserves stock and accepts orders atomically. Recommendations may be absent. A proposal splits validation, stock, order creation, and recommendations into four mandatory synchronous services. All must deploy together. Review boundaries and migration.

**Reviewed response:** The proposal creates remote coordination around an existing atomic invariant and makes optional recommendations a critical dependency. Start by measuring independent change/scale needs. Keep stock/order acceptance local unless an explicit reservation protocol earns its complexity; separate recommendations only with a bounded failure path that permits checkout to continue. Lockstep deployment shows unresolved contract/data coupling. Compare this with stronger internal modules. Migrate by isolating the interface, choosing one authoritative writer, expanding compatible contracts, checkpointing/backfilling and reconciling data, then shifting traffic gradually. Shadow only safe work. Define where rollback ceases to be safe after schema/data changes. Do not count process separation as proven failure isolation.

**Review checks:**

- Covered: Place stock/order invariant explicitly
- Covered: Challenge mandatory optional dependency and coordinated releases
- Covered: Balance independent scale/change against transaction/chatty workflow costs
- Covered: Compare improved in-process modules with remote extraction
- Covered: Give staged ownership, contract compatibility, reconciliation and rollback

**Disqualifying mistakes checked:**

- Absent in this response: Assumes more services improve architecture automatically
- Absent in this response: Claims saga compensation is database rollback

## B1 — database-internals

**Scenario:** A telemetry engine must absorb write bursts and support range queries. An LSM benchmark on an empty database wins. Disk later fills with compaction backlog. A separate SQLite service has a growing WAL despite frequent checkpoints. Review both.

**Reviewed response:** The empty-database result omits maintenance debt. Repeat through sustained flush/compaction and burst recovery, measuring bytes written per logical byte, live/temporary disk use, p99, stalls, and realistic range queries. Compare a B-tree candidate with the same workload and durability. Reserve maintenance space/I/O based on evidence rather than selecting by peak ingest. For SQLite, inspect active read snapshots and checkpoint results: an old reader can pin WAL progress, so increasing checkpoint frequency may not reclaim it. Release/bound readers through the application protocol and use supported backup/checkpoint mechanisms; never delete a live WAL. Confirm synchronization settings and the failure model before claiming power-loss durability.

**Review checks:**

- Covered: Measure steady-state amplification, compaction stalls and free-space headroom
- Covered: Include range queries, skew, secondary indexes, updates/deletes and cache state
- Covered: Do not universally prefer LSM or B-tree
- Covered: Inspect long-lived SQLite readers and checkpoint progress
- Covered: Distinguish durable log synchronization from write return and process kill

**Disqualifying mistakes checked:**

- Absent in this response: Deletes a live WAL to recover disk space
- Absent in this response: Assumes Bloom filter proves a key exists or eliminates range scan work

## S1 — systems-programming

**Scenario:** A C server allocates count * width bytes, then reads a length-prefixed request in one read and writes the reply once. count is signed input. Explain safety fixes and validation.

**Reviewed response:** Validate the parsed count as nonnegative and within an application bound before conversion. Guard multiplication by division before computing it; define zero-width behavior and check allocation failure. Keep a parser across reads, bound the advertised length before allocation, distinguish short progress from EOF, and reject truncated frames. Track output offset through short writes and EINTR; for nonblocking sockets, retain state and wait for readiness under a total deadline. Define SIGPIPE policy and transfer-size limits. Preserve buffer lifetime until completion and report partial progress on failure as needed. Compile the original examples with warnings and exercise boundary sizes plus injected short transfers/interruption; those checks do not constitute complete server validation.

**Review checks:**

- Covered: Validate signed input before size_t conversion
- Covered: Check count > SIZE_MAX / width before multiplication with zero-width policy
- Covered: Handle partial reads/writes, EOF, EINTR and framing state
- Covered: Handle EAGAIN through readiness/deadlines rather than spinning
- Covered: State ownership, SIGPIPE, size limits and partial-progress limitations

**Disqualifying mistakes checked:**

- Absent in this response: Checks multiplication overflow after wrapping
- Absent in this response: Treats positive short read as complete frame or EOF

## R1 — production-reliability

**Scenario:** Five call layers each make three total attempts. A dependency hangs for 30 seconds, occupying all workers. A breaker opens but heap use still grows. Propose bounded failure and recovery behavior.

**Reviewed response:** Three total attempts at five layers can produce 243 leaf attempts. Select a retry-owning layer and cap combined attempts/traffic within the remaining end-to-end deadline. Include pool, DNS/setup, and body waits in the actual timer contract. Preserve operation identity when effects may already have committed. A breaker prevents some new calls but does not bound pending futures, waiter queues, or already running calls. Add finite dependency concurrency, bounded queue age/length, admission rejection, and cancellation handling. Inspect retained buffers/tasks behind heap growth. Bound and spread half-open probes and ramp recovered traffic. Drill slow, failed, and recovering dependencies while checking critical useful throughput and finite resource usage.

**Review checks:**

- Covered: Calculate 243 possible leaf attempts and assign one retry owner/budget
- Covered: Propagate total deadline including pool/setup waits
- Covered: Require safe operation identity/reconciliation before ambiguous retries
- Covered: Bound active calls AND queued work with admission/bulkheads
- Covered: Limit/spread half-open probes and test recovery/backlog drain

**Disqualifying mistakes checked:**

- Absent in this response: Assumes backoff alone bounds total retries/resources
- Absent in this response: Assumes circuit breaker provides queue/concurrency limits

## C1 — concurrent-programming

**Scenario:** Two Java threads increment a volatile integer. A custom CAS stack frees popped nodes immediately and claims wait freedom. Diagnose correctness and progress issues.

**Reviewed response:** A and B can each read zero, then each write one. Java volatile supplies ordering/visibility, not an indivisible read-modify-write. Use an atomic increment for an independent counter or a lock for a larger invariant. For the stack, another thread may already hold the popped pointer when it is freed; CAS does not protect its earlier dereference. Review safe reclamation separately from ABA/version checks. A retrying CAS algorithm may be lock-free but starve one operation; a wait-free claim needs a bound on each operation’s own steps under an explicit model. Include allocator, reclamation, and scheduler limitations. Check bounded histories against the object specification and use race/stress tooling without treating a passing run as proof.

**Review checks:**

- Covered: Show lost-update interleaving and distinguish volatile from atomic compound update
- Covered: Choose atomic increment or lock for the full invariant
- Covered: Separate linearizability from race freedom and local CAS atomicity
- Covered: Find use-after-free/reclamation and distinguish ABA
- Covered: Reject wait-free claim without bounded per-operation steps and runtime assumptions

**Disqualifying mistakes checked:**

- Absent in this response: Says volatile makes increment atomic
- Absent in this response: Says using CAS automatically makes stack safe/wait-free

## A2 — architecture-patterns

**Scenario:** A six-person team proposes 18 microservices for scalability. Its measured bottleneck is one SQL query. Define a conditional architecture choice and two meaningful fitness checks.

**Reviewed response:** Define offered workload, payloads, p99/error targets, and recovery constraints. First test query/index/access-path fixes and stronger modules in the existing deployment; 18 deployments do not inherently repair one query. Compare extraction only where independent scale, change, or containment is demonstrated and operable by the team. A dependency check can forbid checkout domain imports of a vendor SDK while permitting an adapter. A runtime check can overload recommendations and verify bounded checkout latency/errors. The first misses dynamic/runtime coupling; the second covers only the tested load/failure. Record an ADR and revisit when a measured capability needs independent capacity/ownership or coordinated releases prevent required delivery.

**Review checks:**

- Covered: Translate scalability into a workload/latency scenario
- Covered: Compare a modular single deployment and fix the measured query
- Covered: Include operational/team and transaction/ownership costs
- Covered: Add dependency and runtime quality checks with explicit blind spots
- Covered: Define an observable trigger to reconsider extraction

**Disqualifying mistakes checked:**

- Absent in this response: Treats microservices as mandatory maturity stage
- Absent in this response: Treats static import test as proof of runtime availability

## O1 — design-patterns

**Scenario:** A reporting tool permits callers to independently select renderer and style families, producing invalid combinations. Another proposal replaces two simple functions with five interfaces and a global registry. Review both.

**Reviewed response:** Select a complete compatible family at one composition boundary and inject the bundle. A small constructor suffices for two families; a full Abstract Factory collaboration becomes useful when several related products vary together. Keep family identity in the assembled bundle or types so callers cannot reintroduce mixing. New families can be localized, but adding a product kind may require changing every provider. Reject the five-interface/global-registry proposal unless it solves a demonstrated extension or lifecycle need; two functions may express the contract adequately. Test both families, unknown selection, compatibility, and partial-construction cleanup. Pattern names describe a collaboration; they do not justify machinery by themselves.

**Review checks:**

- Covered: Identify compatible-product-family invariant
- Covered: Use one family selection/bundle or appropriate Abstract Factory
- Covered: Explain new-family versus new-product-kind asymmetry
- Covered: Prefer function/composition when variation is small
- Covered: Check behavioral contract, resource cleanup and invalid family tests

**Disqualifying mistakes checked:**

- Absent in this response: Adds hierarchy solely to maximize named patterns
- Absent in this response: Assumes factory naming alone prevents invalid combinations

## N1 — network-engineering

**Scenario:** A request sends 2 KiB through five serial RPCs at 30 ms RTT each. The path is 100 Mbit/s with 80 ms RTT for bulk transfer and a 64 KiB effective in-flight cap. A team wants a faster NIC and claims TCP acknowledgments prove payments committed. Review.

**Reviewed response:** Five full serial RTTs contribute about 150 ms if connections are reused and payload/setup costs are negligible. A faster NIC barely changes propagation/round-trip delay; inspect batching, co-location, and protocol chattiness. For the separate bulk path, BDP is 100000000 × 0.080 / 8 = 1000000 bytes. A 65536-byte effective in-flight cap bounds idealized throughput near 819200 bytes/s before overhead/loss. Check congestion/receive windows and application progress rather than merely increasing buffers. TCP ACKs do not prove the server application committed payment state, so use operation identity and reconciliation. TCP frames bytes, not messages. QUIC can avoid cross-stream delivery blocking but still shares congestion/path limits; measure cold/warm and impaired paths.

**Review checks:**

- Covered: Estimate about 150 ms serial communication under explicit reuse/no-setup assumptions
- Covered: Compute BDP as 1000000 bytes and cap-bound throughput as 819200 bytes/s
- Covered: Investigate pooling/batching/locality versus bandwidth constraint
- Covered: Distinguish transport receipt from business commit and stream framing
- Covered: State QUIC stream/shared-congestion limits and validate actual path

**Disqualifying mistakes checked:**

- Absent in this response: Treats ACK as durable business commit
- Absent in this response: Says QUIC eliminates all blocking or faster NIC fixes RTT-bound calls

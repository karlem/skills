"""Executable exercises. These test selected mechanisms, not agent response quality."""
import hashlib
import importlib.util
import itertools
import json
import math
import re
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
from ipaddress import ip_address, ip_network
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def code(relative, language):
    text = (ROOT / relative).read_text()
    return re.search(rf'```{language}\n(.*?)\n```', text, re.S)[1]


class EngineeringExercises(unittest.TestCase):
    def test_distributed_crash_windows(self):
        # Durable reopen + transaction-close fault model, not physical power loss.
        for crash in ('before', 'marker', 'effect', 'committed', None):
            with self.subTest(crash=crash), tempfile.TemporaryDirectory() as tmp:
                path = str(Path(tmp) / 'ledger.db')
                with sqlite3.connect(path) as db:
                    db.executescript('CREATE TABLE seen(id TEXT PRIMARY KEY); CREATE TABLE account(n INTEGER); INSERT INTO account VALUES(0);')
                def process(cut):
                    db = sqlite3.connect(path)
                    try:
                        if cut == 'before':
                            return
                        db.execute('BEGIN')
                        inserted = db.execute("INSERT OR IGNORE INTO seen VALUES('e1')").rowcount
                        if cut == 'marker':
                            return
                        if inserted:
                            db.execute('UPDATE account SET n=n+1')
                        if cut == 'effect':
                            return
                        db.commit()
                        if cut == 'committed':
                            return  # ack not yet sent; force a redelivery
                    finally:
                        db.close()
                process(crash)
                process(None)
                process(None)
                with sqlite3.connect(path) as db:
                    self.assertEqual(db.execute('SELECT n FROM account').fetchone()[0], 1)
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM seen').fetchone()[0], 1)

    def test_split_commit_counterexamples(self):
        for marker_first, expected in ((True, 0), (False, 2)):
            with self.subTest(marker_first=marker_first), sqlite3.connect(':memory:') as db:
                db.executescript('CREATE TABLE seen(id TEXT PRIMARY KEY); CREATE TABLE effect(n); INSERT INTO effect VALUES(0);')
                if marker_first:
                    db.execute("INSERT INTO seen VALUES('e')")
                else:
                    db.execute('UPDATE effect SET n=n+1')
                db.commit()  # crash between durable marker and effect
                if not db.execute("SELECT 1 FROM seen WHERE id='e'").fetchone():
                    db.execute('UPDATE effect SET n=n+1')
                    db.execute("INSERT INTO seen VALUES('e')")
                self.assertEqual(db.execute('SELECT n FROM effect').fetchone()[0], expected)

    def test_quota_burst_model(self):
        # 8 CPUs, 100 CPU-ms quota per 100 wall-ms period, 200 1-CPU-ms jobs.
        budget, remaining, finished, stalled = 100, 200, 0, 0
        for tick in range(200):
            if tick % 100 == 0:
                budget = 100
            running = min(8, budget, remaining)
            if remaining and not running:
                stalled += 1
            budget -= running
            remaining -= running
            finished += running
        self.assertEqual(finished, 200)
        self.assertGreater(stalled, 70)
        # 200 / (8 * 200) = 12.5% host capacity despite quota saturation.
        self.assertAlmostEqual(finished / (8 * 200), 0.125)
        self.assertAlmostEqual(1000 * 0.080, 80)

    def test_profile_normalization(self):
        baseline, candidate = 2.0 * .4, 1.2 * .6
        self.assertGreater(.6, .4)
        self.assertLess(candidate, baseline)
        self.assertAlmostEqual(baseline, .8)
        self.assertAlmostEqual(candidate, .72)

    def test_dependency_failure_containment(self):
        def impacted(edges, failed):
            affected = set(failed)
            while True:
                next_set = affected | {caller for caller, dep in edges if dep in affected}
                if next_set == affected:
                    return affected
                affected = next_set
        mandatory = {('checkout', 'orders'), ('orders', 'stock'), ('checkout', 'recommendations')}
        self.assertIn('checkout', impacted(mandatory, {'recommendations'}))
        contained = mandatory - {('checkout', 'recommendations')}
        self.assertNotIn('checkout', impacted(contained, {'recommendations'}))
        self.assertIn('checkout', impacted(contained, {'stock'}))

    def test_bloom_no_false_negatives(self):
        # Deterministic SHA-based toy Bloom filter, not a storage engine implementation.
        bits, size, hashes = set(), 2048, 5
        def positions(key):
            return [int.from_bytes(hashlib.sha256(f'{i}:{key}'.encode()).digest()[:8], 'big') % size for i in range(hashes)]
        inserted = [f'key-{i}' for i in range(100)]
        for key in inserted:
            bits.update(positions(key))
        def maybe(key):
            return all(pos in bits for pos in positions(key))
        self.assertTrue(all(maybe(key) for key in inserted))
        self.assertTrue(any(not maybe(f'absent-{i}') for i in range(1000)))
        # A positive result can be false: search the deterministic absent-key set.
        self.assertTrue(any(maybe(f'absent-{i}') for i in range(50000)))
        probability = (1 - math.exp(-hashes * 100 / size)) ** hashes
        self.assertGreater(probability, 0)
        self.assertLess(probability, 1)

    def test_sqlite_reader_pins_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / 'wal.db')
            writer = sqlite3.connect(path)
            reader = sqlite3.connect(path)
            try:
                self.assertEqual(writer.execute('PRAGMA journal_mode=WAL').fetchone()[0], 'wal')
                writer.execute('PRAGMA wal_autocheckpoint=0')
                writer.execute('PRAGMA busy_timeout=30')
                writer.executescript('CREATE TABLE t(n); INSERT INTO t VALUES(1);')
                reader.execute('BEGIN')
                self.assertEqual(reader.execute('SELECT * FROM t').fetchall(), [(1,)])
                writer.execute('INSERT INTO t VALUES(2)')
                writer.commit()
                self.assertEqual(reader.execute('SELECT * FROM t').fetchall(), [(1,)])
                busy, _, _ = writer.execute('PRAGMA wal_checkpoint(TRUNCATE)').fetchone()
                self.assertEqual(busy, 1)
                self.assertGreater(Path(path + '-wal').stat().st_size, 0)
                reader.rollback()
                self.assertEqual(writer.execute('PRAGMA wal_checkpoint(TRUNCATE)').fetchone(), (0, 0, 0))
                self.assertEqual(reader.execute('SELECT * FROM t').fetchall(), [(1,), (2,)])
            finally:
                reader.close()
                writer.close()

    def compile_run(self, source):
        compiler = shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler unavailable; C example NOT verified')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / 'example.c').write_text(source)
            subprocess.run([compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', '-O2', str(path / 'example.c'), '-o', str(path / 'example')], check=True, capture_output=True)
            subprocess.run([str(path / 'example')], check=True, capture_output=True)

    def test_c_allocation_guard(self):
        source = code('engineering/systems-programming/references/memory.md', 'c')
        self.compile_run(source + '''
#include <assert.h>
int main(void) {
    size_t n=99;
    assert(!checked_bytes(SIZE_MAX,2,&n));
    assert(checked_bytes(SIZE_MAX,1,&n) && n==SIZE_MAX);
    assert(checked_bytes(0,SIZE_MAX,&n) && n==0);
    assert(checked_bytes(SIZE_MAX,0,&n) && n==0);
    assert(checked_bytes(7,13,&n) && n==91);
    return 0;
}
''')

    def test_c_partial_write_and_eintr(self):
        source = code('engineering/systems-programming/references/io.md', 'c')
        self.compile_run('''
#include <assert.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>
static unsigned char captured[64];
static size_t used;
static int calls, no_progress;
static ssize_t fake_write(int fd, const void *buf, size_t len) {
    (void)fd;
    if(no_progress) return 0;
    if(calls++ == 0) { errno=EINTR; return -1; }
    size_t n = len > 2 ? 2 : len;
    memcpy(captured+used,buf,n); used+=n;
    return (ssize_t)n;
}
#define write fake_write
''' + source + '''
#undef write
int main(void) {
    const unsigned char value[]="payload";
    assert(write_all_blocking(1,value,7)==0);
    assert(used==7 && memcmp(captured,value,7)==0 && calls>=5);
    no_progress=1;
    assert(write_all_blocking(1,value,7)==-1 && errno==EIO);
    assert(write_all_blocking(1,value,0)==0);
    return 0;
}
''')

    def test_retry_amplification_and_deadline(self):
        self.assertEqual(3 ** 5, 243)
        def attempts(deadline_ms, attempt_ms, delays):
            now, count = 0, 0
            for delay in [0] + list(delays):
                if now + delay + attempt_ms > deadline_ms:
                    break
                now += delay + attempt_ms
                count += 1
            return count, now
        self.assertEqual(attempts(100, 30, [10, 20]), (2, 70))
        self.assertEqual(attempts(29, 30, [0, 0]), (0, 0))
        self.assertEqual(attempts(1000, 1, [0, 0])[0], 3)

    def test_lost_update_interleavings(self):
        results = set()
        histories = []
        for a_positions in itertools.combinations(range(4), 2):
            a_positions = set(a_positions)
            schedule = ['A' if i in a_positions else 'B' for i in range(4)]
            state, reads = 0, {}
            for actor in schedule:
                if actor not in reads:
                    reads[actor] = state
                else:
                    state = reads[actor] + 1
            results.add(state)
            histories.append(schedule)
        self.assertEqual(len(histories), 6)
        self.assertEqual(results, {1, 2})
        self.assertEqual(sum(1 for _ in histories), 6)

    def test_fifo_history_counterexample(self):
        # Enqueue completes before dequeue begins: legal sequential order is fixed.
        def legal_fifo(operations):
            queue = []
            for kind, value in operations:
                if kind == 'enqueue':
                    queue.append(value)
                elif value != (queue.pop(0) if queue else None):
                    return False
            return True
        self.assertFalse(legal_fifo([('enqueue', 'x'), ('dequeue', None)]))
        self.assertTrue(legal_fifo([('enqueue', 'x'), ('dequeue', 'x')]))
        self.assertTrue(legal_fifo([('dequeue', None), ('enqueue', 'x')]))

    def test_fitness_dependency_rule(self):
        def violates(edges):
            return [(a, b) for a, b in edges if a.startswith('checkout.domain') and b.startswith('vendor.payment')]
        allowed = [('checkout.adapter', 'vendor.payment'), ('checkout.domain', 'checkout.port')]
        self.assertEqual(violates(allowed), [])
        self.assertEqual(violates(allowed + [('checkout.domain.order', 'vendor.payment.client')]), [('checkout.domain.order', 'vendor.payment.client')])

    def test_original_bundle_example(self):
        source = code('engineering/design-patterns/references/example.md', 'python')
        namespace = {'__name__': 'example'}
        exec(compile(source, '<original-bundle-example>', 'exec'), namespace)
        make = namespace['create_bundle']
        self.assertEqual((make('compact').render('x'), make('compact').line_spacing), ('<small>x</small>', 1))
        self.assertEqual((make('accessible').render('x'), make('accessible').line_spacing), ('<p>x</p>', 2))
        with self.assertRaises(ValueError):
            make('unknown')

    def test_network_budget_and_prefix(self):
        self.assertAlmostEqual(5 * .030, .150)
        self.assertEqual(100_000_000 * .080 / 8, 1_000_000)
        self.assertEqual(65536 / .080, 819200)
        routes = [('10.0.0.0/8', 'A'), ('10.20.0.0/16', 'B')]
        matches = [(ip_network(prefix).prefixlen, hop) for prefix, hop in routes if ip_address('10.20.4.9') in ip_network(prefix)]
        self.assertEqual(max(matches)[1], 'B')


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""Run deterministic exercises and save observed results, without model-quality scores."""
import contextlib
import io
import json
import platform
import shutil
import sqlite3
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EvidenceResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({'test': test.id(), 'status': 'passed'})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.records.append({'test': test.id(), 'status': 'skipped', 'reason': reason})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append({'test': test.id(), 'status': 'failed'})

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append({'test': test.id(), 'status': 'error'})


def main():
    output = ROOT / 'evaluations/results.json'
    # Ensure documentation links can be validated while the first report is built.
    if not output.exists():
        output.write_text('{}\n')
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    stream = io.StringIO()
    start = time.monotonic()
    with contextlib.redirect_stdout(io.StringIO()):
        result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=EvidenceResult).run(suite)
    report = {
        'method': 'deterministic mechanism exercises and library/installation checks',
        'not_measured': ['independent agent responses', 'baseline-versus-skill uplift', 'production outcomes'],
        'command': 'python3 scripts/evaluate.py',
        'python': platform.python_version(),
        'sqlite': sqlite3.sqlite_version,
        'c_compiler': shutil.which('cc'),
        'tests_run': result.testsRun,
        'passed': sum(x['status'] == 'passed' for x in result.records),
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped),
        'successful': result.wasSuccessful(),
        'elapsed_seconds': round(time.monotonic() - start, 3),
        'records': result.records,
        'runner_output': stream.getvalue(),
    }
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(stream.getvalue())
    print(f'Results written to {output}')
    return not result.wasSuccessful()


if __name__ == '__main__':
    sys.exit(main())

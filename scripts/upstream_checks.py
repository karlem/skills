#!/usr/bin/env python3
"""Run pinned converter host validators and scan ALL skill Markdown via a temp mirror."""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = 'a24e62f4d8caf2ee433f6e48d9073800f56f906e'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('converter_root', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'evaluations/upstream-results.json')
    args = parser.parse_args()
    converter = args.converter_root.resolve()
    commit = subprocess.check_output(['git', '-C', str(converter), 'rev-parse', 'HEAD'], text=True).strip()
    if commit != EXPECTED:
        parser.error(f'Expected {EXPECTED}; found {commit}')
    rows = []
    for item in json.loads((ROOT / 'sources/skills-index.json').read_text()):
        path = ROOT / item['path']
        for lens in ('claude', 'copilot', 'amp', 'opencode'):
            command = [sys.executable, str(converter / 'tools/validate_skill.py'), '--lens', lens, str(path / 'SKILL.md')]
            result = subprocess.run(command, capture_output=True, text=True)
            rows.append(dict(skill=item['name'],check='format',lens=lens,exit_code=result.returncode,output=result.stdout + result.stderr))
        # Upstream scans chapters/ but not references/. Copy, never alter real files.
        with tempfile.TemporaryDirectory(prefix='skill-scan-') as tmp:
            mirror = Path(tmp)
            shutil.copy2(path / 'SKILL.md', mirror / 'SKILL.md')
            shutil.copytree(path / 'references', mirror / 'chapters')
            result = subprocess.run([sys.executable, str(converter / 'tools/scan_generated_skill.py'), str(mirror)], capture_output=True, text=True)
            rows.append(dict(skill=item['name'],check='content-scan',scope='SKILL.md and every references/*.md via temporary chapters mirror',exit_code=result.returncode,output=result.stdout + result.stderr))
    report = dict(converter_commit=commit,all_passed=all(r['exit_code'] == 0 for r in rows),checks=rows)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(f'{len(rows)} checks; all passed={report["all_passed"]}; report={args.output}')
    if not report['all_passed']:
        for row in rows:
            if row['exit_code']:
                print(row['skill'], row['check'], row.get('lens', ''), row['output'])
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

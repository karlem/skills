#!/usr/bin/env python3
"""Offline validation of skill structure, links, source coverage, and evaluation wiring."""
import ast
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    index = json.loads((root / 'sources/skills-index.json').read_text())
    manifest = json.loads((root / 'sources/manifest.json').read_text())
    cases = json.loads((root / 'evaluations/cases.json').read_text())['cases']
    names = {s['name'] for s in index}
    check(len(names) == len(index), 'Duplicate skill names')
    paths = {root / s['path'] / 'SKILL.md' for s in index}
    discovered = {p for p in root.rglob('SKILL.md') if not any(x in {'.git', '.cache', '.venv'} for x in p.parts)}
    check(paths == discovered, 'Index and discovered skills differ')
    sources = {s['id']: s for s in manifest['sources']}
    check(len(sources) == len(manifest['sources']), 'Duplicate source IDs')
    for item in manifest['sources']:
        check(item['url'].startswith('https://'), f"Non-HTTPS source: {item['id']}")
        check(bool(item.get('access_date') and item.get('license_or_access') and item.get('supports')), f"Incomplete source: {item['id']}")
        if item['access_status'] == 'public':
            check(item.get('http_status') == 200, f"Public source lacks observed success: {item['id']}")
            check(bool(re.fullmatch('[0-9a-f]{64}', item.get('sha256', ''))), f"Missing source hash: {item['id']}")
    check(len(manifest['books']) == 10, 'Expected ten book coverage entries')
    mapped = set()
    for book in manifest['books']:
        check(bool(book.get('authors') and book.get('edition')), f"Missing bibliography: {book['id']}")
        check(book['coverage_status'] in {'partial', 'complete'}, f"Unknown coverage: {book['id']}")
        if book['coverage_status'] == 'partial':
            check(bool(book.get('incomplete_reason') and book.get('not_covered')), f"Unexplained coverage: {book['id']}")
        for source in book['source_ids']:
            check(source in sources, f"Unknown source {source} in {book['id']}")
        mapped.update(book['skill_names'])
    check(mapped == names, 'Book-to-skill mapping incomplete')
    tests = set()
    for path in (root / 'tests').glob('test_*.py'):
        tree = ast.parse(path.read_text())
        tests.update(n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'))
    check({c['skill'] for c in cases} == names, 'Missing skill evaluation scenario')
    check(len({c['id'] for c in cases}) == len(cases), 'Duplicate evaluation IDs')
    for case in cases:
        check(len(case['criteria']) >= 4 and len(case['disqualifying_errors']) >= 2, f"Thin rubric: {case['id']}")
        check(bool(case.get('reviewed_response')), f"Missing reviewed response: {case['id']}")
        for test in case['executable_evidence']:
            check(test in tests, f"Missing executable evidence {test} for {case['id']}")
    for item in index:
        path = root / item['path'] / 'SKILL.md'
        if not path.exists():
            continue
        text = path.read_text()
        name = re.search(r'^name: ([a-z0-9]+(?:-[a-z0-9]+)*)$', text, re.M)
        description = re.search(r'^description: "([^"\n]+)"$', text, re.M)
        check(text.startswith('---\n') and '\n---\n' in text[4:], f'{path}: frontmatter absent')
        check(name is not None and name[1] == item['name'] == path.parent.name and len(name[1]) <= 64, f'{path}: name mismatch')
        check(description is not None and 1 <= len(description[1]) <= 1024, f'{path}: invalid description')
        check(len(text.splitlines()) <= 150 and len(text.split()) < 2000, f'{path}: entrypoint budget exceeded')
        check('## Scope and references' in text and 'Partial' in text, f'{path}: missing coverage disclosure')
        refs = list((path.parent / 'references').glob('*.md'))
        check(len(refs) >= 2, f'{path}: insufficient references')
        for ref in refs:
            check(f'references/{ref.name}' in text, f'{path}: reference not routed: {ref.name}')
    markdown = [p for p in root.rglob('*.md') if not any(x in {'.git', '.cache', '.venv'} for x in p.parts)]
    for path in markdown:
        text = path.read_text()
        check(text.count('```') % 2 == 0, f'{path}: unbalanced code fences')
        check(not any(ord(c) in {0x200b, 0x200c, 0x200d, 0x2060, 0xfeff} for c in text), f'{path}: invisible control character')
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
                continue
            target = unquote(link.split('#', 1)[0])
            check((path.parent / target).exists(), f'{path}: broken link {link}')
    return errors, {'skills': len(index), 'books': len(manifest['books']), 'sources': len(sources), 'scenarios': len(cases), 'markdown_files': len(markdown)}


if __name__ == '__main__':
    errors, counts = validate()
    print(json.dumps({'ok': not errors, 'counts': counts, 'errors': errors}, indent=2))
    sys.exit(bool(errors))

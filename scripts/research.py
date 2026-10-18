#!/usr/bin/env python3
"""Fetch one allowlisted public source and extract locally; never put raw sources in git."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def pptx_text(path):
    """Ordered visible slide text only. Images, animation order, equations may be lost."""
    with zipfile.ZipFile(path) as archive:
        names = sorted((n for n in archive.namelist()
                        if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)),
                       key=lambda n: int(re.search(r'(\d+)\.xml', n)[1]))
        parts = []
        for index, name in enumerate(names, 1):
            tree = ET.fromstring(archive.read(name))
            text = [e.text for e in tree.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t') if e.text]
            parts.append(f'## Slide {index}\n' + '\n'.join(text))
        return '\n\n'.join(parts)


def html_text(path):
    from bs4 import BeautifulSoup  # optional research dependency
    soup = BeautifulSoup(path.read_bytes(), 'html.parser')
    for node in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript']):
        node.decompose()
    body = soup.find('article') or soup.find('main') or soup.body or soup
    return body.get_text('\n', strip=True)


def extract(path, output):
    output = output.resolve()
    if output.exists():
        raise FileExistsError(f'Refusing existing extraction: {output}')
    suffix = path.suffix.lower()
    # Supplement formats/cleanup that the primary converter does not handle well.
    if suffix in {'.html', '.pptx'}:
        prepared = path.with_suffix('.prepared.md')
        if prepared.exists():
            raise FileExistsError(f'Refusing existing prepared source: {prepared}')
        prepared.write_text(pptx_text(path) if suffix == '.pptx' else html_text(path))
        path = prepared
    env = dict(os.environ, BOOK_SKILL_WORKDIR=str(output))
    subprocess.run([sys.executable, '-m', 'book_to_skill', str(path),
                    '--mode', 'text', '--no-install-missing'], env=env, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_id')
    parser.add_argument('--extract', action='store_true')
    args = parser.parse_args()
    sources = json.loads((ROOT / 'sources/manifest.json').read_text())['sources']
    source = next((s for s in sources if s['id'] == args.source_id), None)
    if source is None or source['access_status'] != 'public':
        parser.error('Select an observed public source ID from sources/manifest.json.')
    cache = ROOT / '.cache/research' / source['id']
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / ('source.' + source['format'])
    if target.exists():
        parser.error(f'Refusing existing source: {target}')
    request = urllib.request.Request(source['url'], headers={'User-Agent': 'EngineeringKnowledgeLibrary/1.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    target.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f'{source["id"]}: sha256={digest}; matches recorded bytes={digest == source.get("sha256")}')
    if source['format'] == 'pdf' and not data.startswith(b'%PDF'):
        parser.error('Expected PDF; inspect the response locally before proceeding.')
    if args.extract:
        extract(target, cache / 'extracted')
    print('Private local source:', target)


if __name__ == '__main__':
    main()

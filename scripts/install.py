#!/usr/bin/env python3
"""Copy selected standalone skills into a flat agent skill root. Never overwrite."""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def install(destination, names, dry_run=False):
    index = json.loads((ROOT / 'sources/skills-index.json').read_text())
    available = {item['name']: item for item in index}
    unknown = set(names) - available.keys()
    if unknown:
        raise ValueError('Unknown skills: ' + ', '.join(sorted(unknown)))
    destination = Path(destination).expanduser().resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError('Install outside the library checkout.')
    selected = [available[name] for name in dict.fromkeys(names)]
    for item in selected:
        target = destination / item['name']
        if target.exists() or target.is_symlink():
            raise FileExistsError(f'Refusing existing destination: {target}')
    for item in selected:
        target = destination / item['name']
        if not dry_run:
            destination.mkdir(parents=True, exist_ok=True)
            shutil.copytree(ROOT / item['path'], target)
        print(('Would install ' if dry_run else 'Installed ') + str(target))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', required=True, help='Agent skill root, e.g. ~/.agents/skills')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--skill', nargs='+', help='One or more skill names')
    group.add_argument('--all', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    names = args.skill or [x['name'] for x in json.loads((ROOT / 'sources/skills-index.json').read_text())]
    try:
        install(args.dest, names, args.dry_run)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()

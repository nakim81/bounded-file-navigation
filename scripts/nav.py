#!/usr/bin/env python3
"""Bounded, read-only file discovery; never treat a truncated result as exhaustive."""
import argparse
import os
from pathlib import Path

SKIP = {'.git', 'node_modules', 'dist', 'build', '.build', '.next', '.venv',
        'venv', 'tmp', 'test-results', '.cache', 'cache', '__pycache__'}
TEXT = {'.md', '.yaml', '.yml', '.json', '.jsonc', '.py', '.ts', '.tsx', '.js',
        '.mjs', '.swift', '.txt', '.toml', '.go', '.rs', '.sh'}


def navigate(root, query, mode, limit):
    matches = []
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not d.startswith('.'))
        for name in sorted(names):
            path = Path(base) / name
            if path.is_symlink() or path.suffix.lower() not in TEXT:
                continue
            relative = path.relative_to(root).as_posix()
            if mode == 'paths':
                if query in relative.casefold():
                    matches.append(relative)
            elif path.stat().st_size <= 1_000_000:
                try:
                    with path.open(errors='replace') as stream:
                        for number, line in enumerate(stream, 1):
                            if query in line.casefold():
                                matches.append(f'{relative}:{number}: {line.strip()[:180]}')
                                if len(matches) > limit:
                                    break
                except OSError:
                    continue
            if len(matches) > limit:
                break
        if len(matches) > limit:
            break
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('query', help='literal, case-insensitive substring')
    parser.add_argument('--mode', choices=['paths', 'lines'], default='paths')
    parser.add_argument('--limit', type=int, default=12)
    args = parser.parse_args()
    if not args.root.is_dir() or not args.query.strip() or not 1 <= args.limit <= 50:
        parser.error('root must exist, query must be nonempty, limit must be 1..50')
    matches = navigate(args.root.resolve(), args.query.casefold(), args.mode, args.limit)
    for match in matches[:args.limit]:
        print(match)
    if len(matches) > args.limit:
        print('TRUNCATED: narrow the subtree/query; more matches exist')
    elif not matches:
        print('NO MATCH in searched text; excluded dirs/extensions and large files not checked')


if __name__ == '__main__':
    main()

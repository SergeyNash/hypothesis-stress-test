#!/usr/bin/env python3
"""Bounded metadata discovery before extraction; JSON to stdout, no writes.

Path names only rank candidates. They are never evidence of document contents.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

SUPPORTED = {'.md', '.markdown', '.txt', '.log', '.csv', '.srt', '.vtt',
             '.pdf', '.docx', '.xlsx', '.html', '.htm'}
MEDIA = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp3', '.wav', '.m4a',
         '.ogg', '.mp4', '.mov', '.webm', '.mkv'}
EXCLUDED = {'.hst', '.vscode', '.git', '.cline', '.clinerules', '.obsidian', '.agents', '.github',
            '.venv', 'venv', 'env', '.env', 'site-packages', 'node_modules', 'runs', 'examples', '__pycache__'}
HINTS = ('гипотез', 'развит', 'иде', 'стратег', 'исследован', 'интервью',
         'hypothes', 'growth', 'idea', 'strateg', 'research', 'discovery', 'interview')


def priority(path, terms):
    name = path.as_posix().casefold()
    topic = sorted({term for term in terms if (
        re.search(r'(?<![^\W_])' + re.escape(term) + r'(?![^\W_])', name)
        if len(term) <= 3 else term in name)})
    hints = sorted({hint for hint in HINTS if hint in name})
    # Topic matches outrank generic growth/strategy hints, including in ancestors.
    return (bool(topic), len(topic), bool(hints)), topic, hints


def discover(root, query='', *, max_entries=20000, max_depth=32):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError('root_not_directory')
    terms = {word for word in re.findall(r'[\w-]+', query.casefold()) if len(word) >= 2}
    result = {'root': str(root), 'entries_seen': 0, 'limit_reached': False,
              'limits': {'max_entries': max_entries, 'max_depth': max_depth},
              'directories': [], 'files': [], 'excluded': [], 'errors': []}

    def error(exc):
        result['errors'].append({'path': str(exc.filename), 'reason': 'directory_unreadable'})

    for directory, dirs, names in os.walk(root, followlinks=False, onerror=error):
        base = Path(directory)
        kept = []
        # Bound metadata traversal independently from the extraction file cap.
        for name in sorted(dirs) + sorted(names):
            if result['entries_seen'] >= max_entries:
                result['limit_reached'] = True
                break
            result['entries_seen'] += 1
            path = base / name
            relative = path.relative_to(root)
            item = {'path': relative.as_posix()}
            is_dir = name in dirs
            reason = None
            if path.is_symlink():
                reason = 'symlink'
            elif is_dir and name in EXCLUDED:
                reason = 'generated_or_configuration_directory'
            elif is_dir and ((path / '.cline/skills/local-knowledge-retrieval/SKILL.md').is_file()
                             and (path / 'scripts/extract_evidence.py').is_file()):
                reason = 'framework_directory'
            elif is_dir and len(relative.parts) > max_depth:
                reason = 'depth_limit'
                result['limit_reached'] = True
            if reason:
                result['excluded'].append(dict(item, reason=reason))
                continue
            rank, topic, hints = priority(relative, terms)
            item.update(topic_matches=topic, directory_hints=hints)
            if is_dir:
                kept.append(name)
                result['directories'].append(item)
            else:
                ext = path.suffix.casefold()
                item['reader'] = 'document' if ext in SUPPORTED else ('media' if ext in MEDIA else 'unsupported')
                try:
                    item['size_bytes'] = path.stat().st_size
                except OSError:
                    item['reason'] = 'stat_failed'
                result['files'].append(item)
        dirs[:] = kept
        if result['entries_seen'] >= max_entries and result['limit_reached']:
            break
    result['files'].sort(key=lambda x: (
        -int(bool(x['topic_matches'])), -len(x['topic_matches']),
        -int(bool(x['directory_hints'])), x['path'].casefold()))
    return result


def positive(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError('must be positive')
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--query', default='', help='Short topic terms from the hypothesis; no client secrets')
    parser.add_argument('--max-entries', type=positive, default=20000)
    parser.add_argument('--max-depth', type=positive, default=32)
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error('--root must be an existing directory')
    print(json.dumps(discover(args.root, args.query, max_entries=args.max_entries,
                              max_depth=args.max_depth), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

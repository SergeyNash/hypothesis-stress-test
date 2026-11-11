#!/usr/bin/env python3
"""Capture bounded source fragments without interpretation; retain paged extraction history."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from extract_evidence import extract
from run_progress import atomic, output_dir


def capture(run, root, paths, **limits):
    run, root = Path(run).resolve(), Path(root).resolve()
    target = output_dir(run) / 'source_snapshot.json'
    snapshot = json.loads(target.read_text(encoding='utf-8')) if target.exists() else {
        'schema_version': 1, 'files': [], 'captures': []}
    if snapshot.get('schema_version') != 1:
        raise ValueError('unsupported snapshot')
    for path in paths:
        if (root / path).resolve() == run / 'input/hypothesis.md':
            raise ValueError('The mutable run hypothesis is not a source document; preserve its formulation in the report.')
        result = extract(root / path, root, **limits)
        result['root'] = str(root)
        # Reject silently merging pages from different file revisions.
        prior = next((f for f in snapshot['files'] if f['source_path'] == result['source_path']), None)
        if prior:
            if prior.get('sha256') != result.get('sha256'):
                raise ValueError('source_changed: preserve prior snapshot and invalidate dependent evidence before recapture')
            locations = {u['location']: u for u in prior['units']}
            locations.update({u['location']: u for u in result['units']})
            prior['units'] = list(locations.values())
            prior.setdefault('pages', []).append({k:v for k,v in result.items() if k != 'units'})
        else:
            snapshot['files'].append(dict(result, pages=[{k:v for k,v in result.items() if k != 'units'}]))
        snapshot['captures'].append({'at': datetime.now(timezone.utc).isoformat(),
                                     **{k:v for k,v in result.items() if k != 'units'}})
    atomic(target, json.dumps(snapshot, ensure_ascii=False, indent=2))
    return snapshot


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run-dir', type=Path, required=True)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--path', action='append', required=True)
    p.add_argument('--start-unit', type=int, default=0)
    p.add_argument('--max-units', type=int, default=1000)
    p.add_argument('--max-chars', type=int, default=100000)
    a = p.parse_args()
    if a.start_unit < 0 or min(a.max_units, a.max_chars) < 1:
        p.error('invalid extraction limits')
    try:
        snapshot = capture(a.run_dir, a.root, a.path, start_unit=a.start_unit,
                           max_units=a.max_units, max_chars=a.max_chars)
        print(json.dumps({'snapshot': str(a.run_dir.resolve()/'outputs/source_snapshot.json'),
            'files': [{k:v for k,v in f.items() if k not in {'units','pages'}} for f in snapshot['files']]}, ensure_ascii=False))
    except (OSError, ValueError, KeyError) as exc:
        p.error(str(exc))


if __name__ == '__main__':
    main()

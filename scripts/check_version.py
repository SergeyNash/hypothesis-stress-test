#!/usr/bin/env python3
"""Validate release metadata and the project's next-MINOR-per-PR policy."""
import argparse
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def parse(value):
    if not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.0', value):
        raise ValueError('Expected MAJOR.MINOR.0, got: ' + value)
    return tuple(map(int, value.split('.')))


def check(root, base_version=None):
    version = (root / 'VERSION').read_text(encoding='utf-8').strip()
    current = parse(version)
    errors = []
    if base_version is not None:
        previous = parse(base_version.strip())
        expected = (previous[0], previous[1] + 1, 0)
        if current != expected:
            errors.append('Every PR requires the next MINOR: expected ' + '.'.join(map(str, expected)))
    texts = {name: (root / name).read_text(encoding='utf-8') for name in
             ['README.md', '.clinerules/00-hypothesis-framework.md', 'CHANGELOG.md']}
    for name, pattern in [
        ('README.md', r'Версия фреймворка <b>([^<]+)</b>'),
        ('.clinerules/00-hypothesis-framework.md', r'\*\*Framework version:\*\* ([\d.]+)')
    ]:
        found = re.search(pattern, texts[name])
        if not found or found.group(1) != version:
            errors.append(name + ' must declare ' + version)
    releases = re.findall(r'^## \[([\d.]+)\] — (\d{4}-\d{2}-\d{2})$', texts['CHANGELOG.md'], re.M)
    if not releases or releases[0][0] != version:
        errors.append('CHANGELOG must start with a dated release for ' + version)
    if re.search(r'^## \[?Unreleased\]?\s*$', texts['CHANGELOG.md'], re.M | re.I):
        errors.append('Move Unreleased entries into the current dated release')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', help='Git commit/ref of the target branch')
    args = parser.parse_args()
    try:
        base_version = None
        if args.base:
            base_version = subprocess.check_output(
                ['git', 'show', args.base + ':VERSION'], cwd=ROOT, text=True).strip()
        errors = check(ROOT, base_version)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        errors = [str(exc)]
    for error in errors:
        print('FAIL: ' + error)
    if not errors:
        print('Version policy: PASS')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())

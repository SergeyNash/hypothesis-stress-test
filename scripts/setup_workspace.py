#!/usr/bin/env python3
"""Inspect/install HST's Cline adapter without moving a user's knowledge base."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys

FRAMEWORK = Path(__file__).resolve().parents[1]


def plan(workspace, framework=FRAMEWORK):
    workspace, framework = Path(workspace).resolve(), Path(framework).resolve()
    if not workspace.is_dir():
        raise ValueError('workspace_not_directory')
    if not (framework / 'scripts/extract_evidence.py').is_file():
        raise ValueError('framework_not_found')
    entries = []
    for directory in ['.cline', '.clinerules']:
        for source in sorted((framework / directory).rglob('*')):
            if not source.is_file() or source.is_symlink():
                continue
            relative = source.relative_to(framework)
            target = workspace / relative
            if not target.resolve().is_relative_to(workspace):
                raise ValueError('destination_outside_workspace')
            if target.exists() and not target.is_file():
                raise ValueError('destination_not_file:' + relative.as_posix())
            status = ('same' if target.read_bytes() == source.read_bytes() else 'conflict') if target.exists() else 'missing'
            entries.append({'path': relative.as_posix(), 'status': status, 'source': str(source)})
    if workspace != framework:
        # Resolve actual ZIP names without assuming a conventional directory name.
        import os
        location = Path(os.path.relpath(framework, workspace)).as_posix()
        content = f'''# HST workspace locations\n\nKB_ROOT is the current workspace. FRAMEWORK_DIR is `{location}` relative to KB_ROOT. Resolve all HST scripts, templates, profiles, layers and docs against FRAMEWORK_DIR, including relative links in copied skills. Runs go in KB_ROOT/runs. Existing KB materials stay where they are.\n'''
        target = workspace / '.clinerules/05-hst-workspace.md'
        if not target.resolve().is_relative_to(workspace):
            raise ValueError('destination_outside_workspace')
        status = ('same' if target.read_text(encoding='utf-8') == content else 'conflict') if target.exists() else 'missing'
        entries.append({'path': '.clinerules/05-hst-workspace.md', 'status': status, 'content': content})
    return {'workspace': str(workspace), 'framework': str(framework), 'files': entries,
            'readers': {name: bool(importlib.util.find_spec(name)) for name in ['docx', 'openpyxl', 'pypdf']},
            'python': sys.executable}


def install(workspace, framework=FRAMEWORK, replace=False):
    result = plan(workspace, framework)
    conflicts = [x['path'] for x in result['files'] if x['status'] == 'conflict']
    if conflicts and not replace:
        raise ValueError('conflicts; no files changed: ' + ', '.join(conflicts))
    for item in result['files']:
        if item['status'] == 'same':
            continue
        target = Path(workspace).resolve() / item['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        if 'content' in item:
            target.write_text(item['content'], encoding='utf-8')
        else:
            shutil.copyfile(item['source'], target)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--framework', type=Path, default=FRAMEWORK)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--replace-framework-files', action='store_true')
    args = p.parse_args()
    try:
        report = install(args.workspace, args.framework, args.replace_framework_files) if args.apply else plan(args.workspace, args.framework)
        report['action'] = 'applied' if args.apply else 'inspection_only'
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except (ValueError, OSError) as e:
        p.error(str(e))


if __name__ == '__main__':
    main()

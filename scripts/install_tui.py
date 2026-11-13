#!/usr/bin/env python3
"""Install a supplied TUI binary and the dependency-free VS Code/Cline bridge."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
from xml.sax.saxutils import escape
from run_progress import atomic

ROOT = Path(__file__).resolve().parents[1]


def package(destination):
    version = (ROOT / 'VERSION').read_text().strip()
    source = ROOT / 'integrations/vscode-bridge'
    metadata = json.loads((source / 'package.json').read_text(encoding='utf-8'))
    metadata['version'] = version
    manifest = f'''<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011"><Metadata><Identity Language="en-US" Id="hst-pipeline-bridge" Version="{version}" Publisher="hst"/><DisplayName>HST Pipeline Bridge</DisplayName><Description xml:space="preserve">Local HST TUI/Cline bridge</Description><Tags>HST</Tags><Categories>Other</Categories><GalleryFlags>Public</GalleryFlags><Properties><Property Id="Microsoft.VisualStudio.Code.Engine" Value="^1.93.0"/><Property Id="Microsoft.VisualStudio.Code.ExtensionDependencies" Value="saoudrizwan.claude-dev"/></Properties></Metadata><Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation><Dependencies/><Assets><Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/></Assets></PackageManifest>'''
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('extension.vsixmanifest', manifest)
        z.writestr('[Content_Types].xml', '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="json" ContentType="application/json"/><Default Extension="js" ContentType="application/javascript"/><Default Extension="vsixmanifest" ContentType="text/xml"/></Types>')
        z.writestr('extension/package.json', json.dumps(metadata))
        for name in ['extension.js', 'protocol.js']:
            z.write(source / name, 'extension/' + name)
    return destination


def install(workspace, binary):
    workspace, binary = Path(workspace).resolve(), Path(binary).resolve()
    state = workspace / '.hst'
    if state.is_symlink() or (state / 'bin').is_symlink(): raise ValueError('TUI state must not be a symlink')
    for name in ['.hst/workspace.json', '.hst/tui.json', '.vscode/tasks.json']:
        target = workspace / name
        if target.is_symlink() or not target.resolve().is_relative_to(workspace):
            raise ValueError('Installer path outside workspace: ' + name)
    from setup_workspace import install as install_adapter
    # The installed bridge and the model must resolve the same framework.
    install_adapter(workspace, ROOT, replace=True, terminal=False)
    state.mkdir(exist_ok=True)
    version = (ROOT / 'VERSION').read_text().strip()
    destination = state / 'bin' / ('hst-tui-' + version + ('.exe' if sys.platform == 'win32' else ''))
    destination.parent.mkdir(exist_ok=True)
    if destination.is_symlink(): raise ValueError('TUI binary must not be a symlink')
    if destination != binary:
        shutil.copyfile(binary, destination)
    if sys.platform != 'win32': destination.chmod(0o755)
    import os
    workspace_config = state / 'workspace.json'
    previous = json.loads(workspace_config.read_text(encoding="utf-8-sig")) if workspace_config.exists() else {}
    previous.update(schema_version=1, framework_dir=Path(os.path.relpath(ROOT, workspace)).as_posix())
    atomic(workspace_config, json.dumps(previous, ensure_ascii=False, indent=2))
    # TUI is the automatic terminal surface; preserve all other VS Code tasks.
    tasks = workspace / '.vscode/tasks.json'
    if tasks.exists():
        from vscode_tasks import parse, merge, LABEL
        text = tasks.read_text(encoding='utf-8'); data, _ = parse(text)
        entry = next((x for x in data.get('tasks', []) if x.get('label') == LABEL), None)
        if entry:
            entry.pop('runOptions', None)
            content, _ = merge(text, entry, replace=True)
            atomic(tasks, content)
    atomic(state / 'tui.json', json.dumps({'schema_version': 1, 'binary': str(destination), 'python': sys.executable}, indent=2))
    vsix = package(state / ('hst-bridge-' + version + '.vsix'))
    code = shutil.which('code')
    if not code: raise ValueError('VS Code command code not found; install VSIX manually: ' + str(vsix))
    command = [code, '--install-extension', str(vsix), '--force']
    environment = None
    if sys.platform == 'win32' and Path(code).suffix.lower() in {'.cmd', '.bat'}:
        executable = Path(code).parent.parent / 'Code.exe'
        cli = Path(code).parent.parent / 'resources/app/out/cli.js'
        if not executable.is_file() or not cli.is_file():
            raise ValueError('Install VSIX manually in VS Code: ' + str(vsix))
        command = [str(executable), str(cli), '--install-extension', str(vsix), '--force']
        environment = dict(os.environ, ELECTRON_RUN_AS_NODE='1')
    subprocess.run(command, check=True, env=environment)
    return {'binary': str(destination), 'bridge': str(vsix), 'next': 'Reload the DataB VS Code window; HST control opens automatically'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace', type=Path)
    p.add_argument('--binary', type=Path)
    p.add_argument('--package', type=Path)
    a = p.parse_args()
    if a.package: print(package(a.package)); return
    if not a.workspace or not a.binary: p.error('--workspace and --binary required')
    print(json.dumps(install(a.workspace, a.binary), ensure_ascii=False))


if __name__ == '__main__': main()

'use strict';
const vscode = require('vscode');
const fs = require('node:fs/promises');
const path = require('node:path');
const {execFile} = require('node:child_process');
const {promisify} = require('node:util');
const {processRequest} = require('./protocol');
const execute = promisify(execFile);
let polling = false;
let terminal;

async function localJSON(root, relative) {
  const target = path.join(root, relative);
  const real = await fs.realpath(target);
  const rel = path.relative(root, real);
  if (rel.startsWith('..') || path.isAbsolute(rel)) throw Error('Control path outside workspace');
  const info = await fs.lstat(target);
  if (info.isSymbolicLink() || info.size > 1024 * 1024) throw Error('Invalid control file');
  return JSON.parse(await fs.readFile(real, 'utf8'));
}
async function writeJSON(file, value) {
  const tmp = file + '.' + require('node:crypto').randomUUID() + '.tmp';
  await fs.writeFile(tmp, JSON.stringify(value));
  await fs.rename(tmp, file);
}
async function contextFor(folder) {
  const root = await fs.realpath(folder.uri.fsPath);
  const settings = await localJSON(root, '.hst/workspace.json');
  const framework = await fs.realpath(path.resolve(root, settings.framework_dir));
  if (path.relative(root, framework).startsWith('..')) throw Error('Framework outside workspace');
  const tui = await localJSON(root, '.hst/tui.json');
  const helper = path.join(framework, 'scripts/tui_control.py');
  const call = async (action, id, args=[]) => {
    const command = [helper, action, '--workspace', root];
    if (id) command.push('--request', id);
    command.push(...args);
    const {stdout} = await execute(tui.python, command, {cwd: root, windowsHide: true, maxBuffer: 2 * 1024 * 1024, env: {...process.env, PYTHONUTF8: '1', HST_COMMAND_ORIGIN: 'vscode_bridge'}});
    return JSON.parse(stdout.trim());
  };
  return {root, framework, tui, call};
}
async function openControl() {
  if (terminal) { terminal.show(true); return; }
  const folder = vscode.workspace.workspaceFolders?.[0];
  if (!folder || !vscode.workspace.isTrusted) return;
  const ctx = await contextFor(folder);
  const binary = await fs.realpath(ctx.tui.binary);
  if (path.relative(ctx.root, binary).startsWith('..')) throw Error('TUI binary outside workspace');
  terminal = vscode.window.createTerminal({name: 'HST · Управление', shellPath: binary, shellArgs: ['--workspace', ctx.root], cwd: ctx.root});
  terminal.show(true);
}
async function poll(output) {
  if (polling || !vscode.workspace.isTrusted) return;
  polling = true;
  try {
    // Cline's public API controls the current VS Code workspace. Ambiguous multi-root launch is disabled.
    if (vscode.workspace.workspaceFolders?.length !== 1) return;
    const ctx = await contextFor(vscode.workspace.workspaceFolders[0]);
    const extension = vscode.extensions.getExtension('saoudrizwan.claude-dev');
    const api = extension && (extension.isActive ? extension.exports : await extension.activate());
    const ready = Boolean(api && typeof api.startNewTask === 'function' && typeof api.sendMessage === 'function');
    await writeJSON(path.join(ctx.root, '.hst/tui-bridge.json'), {schema_version: 1, workspace: ctx.root, ready, at: new Date().toISOString(), message: ready ? 'Cline API ready' : 'Cline API недоступен'});
    if (!ready) return;
    const directory = path.join(ctx.root, '.hst/requests');
    let entries;
    try { entries = await fs.readdir(directory); } catch (e) { if (e.code === 'ENOENT') return; throw e; }
    for (const id of entries.filter(s => /^[a-f0-9]{32}$/.test(s))) {
      const saved = await localJSON(ctx.root, '.hst/requests/' + id + '/status.json');
      if (['finished','failed','cancelled'].includes(saved.state)) continue;
      const value = await ctx.call('status', id);
      await processRequest(ctx, id, value, api, message => output.appendLine(message));
    }
  } catch (e) {
    // A folder without TUI installation is normal. Errors during actual requests are retained by the protocol.
    if (e.code !== 'ENOENT') output.appendLine(String(e));
  } finally { polling = false; }
}
function activate(context) {
  const output = vscode.window.createOutputChannel('HST Bridge');
  context.subscriptions.push(output, vscode.commands.registerCommand('hst.openControl', openControl));
  context.subscriptions.push(vscode.window.onDidCloseTerminal(t => { if (t === terminal) terminal = undefined; }));
  context.subscriptions.push(vscode.window.registerUriHandler({handleUri: uri => uri.path === '/open' ? openControl() : undefined}));
  const timer = setInterval(() => poll(output), 2000);
  context.subscriptions.push({dispose: () => clearInterval(timer)});
  poll(output).then(async () => {
    try { if (vscode.workspace.workspaceFolders?.length === 1) await openControl(); }
    catch (e) { if (e.code !== 'ENOENT') output.appendLine(String(e)); }
  });
}
module.exports = {activate};

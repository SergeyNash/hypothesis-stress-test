'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const {processRequest} = require('./protocol');
function fixture() {
  const value = {state: 'queued', run_dir: 'runs/HYP-2026-11-13-001'};
  const calls = [];
  const ctx = {root: '/kb', framework: '/kb/hst', call: async (action, id, args=[]) => {
    calls.push({action, id, args});
    if (action === 'bootstrap') value.state = 'prepared';
    if (action === 'transition') {
      const next = args[1];
      if (next === 'dispatching') assert.equal(value.state, 'prepared');
      if (next !== 'dispatched' || value.state !== 'accepted') value.state = next;
    }
    if (action === 'question-sent') {assert.equal(value.question.state, 'answered');value.question.state='sent';}
    return {...value};
  }};
  return {value, calls, ctx};
}
test('dispatch invokes real API contract but never fabricates agent acknowledgement', async () => {
  const {value,calls,ctx} = fixture();
  let tasks = 0;
  const api = {startNewTask: async prompt => {tasks++;assert.match(prompt,/acknowledge/);assert.match(prompt,/55-tui-control/);},sendMessage: async()=>{}};
  await processRequest(ctx, 'a'.repeat(32), value, api, ()=>{});
  assert.equal(tasks,1); assert.equal(value.state,'dispatched');
  await processRequest(ctx, 'a'.repeat(32), value, api, ()=>{});
  assert.equal(tasks,1);
  assert.ok(!calls.some(c=>c.args.includes('accepted')));
});
test('early acknowledgement cannot be demoted to dispatched', async () => {
  const {value,ctx}=fixture();
  await processRequest(ctx,'a'.repeat(32),value,{startNewTask:()=>{value.state='accepted';return Promise.resolve();}},()=>{});
  assert.equal(value.state,'accepted');
});
test('choice sent once via message, never tool approval buttons', async () => {
  const {value,ctx}=fixture();value.state='accepted';value.question={id:'b'.repeat(32),state:'answered',response:'Подробно'};
  let messages=0;
  const api={sendMessage:async text=>{messages++;assert.match(text,/consume/);assert.match(text,/HYP-2026-11-13-001/);},pressPrimaryButton:()=>assert.fail('No permission bypass')};
  await processRequest(ctx,'a'.repeat(32),value,api,()=>{});
  await processRequest(ctx,'a'.repeat(32),value,api,()=>{});
  assert.equal(messages,1);assert.equal(value.question.state,'sent');
});
test('synchronous API failure is visible and never accepted',async()=>{
 const {value,ctx}=fixture();
 await processRequest(ctx,'a'.repeat(32),value,{startNewTask:()=>{throw Error('Cline unavailable');}},()=>{});
 assert.equal(value.state,'failed');
});

'use strict';
// Invoked by the Python integration test on a real temporary workspace.
// Only Cline's API is doubled; request storage, allocation, source guards and acknowledgements are real.
const {promisify} = require('node:util');
const {execFile} = require('node:child_process');
const path = require('node:path');
const assert = require('node:assert/strict');
const {processRequest} = require('./protocol');
const execute = promisify(execFile);
const [root,framework,python,id] = process.argv.slice(2);
const ctx={root,framework,call:async(action,request,args=[])=>{
 const {stdout}=await execute(python,[path.join(framework,'scripts/tui_control.py'),action,'--workspace',root,'--request',request,...args],{env:{...process.env,PYTHONUTF8:'1'}});
 return JSON.parse(stdout);
}};
async function main(){
 let started=0,sent=0,accept;
 const api={startNewTask:prompt=>{started++;assert.match(prompt,/acknowledge/);accept=ctx.call('acknowledge',id);return accept;},sendMessage:async prompt=>{
  sent++;assert.match(prompt,/consume/);
  const status=await ctx.call('status',id);
  await ctx.call('consume',id,['--question-id',status.question.id]);
 }};
 let status=await ctx.call('status',id);
 await processRequest(ctx,id,status,api,()=>{});await accept;
 status=await ctx.call('status',id);assert.equal(status.state,'accepted');
 const question=await ctx.call('ask',id,['--phase','validation','--question','Подтвердить контекст?','--option','Продолжить','--option','Уточнить']);
 await ctx.call('answer',id,['--question-id',question.id,'--response','Продолжить']);
 status=await ctx.call('status',id);await processRequest(ctx,id,status,api,()=>{});
 status=await ctx.call('status',id);assert.equal(status.question.state,'consumed');
 await processRequest(ctx,id,status,api,()=>{});
 assert.equal(started,1);assert.equal(sent,1);
 console.log(JSON.stringify({started,sent,response:status.question.response,state:status.state}));
}
main().catch(e=>{console.error(e);process.exitCode=1;});

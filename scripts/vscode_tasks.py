"""Generate and surgically merge one HST task, preserving user JSONC content."""
import json
from pathlib import Path

LABEL='HST · Прогресс'


def tokens(text):
    """Token offsets ignore comments; strings are decoded, never mistaken for structure."""
    i=0
    while i<len(text):
        if text[i].isspace() or text[i]=='\ufeff':i+=1;continue
        if text.startswith('//',i):
            end=text.find('\n',i);i=len(text) if end<0 else end+1;continue
        if text.startswith('/*',i):
            end=text.find('*/',i+2)
            if end<0:raise ValueError('Unclosed JSONC comment')
            i=end+2;continue
        start=i
        if text[i]=='"':
            i+=1
            while i<len(text):
                if text[i]=='\\':i+=2;continue
                if text[i]=='"':i+=1;break
                i+=1
            value=json.loads(text[start:i]);yield 'string',start,i,value
        else:
            yield text[i],i,i+1,text[i];i+=1


def parse(text):
    tok=list(tokens(text));chars=list(text)
    # Strip comments outside strings while preserving exact offsets.
    keep=[False]*len(text)
    for _,a,b,_ in tok:keep[a:b]=[True]*(b-a)
    for i,c in enumerate(chars):
        if not keep[i] and not c.isspace():chars[i]=' '
    for i,t in enumerate(tok[:-1]):
        if t[0]==',' and tok[i+1][0] in {']','}'}:chars[t[1]]=' '
    def unique(pairs):
        value={}
        for key,item in pairs:
            if key in value:raise ValueError('Duplicate JSONC key: '+key)
            value[key]=item
        return value
    data=json.loads(''.join(chars),object_pairs_hook=unique)
    if not isinstance(data,dict):raise ValueError('tasks.json must be an object')
    return data,tok


def task(workspace,framework):
    workspace,framework=Path(workspace).resolve(),Path(framework).resolve()
    # VS Code executes an argument vector, not a shell-interpolated command.
    return {'label':LABEL,'type':'process',
        'command':'${workspaceFolder}/.hst/terminal-venv/bin/python',
        'windows':{'command':'${workspaceFolder}/.hst/terminal-venv/Scripts/python.exe'},
        'args':[str(framework/'scripts/terminal_progress.py'),'--workspace','${workspaceFolder}'],
        'options':{'cwd':'${workspaceFolder}','env':{'PYTHONUTF8':'1'}},
        'problemMatcher':[],
        'presentation':{'reveal':'always','focus':False,'panel':'dedicated','clear':True,
                        'echo':False,'showReuseMessage':False,'close':False},
        'runOptions':{'runOn':'folderOpen','instanceLimit':1}}


def merge(text, entry, replace=False):
    """Return (new text, changed-owned-entry). Other task bytes remain unchanged."""
    if not text.strip():
        return json.dumps({'version':'2.0.0','tasks':[entry]},ensure_ascii=False,indent=2)+'\n',False
    data,tok=parse(text)
    existing=data.get('tasks',[])
    if not isinstance(existing,list):raise ValueError('tasks must be an array')
    matches=[x for x in existing if isinstance(x,dict) and x.get('label')==LABEL]
    if len(matches)>1:raise ValueError('Duplicate HST task labels; resolve before install')
    if matches and matches[0]==entry:return text,False
    if matches and not replace:return text,True
    # Find a top-level tasks property, then its array and direct item spans.
    depth=0;start_index=None
    for i,t in enumerate(tok):
        if t[0]=='string' and t[3]=='tasks' and depth==1 and tok[i+1][0]==':':
            if tok[i+2][0]!='[':raise ValueError('tasks must be an array')
            start_index=i+2;break
        if t[0] in {'{','['}:depth+=1
        elif t[0] in {'}',']'}:depth-=1
    formatted=json.dumps(entry,ensure_ascii=False,indent=2)
    formatted='\n'.join('    '+line for line in formatted.splitlines())
    if start_index is None:
        closing=next(t for t in reversed(tok) if t[0]=='}')
        before=next((t for t in reversed(tok) if t[2]<=closing[1]),None)
        comma='' if before is None or before[0] in {'{',','} else ','
        insertion=comma+'\n  "tasks": [\n'+formatted+'\n  ]\n'
        return text[:closing[1]]+insertion+text[closing[1]:],False
    nesting=0;items=[];item_start=None;end=None
    for t in tok[start_index:]:
        kind,a,b,_=t
        if nesting==1 and kind not in {',',']'} and item_start is None:item_start=a
        if kind in {'[','{'}:nesting+=1
        elif kind in {']','}'}:
            nesting-=1
            if nesting==0:
                if item_start is not None:items.append((item_start,a))
                end=a;break
        if kind==',' and nesting==1 and item_start is not None:
            items.append((item_start,a));item_start=None
    if end is None:raise ValueError('Unclosed tasks array')
    if len(items)!=len(existing):raise ValueError('Cannot safely merge task spans')
    if matches:
        index=next(i for i,x in enumerate(existing) if isinstance(x,dict) and x.get('label')==LABEL)
        a,b=items[index]
        # Keep task-adjacent comments/whitespace; replace only the managed object's tokens.
        last=next(t for t in reversed(tok) if t[1]<b and t[2]>a)
        return text[:a]+formatted.lstrip()+text[last[2]:],True
    preceding=next(t for t in reversed(tok) if t[2]<=end)
    comma='' if preceding[0] in {'[',','} else ','
    return text[:end]+comma+'\n'+formatted+'\n  '+text[end:],False

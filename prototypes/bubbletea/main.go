package main

import (
 "flag"
 "fmt"
 "os"
 "os/exec"
 "path/filepath"
 "runtime"
 "strings"
 "time"

 tea "charm.land/bubbletea/v2"
)

type tickMsg time.Time
type loadedMsg struct { generation int; runs []run; data snapshot; err error }
type openedMsg struct { err error }
type model struct {
 demo bool
 workspace string
 runs []run
 selected int
 data snapshot
 page int
 cursor int
 draft [3]bool
 dirty bool
 offset int
 width, height int
 notice string
 generation int
 step int
 paused bool
 waiting bool
}

func tick() tea.Cmd { return tea.Tick(time.Second,func(t time.Time) tea.Msg { return tickMsg(t) }) }
func (m model) load() tea.Cmd {
 generation,root,id:=m.generation,m.workspace,m.data.Run
 return func() tea.Msg {
  runs,err:=listRuns(root)
  if err!=nil { return loadedMsg{generation:generation,err:err} }
  if id=="" && len(runs)>0 { id=runs[0].ID }
  data,err:=readSnapshot(root,id)
  return loadedMsg{generation:generation,runs:runs,data:data,err:err}
 }
}
func (m model) Init() tea.Cmd {
 if m.demo { return tick() }
 return tea.Batch(tick(),m.load())
}
func (m *model) choose(i int) {
 if len(m.runs)==0 { return }
 m.selected=max(0,min(i,len(m.runs)-1));m.offset=0;m.dirty=false;m.generation++
 if m.demo { m.data=demoSnapshot(m.selected);m.step=0;m.waiting=false;m.paused=false;m.draft=[3]bool{true,true,true} } else { m.data=snapshot{Run:m.runs[m.selected].ID} }
}
func (m model) Update(message tea.Msg) (tea.Model,tea.Cmd) {
 switch msg:=message.(type) {
 case tea.WindowSizeMsg:
  m.width,m.height=msg.Width,msg.Height
 case loadedMsg:
  if msg.generation!=m.generation { return m,nil }
  if msg.err!=nil { m.notice="Не удалось прочитать: "+safe(msg.err.Error());return m,nil }
  m.runs=msg.runs;m.data=msg.data
  for i,r:=range m.runs { if r.ID==m.data.Run { m.selected=i } }
  if !m.dirty { for i,k:=range channels { m.draft[i]=m.data.Sources[k] } }
  m.notice=""
 case openedMsg:
  if msg.err!=nil { m.notice="Не удалось открыть: "+safe(msg.err.Error()) } else { m.notice="Отчёт открыт в браузере" }
 case tickMsg:
  if m.demo {
   if m.page==2 && m.selected==0 && !m.paused && !m.waiting { m.advanceDemo() }
   return m,tick()
  }
  return m,tea.Batch(tick(),m.load())
 case tea.KeyPressMsg:
  key:=msg.String()
  switch key {
  case "ctrl+c","q": return m,tea.Quit
  case "tab": m.page=(m.page+1)%3;m.offset=0
  case "shift+tab":m.page=(m.page+2)%3;m.offset=0
  case "r": if m.demo { m.choose(m.selected) } else { return m,m.load() }
  case "o": return m,m.openReport()
  case "p": if m.demo && m.page==2 { m.paused=!m.paused }
  case "enter":
   if m.page==0 && len(m.runs)>0 { m.page=1 } else if m.page==1 { m.page=2 }
  case "up","k":
   if m.page==0 { m.choose(m.selected-1);if !m.demo { return m,m.load() } } else if m.page==1 { m.cursor=max(0,m.cursor-1) } else { m.offset=min(max(0,len(m.data.Events)-1),m.offset+1) }
  case "down","j":
   if m.page==0 { m.choose(m.selected+1);if !m.demo { return m,m.load() } } else if m.page==1 { m.cursor=min(2,m.cursor+1) } else { m.offset=max(0,m.offset-1) }
  case "pgup": if m.page==2 { m.offset=min(max(0,len(m.data.Events)-1),m.offset+5) }
  case "pgdown": if m.page==2 { m.offset=max(0,m.offset-5) }
  case "home": if m.page==2 { m.offset=0 }
  case "space":if m.page==1 { m.draft[m.cursor]=!m.draft[m.cursor];m.dirty=true }
  case "1","2","3":
   if m.page==1 { i:=int(key[0]-'1');m.cursor=i;m.draft[i]=!m.draft[i];m.dirty=true }
   if m.demo && m.page==2 && m.waiting {
    m.waiting=false;m.data.add("local_evidence","running","ДЕМО: выбран вариант "+map[string]string{"1":"быстро","2":"подробно","3":"пропустить"}[key]);m.step++
   }
  }
 }
 return m,nil
}

func (m model) openReport() tea.Cmd {
 root,id,demo:=m.workspace,m.data.Run,m.demo
 return func() tea.Msg {
  var path string;var err error
  if demo {
   executable,e:=os.Executable();if e!=nil { return openedMsg{e} };path=filepath.Join(filepath.Dir(executable),"demo-report.html")
  } else { path,err=within(root,filepath.Join("runs",id,"outputs","human_report.html"));if err!=nil {return openedMsg{err}} }
  if _,err=os.Stat(path);err!=nil {return openedMsg{fmt.Errorf("отчёт ещё не создан: %w",err)}}
  var command *exec.Cmd
  switch runtime.GOOS {
  case "windows":command=exec.Command("rundll32","url.dll,FileProtocolHandler",path)
  case "darwin":command=exec.Command("open",path)
  default:command=exec.Command("xdg-open",path)
  }
  return openedMsg{command.Run()}
 }
}

func (m model) View() tea.View {
 width:=max(36,m.width-4);bodyHeight:=max(5,m.height-11)
 mode:="ПРОСМОТР ФАЙЛОВ · без управления Cline"
 if m.demo { mode="ДЕМО · синтетические события" }
 title:=paint("1;34","HST / ТЕРМИНАЛЬНЫЙ ПРОТОТИП")
 completed:=0;for _,p:=range m.data.Phases { if p.State=="completed" {completed++} }
 status:=fmt.Sprintf("%s   %d/10 этапов",safe(m.data.Run),completed)
 if m.data.Validation!="" {status+="   Проверка: "+safe(m.data.Validation)}
 var tabs []string
 for i,label:=range []string{"Прогоны","Источники","Журнал"} { if i==m.page {tabs=append(tabs,paint("1;34","["+label+"]"))} else {tabs=append(tabs,label)} }
 var body []string
 switch m.page {
 case 0:
  body=append(body,"Выбери прогон стрелками. Enter — к выбору источников.","")
  if len(m.runs)==0 {body=append(body,"Прогонов пока нет. Начни новый прогон в Cline.")}
  start:=max(0,m.selected-max(1,bodyHeight-4))
  for i:=start;i<len(m.runs)&&len(body)<bodyHeight;i++ {prefix:="  ";if i==m.selected {prefix="▶ "};line:=prefix+safe(m.runs[i].ID);if i==m.selected {line=paint("1;34",line)};body=append(body,line)}
  body=append(body,"","Выбор здесь меняет только просмотр.")
 case 1:
  body=append(body,"ЧЕРНОВИК ИСТОЧНИКОВ", "Space или 1/2/3 — переключить. Enter — показать журнал.", "")
  for i,label:=range []string{"Локальная база знаний","Confluence","Интернет"} {mark:=" ";if m.draft[i] {mark="✓"};prefix:="  ";if i==m.cursor {prefix="▶ "};line:=fmt.Sprintf("%s[%s] %s",prefix,mark,label);if i==m.cursor {line=paint("1;34",line)};body=append(body,line)}
  body=append(body,"")
  if m.demo { body=append(body,"Выбор влияет только на демонстрацию.") } else {body=append(body,"В этом прототипе черновик НЕ сохраняется в настройках прогона.","Действующие разрешения Cline остаются прежними.")}
 case 2:
  phaseRows:=min(5,max(0,bodyHeight/3))
  logBudget:=max(2,bodyHeight-phaseRows-3)
  body=append(body,"ЖУРНАЛ · новые сверху · ↑/↓ прокрутка · Home к свежим")
  if m.demo && m.waiting {body=append(body,paint("1;33","Нужен выбор: 1 быстро · 2 подробно · 3 пропустить"));logBudget--}
  if m.demo && m.paused {body=append(body,paint("1;33","Демонстрация на паузе · P продолжить"));logBudget--}
  if m.offset>0 {body=append(body,fmt.Sprintf("История: отступ %d событий · Home вернёт новые",m.offset));logBudget--}
  count:=0
  for i:=len(m.data.Events)-1-m.offset;i>=0&&count<logBudget;i-- {
   e:=m.data.Events[i];clock:="--:--:--";if t,err:=time.Parse(time.RFC3339,e.At);err==nil {clock=t.In(time.FixedZone("МСК",3*3600)).Format("15:04:05")}
   name:=phaseName(e.Phase);if e.Channel!="" {name=channelName(e.Channel)}
   line:=clock+"  "+stateName(e.State)+" · "+name+" · "+safe(e.Message)
   for _,part:=range wrap(line,width) {if count>=logBudget {break};body=append(body,paint(stateColor(e.State),part));count++}
  }
  if len(m.data.Events)==0 {body=append(body,"Журнал ещё не появился. R — обновить.")}
  body=append(body,"","ЭТАПЫ · по порядку")
  for i:=0;i<len(m.data.Phases)&&i<phaseRows*2;i+=2 {
   cells:=[]string{}
   for j:=i;j<min(i+2,len(m.data.Phases));j++ {p:=m.data.Phases[j];mark:="·";if p.State=="completed" {mark="✓"} else if p.State=="running" {mark="▶"};cells=append(cells,fmt.Sprintf("%s %02d %s: %s",mark,j+1,phaseName(p.ID),stateName(p.State)))}
   body=append(body,strings.Join(cells,"  |  "))
  }
 }
 if len(body)>bodyHeight {body=body[:bodyHeight]}
 for len(body)<bodyHeight {body=append(body,"")}
 help:="Tab экран · O отчёт · R обновить · Q выход"
 if m.demo {help+=" · P пауза демо"}
 notice:=safe(m.notice)
 content:=title+"\n"+mode+"\n"+status+"\n\n"+strings.Join(tabs,"   ")+"\n"+strings.Repeat("─",width)+"\n"+strings.Join(body,"\n")+"\n"+notice+"\n"+help
 view:=tea.NewView(content);view.AltScreen=true;view.WindowTitle="HST · Bubble Tea prototype"
 return view
}

func main() {
 workspace:=flag.String("workspace","","Корень DataB: только чтение реальных прогонов")
 demo:=flag.Bool("demo",false,"Демонстрация без записи файлов")
 flag.Parse()
 if *workspace!="" && *demo {fmt.Fprintln(os.Stderr,"Выбери --demo или --workspace");os.Exit(2)}
 m:=model{demo:*demo||*workspace=="",width:110,height:36,draft:[3]bool{true,true,true}}
 if m.demo {m.runs=[]run{{ID:"DEMO-001 · новый прогон"},{ID:"DEMO-002 · завершён"},{ID:"DEMO-003 · ошибка доступа"}};m.data=demoSnapshot(0)} else {
  root,err:=filepath.EvalSymlinks(*workspace);if err!=nil {fmt.Fprintln(os.Stderr,err);os.Exit(2)}
  m.workspace,err=filepath.Abs(root);if err!=nil {fmt.Fprintln(os.Stderr,err);os.Exit(2)}
 }
 if _,err:=tea.NewProgram(m).Run();err!=nil {fmt.Fprintln(os.Stderr,err);os.Exit(1)}
}

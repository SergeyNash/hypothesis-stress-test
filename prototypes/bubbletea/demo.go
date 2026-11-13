package main

import "time"

func (s *snapshot) add(id,state,message string) {
 s.Events=append(s.Events,event{At:time.Now().UTC().Format(time.RFC3339),Kind:"phase",Phase:id,State:state,Message:message})
 for i,p:=range s.Phases {if p.ID==id {s.Phases[i].State=state}}
}
func demoSnapshot(index int) snapshot {
 s:=emptySnapshot([]string{"DEMO-001 · новый прогон","DEMO-002 · завершён","DEMO-003 · ошибка доступа"}[index])
 s.Sources=map[string]bool{"local":true,"confluence":true,"internet":true}
 if index==1 {for _,p:=range phaseIDs {s.add(p,"completed","ДЕМО: этап завершён")};s.Validation="PASS"}
 if index==2 {
  for _,p:=range phaseIDs[:4] {s.add(p,"completed","ДЕМО: этап завершён")}
  s.add("business_context","waiting_user","ДЕМО: Confluence недоступен. Требуется решение пользователя в Cline.")
  s.Events=append(s.Events,event{At:time.Now().UTC().Format(time.RFC3339),Kind:"source",Phase:"business_context",Channel:"confluence",State:"auth_error",Message:"ДЕМО: HTTP 401, источник не прочитан"})
 }
 return s
}
func (m *model) advanceDemo() {
 if m.step>=len(phaseIDs)*2 {m.data.Validation="PASS";return}
 index:=m.step/2;id:=phaseIDs[index]
 if m.step%2==0 {
  if id=="local_evidence"&&m.draft[0] {m.data.add(id,"waiting_user","ДЕМО: найдены таблицы. Выбери глубину анализа.");m.waiting=true;return}
  m.data.add(id,"running","ДЕМО: подготовка этапа; модель и источники не вызываются")
 } else {m.data.add(id,"completed","ДЕМО: этап завершён")}
 m.step++
 if m.step==len(phaseIDs)*2 {m.data.Validation="PASS"}
}

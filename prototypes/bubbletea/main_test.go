package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
)

func TestSourceDraftAndDemoWait(t *testing.T) {
	m := model{demo: true, page: 1, runs: []run{{ID: "demo"}}, data: demoSnapshot(0), draft: [3]bool{true, true, true}}
	next, _ := m.Update(tea.KeyPressMsg{Code: ' '})
	m = next.(model)
	if m.draft[0] {
		t.Fatal("space did not toggle source")
	}
	m.page = 2
	m.draft[0] = true
	m.step = 6
	m.advanceDemo()
	if !m.waiting || m.data.Phases[3].State != "waiting_user" {
		t.Fatal("missing real demo wait")
	}
	next, _ = m.Update(tea.KeyPressMsg{Code: '1'})
	m = next.(model)
	if m.waiting || m.step != 7 {
		t.Fatal("demo answer did not continue")
	}
}
func TestSourceDraftDoesNotMutateObservedSettings(t *testing.T) {
	m := model{demo: true, page: 1, data: demoSnapshot(0), draft: [3]bool{true, true, true}}
	next, _ := m.Update(tea.KeyPressMsg{Code: '1'})
	m = next.(model)
	if !m.data.Sources["local"] || m.draft[0] {
		t.Fatal("observed settings were mutated")
	}
}
func TestEscapesAreNeverInterpretedFromJournal(t *testing.T) {
	actual := safe("text\x1b[31mRED\x1b[0m\x1b]8;;https://bad.test\x07link\x1b]8;;\x07\u202e")
	if strings.ContainsAny(actual, "\x1b\x07\u202e") {
		t.Fatal("terminal instructions leaked")
	}
}
func TestWorkspaceReadUsesJournalAndKeepsFilesUnchanged(t *testing.T) {
	root := t.TempDir()
	id := "HYP-2026-11-13-001"
	out := filepath.Join(root, "runs", id, "outputs")
	if err := os.MkdirAll(out, 0700); err != nil {
		t.Fatal(err)
	}
	row := `{"kind":"phase","phase":"intake","state":"completed","message":"test","at":"2026-11-13T07:30:11Z"}`
	path := filepath.Join(out, "pipeline_events.jsonl")
	os.WriteFile(path, []byte(row+"\n"), 0600)
	os.WriteFile(filepath.Join(out, "progress.json"), []byte("{stale"), 0600)
	s, err := readSnapshot(root, id)
	if err != nil {
		t.Fatal(err)
	}
	if s.Phases[0].State != "completed" {
		t.Fatal("did not reconstruct durable events")
	}
	after, _ := os.ReadFile(path)
	if string(after) != row+"\n" {
		t.Fatal("viewer changed the journal")
	}
	runs, err := listRuns(root)
	if err != nil || len(runs) != 1 {
		t.Fatal(runs, err)
	}
}
func TestOutsidePathAndInvalidIDsAreRejected(t *testing.T) {
	root := t.TempDir()
	outside := t.TempDir()
	os.WriteFile(filepath.Join(outside, "secret"), []byte("private"), 0600)
	rel, _ := filepath.Rel(root, filepath.Join(outside, "secret"))
	if _, err := within(root, rel); err == nil {
		t.Fatal("outside path accepted")
	}
	if _, err := readSnapshot(root, "../other"); err == nil {
		t.Fatal("invalid run ID accepted")
	}
}
func TestValidationMustBelongToSelectedRun(t *testing.T) {
	root := t.TempDir()
	id := "HYP-2026-11-13-001"
	out := filepath.Join(root, "runs", id, "outputs")
	os.MkdirAll(out, 0700)
	body, _ := json.Marshal(map[string]string{"scope": "run", "target": filepath.Join(root, "runs", "HYP-2026-11-13-002"), "status": "PASS"})
	os.WriteFile(filepath.Join(out, "run_validation.json"), body, 0600)
	s, err := readSnapshot(root, id)
	if err != nil {
		t.Fatal(err)
	}
	if s.Validation != "" {
		t.Fatal("another run's PASS displayed")
	}
}
func TestSwitchingDemoDoesNotMixHistory(t *testing.T) {
	m := model{demo: true, runs: []run{{ID: "a"}, {ID: "b"}, {ID: "c"}}, data: demoSnapshot(1)}
	m.choose(0)
	if len(m.data.Events) != 0 || m.data.Validation != "" {
		t.Fatal("previous run leaked")
	}
}
func TestViewHasHonestPrototypeLabels(t *testing.T) {
	m := model{width: 110, height: 36, page: 1, data: demoSnapshot(0)}
	content := safe(m.View().Content)
	if !strings.Contains(content, "ПРОСМОТР ФАЙЛОВ") || !strings.Contains(content, "только чтение") || strings.Contains(content, "переключить") || strings.Contains(content, "ЧЕРНОВИК") {
		t.Fatal("real source draft looks like applied control")
	}
	m.demo = true
	if !strings.Contains(safe(m.View().Content), "ДЕМО") {
		t.Fatal("demo not labelled")
	}
}

func TestRealSourcesIgnoreToggleKeys(t *testing.T) {
	m := model{page: 1, data: demoSnapshot(0), draft: [3]bool{true, true, true}}
	for _, key := range []rune{' ', '1', '2', '3'} {
		next, _ := m.Update(tea.KeyPressMsg{Code: key})
		m = next.(model)
	}
	if m.dirty || m.draft != [3]bool{true, true, true} || !m.data.Sources["local"] || !m.data.Sources["confluence"] || !m.data.Sources["internet"] {
		t.Fatal("real sources accepted editing")
	}
	content := safe(m.View().Content)
	if strings.Contains(content, "[✓]") || strings.Contains(content, "Space") || !strings.Contains(content, "ИСТОЧНИКИ ЭТОГО ПРОГОНА") {
		t.Fatal("real source view offers controls")
	}
}

func TestSourceSelectionAndActivityAreSeparate(t *testing.T) {
	s := emptySnapshot("HYP-2026-11-13-001")
	if s.sourceSetting("local") != "Нет данных о выборе" || s.sourceActivity("local") != "Обращения не записаны" {
		t.Fatal("missing history was presented as a choice or read")
	}
	s.Sources["local"] = true
	s.Sources["internet"] = false
	if s.sourceSetting("local") != "Включён" || s.sourceSetting("internet") != "Отключён" || s.sourceActivity("local") != "Обращения не записаны" {
		t.Fatal("enabled source was confused with access")
	}
	s.Events = []event{
		{Kind: "source", Channel: "local", State: "read"},
		{Kind: "source", Channel: "local", State: "used"},
		{Kind: "source", Channel: "confluence", State: "auth_error"},
		{Kind: "phase", Channel: "local", State: "read"},
		{Kind: "source", Channel: "local", State: "error"},
	}
	activity := s.sourceActivity("local")
	if !strings.Contains(activity, "чтения: 1") || !strings.Contains(activity, "использования: 1") || !strings.Contains(activity, "последнее: Ошибка") {
		t.Fatal(activity)
	}
	if !strings.Contains(s.sourceActivity("confluence"), "Ошибка доступа") || s.sourceSetting("confluence") != "Нет данных о выборе" {
		t.Fatal("events fabricated a saved choice")
	}
}

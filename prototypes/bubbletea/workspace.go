package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"unicode"
	"unicode/utf8"
)

type run struct{ ID string }
type phase struct {
	ID    string `json:"id"`
	State string `json:"state"`
}
type event struct {
	At      string `json:"at"`
	Kind    string `json:"kind"`
	Phase   string `json:"phase"`
	State   string `json:"state"`
	Message string `json:"message"`
	Channel string `json:"channel"`
}
type snapshot struct {
	Run        string
	Phases     []phase
	Events     []event
	Sources    map[string]bool
	Validation string
}

var channels = []string{"local", "confluence", "internet"}
var phaseIDs = []string{"intake", "validation", "facilitator", "local_evidence", "business_context", "market", "synthesis", "customer_discovery_planning", "decision_review", "human_report"}
var phaseNames = []string{"Гипотеза", "Входные данные", "Роли", "Локальные материалы", "Бизнес-контекст", "Рынок", "Синтез", "План проверки", "Разбор решения", "Отчёт"}
var runID = regexp.MustCompile(`^HYP-\d{4}-\d{2}-\d{2}-\d{3}$`)
var escape = regexp.MustCompile("\x1b\\][^\x07\x1b]*(?:\x07|\x1b\\\\)|\x1b\\[[0-?]*[ -/]*[@-~]")

func safe(value string) string {
	value = escape.ReplaceAllString(value, "")
	return strings.Map(func(r rune) rune {
		if unicode.IsControl(r) || r >= 0x202a && r <= 0x202e || r >= 0x2066 && r <= 0x2069 {
			return ' '
		}
		return r
	}, value)
}
func paint(color, text string) string { return "\x1b[" + color + "m" + text + "\x1b[0m" }
func wrap(text string, width int) []string {
	if width < 1 {
		width = 1
	}
	var result []string
	for utf8.RuneCountInString(text) > width {
		chars := []rune(text)
		cut := width
		for i := width; i > width/2; i-- {
			if chars[i-1] == ' ' {
				cut = i
				break
			}
		}
		result = append(result, string(chars[:cut]))
		text = strings.TrimLeft(string(chars[cut:]), " ")
	}
	return append(result, text)
}
func phaseName(id string) string {
	for i, k := range phaseIDs {
		if id == k {
			return phaseNames[i]
		}
	}
	return safe(id)
}
func channelName(id string) string {
	switch id {
	case "local":
		return "Локальные"
	case "confluence":
		return "Confluence"
	case "internet":
		return "Интернет"
	}
	return safe(id)
}
func stateName(id string) string {
	names := map[string]string{"pending": "Ожидает", "running": "Выполняется", "completed": "Готово", "waiting_user": "Нужен ответ", "error": "Ошибка", "declined": "Отключён", "read": "Прочитано", "found": "Найдено", "query_started": "Поиск", "used": "Использовано", "auth_error": "Ошибка доступа", "invalidated": "Нужно обновить", "no_results": "Нет результатов", "partial": "Частично", "unavailable": "Недоступен", "waiting_approval": "Нужно разрешение"}
	if name, ok := names[id]; ok {
		return name
	}
	return safe(id)
}
func stateColor(id string) string {
	switch id {
	case "completed", "used":
		return "32"
	case "error", "auth_error":
		return "31"
	case "waiting_user":
		return "33"
	case "running":
		return "34"
	}
	return "0"
}
func emptySnapshot(id string) snapshot {
	s := snapshot{Run: id, Sources: map[string]bool{}}
	for _, id := range phaseIDs {
		s.Phases = append(s.Phases, phase{ID: id, State: "pending"})
	}
	return s
}
func within(root, relative string) (string, error) {
	if filepath.IsAbs(relative) {
		return "", fmt.Errorf("ожидался относительный путь")
	}
	root, err := filepath.EvalSymlinks(root)
	if err != nil {
		return "", err
	}
	path, err := filepath.EvalSymlinks(filepath.Join(root, relative))
	if err != nil {
		return "", err
	}
	rel, err := filepath.Rel(root, path)
	if err != nil || rel == ".." || strings.HasPrefix(rel, ".."+string(filepath.Separator)) {
		return "", fmt.Errorf("путь вне рабочей папки")
	}
	return path, nil
}
func readFile(root, relative string) ([]byte, error) {
	path, err := within(root, relative)
	if err != nil {
		return nil, err
	}
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	data, err := io.ReadAll(io.LimitReader(f, 16*1024*1024+1))
	if err != nil {
		return nil, err
	}
	if len(data) > 16*1024*1024 {
		return nil, fmt.Errorf("файл больше 16 МБ")
	}
	return data, nil
}
func listRuns(root string) ([]run, error) {
	directory, err := within(root, "runs")
	if os.IsNotExist(err) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	entries, err := os.ReadDir(directory)
	if err != nil {
		return nil, err
	}
	var result []run
	for _, e := range entries {
		if e.IsDir() && e.Type()&os.ModeSymlink == 0 && runID.MatchString(e.Name()) {
			result = append(result, run{ID: e.Name()})
		}
	}
	sort.Slice(result, func(i, j int) bool { return result[i].ID > result[j].ID })
	if len(result) > 2000 {
		result = result[:2000]
	}
	return result, nil
}
func readSnapshot(root, id string) (snapshot, error) {
	s := emptySnapshot(id)
	if id == "" {
		return s, nil
	}
	if !runID.MatchString(id) {
		return s, fmt.Errorf("некорректный HYP-ID")
	}
	base := filepath.Join("runs", id)
	data, err := readFile(root, filepath.Join(base, "outputs", "pipeline_events.jsonl"))
	if err == nil {
		scanner := bufio.NewScanner(strings.NewReader(string(data)))
		scanner.Buffer(make([]byte, 4096), 1024*1024)
		for scanner.Scan() {
			if strings.TrimSpace(scanner.Text()) == "" {
				continue
			}
			var e event
			if err = json.Unmarshal(scanner.Bytes(), &e); err != nil {
				return s, fmt.Errorf("журнал временно недоступен: %w", err)
			}
			s.Events = append(s.Events, e)
		}
		if err = scanner.Err(); err != nil {
			return s, err
		}
	} else if os.IsNotExist(err) {
		data, err = readFile(root, filepath.Join(base, "outputs", "progress.json"))
		if err == nil {
			var saved struct {
				Run    string  `json:"run"`
				Events []event `json:"events"`
			}
			if err = json.Unmarshal(data, &saved); err != nil {
				return s, err
			}
			if saved.Run != id {
				return s, fmt.Errorf("журнал относится к другому прогону")
			}
			s.Events = saved.Events
		} else if !os.IsNotExist(err) {
			return s, err
		}
	} else {
		return s, err
	}
	for _, e := range s.Events {
		if e.Kind == "phase" {
			for i, p := range s.Phases {
				if p.ID == e.Phase {
					s.Phases[i].State = e.State
				}
			}
		}
	}
	data, err = readFile(root, filepath.Join(base, "run_config.json"))
	if err == nil {
		var config struct {
			Selection struct {
				Channels map[string]bool `json:"channels"`
			} `json:"source_selection"`
		}
		if err = json.Unmarshal(data, &config); err != nil {
			return s, err
		}
		s.Sources = config.Selection.Channels
	} else if !os.IsNotExist(err) {
		return s, err
	}
	data, err = readFile(root, filepath.Join(base, "outputs", "run_validation.json"))
	if err == nil {
		var v struct {
			Scope  string `json:"scope"`
			Target string `json:"target"`
			Status string `json:"status"`
		}
		if err = json.Unmarshal(data, &v); err != nil {
			return s, err
		}
		target, _ := filepath.Abs(filepath.Join(root, base))
		if v.Scope == "run" && filepath.Clean(v.Target) == target {
			s.Validation = v.Status
		}
	} else if !os.IsNotExist(err) {
		return s, err
	}
	return s, nil
}

// A missing choice must not be confused with an explicit opt-out.
func (s snapshot) sourceSetting(channel string) string {
	enabled, recorded := s.Sources[channel]
	if !recorded {
		return "Нет данных о выборе"
	}
	if enabled {
		return "Включён"
	}
	return "Отключён"
}

// Counts are journal events, not unique documents or independently verified evidence.
func (s snapshot) sourceActivity(channel string) string {
	reads, uses := 0, 0
	last := ""
	for _, e := range s.Events {
		if e.Kind != "source" || e.Channel != channel {
			continue
		}
		last = e.State
		if e.State == "read" {
			reads++
		}
		if e.State == "used" {
			uses++
		}
	}
	if last == "" {
		return "Обращения не записаны"
	}
	return fmt.Sprintf("Событий чтения: %d · использования: %d · последнее: %s", reads, uses, stateName(last))
}

// Startup is workspace state, not a fabricated HYP run or completed phase.
func readStartup(root string) (string, error) {
 data, err := readFile(root, filepath.Join(".hst", "startup.json"))
 if os.IsNotExist(err) { return "", nil }
 if err != nil { return "", err }
 if len(data) > 16384 { return "", fmt.Errorf("слишком большое состояние подготовки") }
 var value struct {
  Version int `json:"schema_version"`
  Session string `json:"session_id"`
  State string `json:"state"`
  Stage string `json:"stage"`
  Message string `json:"message"`
  At string `json:"at"`
 }
 if err := json.Unmarshal(data, &value); err != nil { return "", err }
 if value.Version != 1 || !regexp.MustCompile(`^[a-f0-9]{32}$`).MatchString(value.Session) {
  return "", fmt.Errorf("некорректное состояние подготовки")
 }
 if value.State == "attached" || value.State == "cancelled" { return "", nil }
 if value.State != "running" && value.State != "waiting_user" && value.State != "error" {
  return "", fmt.Errorf("некорректный статус подготовки")
 }
 return "НОВАЯ ГИПОТЕЗА · до создания папки · " + stateName(value.State) + ": " + safe(value.Message) + " · " + safe(value.At), nil
}

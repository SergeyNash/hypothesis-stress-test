package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"

	tea "charm.land/bubbletea/v2"
)

type launchConfig struct {
	Statement  string          `json:"statement"`
	Profile    string          `json:"profile"`
	Type       string          `json:"hypothesis_type"`
	Domain     string          `json:"domain"`
	Audience   string          `json:"audience"`
	Scenario   string          `json:"scenario"`
	Roles      string          `json:"roles"`
	Channels   map[string]bool `json:"channels"`
	LocalPaths []string        `json:"local_paths"`
}
type controlQuestion struct {
	ID       string   `json:"id"`
	State    string   `json:"state"`
	Text     string   `json:"question"`
	Options  []string `json:"options"`
	Response string   `json:"response"`
}
type launchStatus struct {
	At         string           `json:"at"`
	Connection string           `json:"connection"`
	ID         string           `json:"request_id"`
	State      string           `json:"state"`
	Run        string           `json:"run_dir"`
	Message    string           `json:"message"`
	Question   *controlQuestion `json:"question"`
}
type controlMsg struct {
	value launchStatus
	err   error
}
type newForm struct {
	values   [8]string
	channels [3]bool
	cursor   int
	review   bool
}

var formNames = []string{"Гипотеза (Alt+Enter — новая строка)", "Профиль (←/→)", "Домен", "Заказчик / аудитория", "Сценарий", "Роли через ; (для сервиса укажи customer/provider)", "Тип сервисной гипотезы (←/→)", "Папки локальной базы через ; (пусто — вся база)"}
var serviceTypes = []string{"service_improvement", "new_service", "service_offer", "commercial_model", "delivery_model", "renewal_expansion"}

func freshForm() *newForm {
	f := &newForm{channels: [3]bool{true, true, true}}
	f.values[1] = "service_business"
	f.values[6] = "service_improvement"
	return f
}
func (f *newForm) config() launchConfig {
	paths := []string{}
	for _, p := range strings.Split(f.values[7], ";") {
		if strings.TrimSpace(p) != "" {
			paths = append(paths, strings.TrimSpace(p))
		}
	}
	return launchConfig{Statement: f.values[0], Profile: f.values[1], Domain: f.values[2], Audience: f.values[3], Scenario: f.values[4], Roles: f.values[5], Type: f.values[6], LocalPaths: paths, Channels: map[string]bool{"local": f.channels[0], "confluence": f.channels[1], "internet": f.channels[2]}}
}
func backend(root string, action string, id string, payload any, args ...string) (launchStatus, error) {
	var result launchStatus
	data, err := readFile(root, filepath.Join(".hst", "workspace.json"))
	if err != nil {
		return result, fmt.Errorf("сначала подключи HST к базе: %w", err)
	}
	var setup struct {
		Framework string `json:"framework_dir"`
	}
	if err = json.Unmarshal(data, &setup); err != nil {
		return result, err
	}
	script, err := within(root, filepath.Join(setup.Framework, "scripts", "tui_control.py"))
	if err != nil {
		return result, err
	}
	python := "python"
	if runtime.GOOS != "windows" {
		python = "python3"
	}
	installed := filepath.Join(root, ".hst", "terminal-venv", "bin", "python")
	if runtime.GOOS == "windows" {
		installed = filepath.Join(root, ".hst", "terminal-venv", "Scripts", "python.exe")
	}
	if _, e := os.Stat(installed); e == nil {
		python = installed
	}
	commandArgs := []string{script, action, "--workspace", root}
	if id != "" {
		commandArgs = append(commandArgs, "--request", id)
	}
	commandArgs = append(commandArgs, args...)
	command := exec.Command(python, commandArgs...)
	command.Dir = root
	command.Env = append(os.Environ(), "PYTHONUTF8=1", "HST_COMMAND_ORIGIN=tui")
	if payload != nil {
		encoded, e := json.Marshal(payload)
		if e != nil {
			return result, e
		}
		command.Stdin = bytes.NewReader(encoded)
	}
	var diagnostic bytes.Buffer
	command.Stderr = &diagnostic
	output, e := command.Output()
	if e != nil {
		return result, fmt.Errorf("%s", strings.TrimSpace(diagnostic.String()+string(output)))
	}
	err = json.Unmarshal(output, &result)
	return result, err
}
func (m model) submitForm() tea.Cmd {
	root, config := m.workspace, m.form.config()
	return func() tea.Msg { value, err := backend(root, "submit", "", config); return controlMsg{value, err} }
}
func (m model) pollControl() tea.Cmd {
	root, id := m.workspace, m.control.ID
	return func() tea.Msg { value, err := backend(root, "status", id, nil); return controlMsg{value, err} }
}
func (m model) answerQuestion(response string) tea.Cmd {
	root, id, qid := m.workspace, m.control.ID, m.control.Question.ID
	return func() tea.Msg {
		_, err := backend(root, "answer", id, nil, "--question-id", qid, "--response", response)
		if err != nil {
			return controlMsg{err: err}
		}
		value, err := backend(root, "status", id, nil)
		return controlMsg{value, err}
	}
}
func (m model) updateForm(key string) (model, tea.Cmd) {
	f := m.form
	if key == "esc" {
		m.form = nil
		return m, nil
	}
	if f.review {
		if key == "enter" && !m.submitting {
			m.submitting = true
			return m, m.submitForm()
		}
		if key == "backspace" {
			f.review = false
		}
		return m, nil
	}
	switch key {
	case "tab", "down":
		f.cursor = (f.cursor + 1) % 11
	case "shift+tab", "up":
		f.cursor = (f.cursor + 10) % 11
	case "enter":
		if f.cursor == 10 {
			f.review = true
		} else {
			f.cursor++
		}
	case "backspace":
		if f.cursor < 8 && f.cursor != 1 && f.cursor != 6 {
			r := []rune(f.values[f.cursor])
			if len(r) > 0 {
				f.values[f.cursor] = string(r[:len(r)-1])
			}
		}
	case "left", "right":
		if f.cursor == 1 {
			if f.values[1] == "service_business" {
				f.values[1] = "digital_product"
			} else {
				f.values[1] = "service_business"
			}
		}
		if f.cursor == 6 {
			for i, s := range serviceTypes {
				if f.values[6] == s {
					f.values[6] = serviceTypes[(i+1)%len(serviceTypes)]
					break
				}
			}
		}
	case "space":
		if f.cursor >= 8 {
			f.channels[f.cursor-8] = !f.channels[f.cursor-8]
		} else if f.cursor != 1 && f.cursor != 6 {
			f.values[f.cursor] += " "
		}
	case "alt+enter":
		if f.cursor == 0 || f.cursor == 4 {
			f.values[f.cursor] += "\n"
		}
	default:
		if f.cursor < 8 && f.cursor != 1 && f.cursor != 6 && len([]rune(key)) == 1 && len(f.values[f.cursor]) < 20000 {
			f.values[f.cursor] += key
		}
	}
	return m, nil
}
func (m model) formView(width int) string {
	f := m.form
	lines := []string{paint("1;34", "HST / НОВЫЙ ПРОГОН"), "Папка создастся после Запустить. Будет открыта новая задача Cline.", ""}
	config := f.config()
	for i, name := range formNames {
		prefix := "  "
		if f.cursor == i && !f.review {
			prefix = "▶ "
		}
		value := f.values[i]
		if value == "" {
			value = "[не заполнено]"
		}
		fieldLines := wrap(prefix+name+": "+safe(value), width)
		if len(fieldLines) > 2 {
			fieldLines = fieldLines[:2]
			fieldLines[1] += " …"
		}
		lines = append(lines, fieldLines...)
	}
	for i, key := range channels {
		mark := "[ ]"
		if config.Channels[key] {
			mark = "[x]"
		}
		prefix := "  "
		if f.cursor == i+8 && !f.review {
			prefix = "▶ "
		}
		lines = append(lines, prefix+mark+" "+channelName(key))
	}
	if f.review {
		lines = append(lines, "", paint("1;33", "Enter — ЗАПУСТИТЬ НОВУЮ ЗАДАЧУ CLINE · Backspace — изменить"))
	} else {
		lines = append(lines, "", "Tab/↑/↓ — поле · Space — источник · ←/→ — профиль/тип · Enter — далее")
	}
	if m.submitting {
		lines = append(lines, "Сохраняю запрос…")
	}
	lines = append(lines, safe(m.notice), "Esc — отменить без создания прогона · Ctrl+C — выйти")
	return strings.Join(lines, "\n")
}
func controlLabel(state string) string {
	labels := map[string]string{"queued": "Настройки сохранены · ожидаю модуль связи", "allocated": "Папка создана · проверка входа", "prepared": "Источники применены · передача в Cline", "dispatching": "Вызываю Cline", "dispatched": "Передано Cline · ожидаю подтверждения", "accepted": "Cline принял запрос", "finished": "Прогон завершён · PASS", "failed": "Ошибка запуска", "cancelled": "Запуск отменён"}
	if label, ok := labels[state]; ok {
		return label
	}
	return state
}

func (m model) restoreControl() tea.Cmd {
	root := m.workspace
	return func() tea.Msg { value, err := backend(root, "current", "", nil); return controlMsg{value, err} }
}

package main

import (
	"encoding/json"
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

var version = "development"

type tickMsg time.Time
type loadedMsg struct {
	startup    string
	generation int
	runs       []run
	data       snapshot
	err        error
}
type openedMsg struct{ err error }
type model struct {
	form       *newForm
	control    launchStatus
	submitting bool
	answer     string

	startup       string
	demo          bool
	workspace     string
	runs          []run
	selected      int
	data          snapshot
	page          int
	cursor        int
	draft         [3]bool
	dirty         bool
	offset        int
	width, height int
	notice        string
	generation    int
	step          int
	paused        bool
	waiting       bool
}

func tick() tea.Cmd { return tea.Tick(time.Second, func(t time.Time) tea.Msg { return tickMsg(t) }) }
func (m model) load() tea.Cmd {
	generation, root, id := m.generation, m.workspace, m.data.Run
	return func() tea.Msg {
		runs, err := listRuns(root)
		if err != nil {
			return loadedMsg{generation: generation, err: err}
		}
		if id == "" && len(runs) > 0 {
			id = runs[0].ID
		}
		data, err := readSnapshot(root, id)
		startup, startupErr := readStartup(root)
		if err == nil {
			err = startupErr
		}
		return loadedMsg{generation: generation, runs: runs, data: data, err: err, startup: startup}
	}
}
func (m model) Init() tea.Cmd {
	if m.demo {
		return tick()
	}
	return tea.Batch(tick(), m.load(), m.restoreControl())
}
func (m *model) choose(i int) {
	if len(m.runs) == 0 {
		return
	}
	m.selected = max(0, min(i, len(m.runs)-1))
	m.offset = 0
	m.dirty = false
	m.generation++
	if m.demo {
		m.data = demoSnapshot(m.selected)
		m.step = 0
		m.waiting = false
		m.paused = false
		m.draft = [3]bool{true, true, true}
	} else {
		m.data = snapshot{Run: m.runs[m.selected].ID}
	}
}
func (m model) Update(message tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := message.(type) {
	case controlMsg:
		m.submitting = false
		if msg.err != nil {
			m.notice = safe(msg.err.Error())
			return m, nil
		}
		oldRun := m.control.Run
		m.control = msg.value
		m.notice = ""
		if m.control.ID != "" {
			m.form = nil
		}
		if m.control.Run != "" && m.control.Run != oldRun {
			m.data = snapshot{Run: filepath.Base(m.control.Run)}
			m.page = 2
			m.generation++
			return m, m.load()
		}
	case tea.PasteMsg:
		if m.form != nil && !m.form.review && m.form.cursor < 8 && m.form.cursor != 1 && m.form.cursor != 6 {
			m.form.values[m.form.cursor] += msg.Content
		} else if m.control.Question != nil && m.control.Question.State == "pending" && len(m.control.Question.Options) == 0 {
			m.answer += msg.Content
		}
	case tea.WindowSizeMsg:
		m.width, m.height = msg.Width, msg.Height
	case loadedMsg:
		if msg.generation != m.generation {
			return m, nil
		}
		if msg.err != nil {
			m.notice = "Не удалось прочитать: " + safe(msg.err.Error())
			return m, nil
		}
		m.startup = msg.startup
		m.runs = msg.runs
		m.data = msg.data
		for i, r := range m.runs {
			if r.ID == m.data.Run {
				m.selected = i
			}
		}
		if !m.dirty {
			for i, k := range channels {
				m.draft[i] = m.data.Sources[k]
			}
		}
		m.notice = ""
	case openedMsg:
		if msg.err != nil {
			m.notice = "Не удалось открыть: " + safe(msg.err.Error())
		} else {
			m.notice = "Отчёт открыт в браузере"
		}
	case tickMsg:
		if m.demo {
			if m.page == 2 && m.selected == 0 && !m.paused && !m.waiting {
				m.advanceDemo()
			}
			return m, tick()
		}
		if m.control.ID != "" {
			return m, tea.Batch(tick(), m.load(), m.pollControl())
		}
		return m, tea.Batch(tick(), m.load())
	case tea.KeyPressMsg:
		key := msg.String()
		if key == "ctrl+c" {
			return m, tea.Quit
		}
		if m.form != nil {
			return m.updateForm(key)
		}
		if !m.demo && m.control.Question != nil && m.control.Question.State == "pending" {
			q := m.control.Question
			if len(q.Options) > 0 && len(key) == 1 && key[0] >= '1' && int(key[0]-'1') < len(q.Options) {
				return m, m.answerQuestion(q.Options[int(key[0]-'1')])
			}
			if len(q.Options) == 0 {
				if key == "enter" && strings.TrimSpace(m.answer) != "" {
					answer := m.answer
					m.answer = ""
					return m, m.answerQuestion(answer)
				}
				if key == "backspace" {
					r := []rune(m.answer)
					if len(r) > 0 {
						m.answer = string(r[:len(r)-1])
					}
				} else if key == "space" {
					m.answer += " "
				} else if len([]rune(key)) == 1 {
					m.answer += key
				}
			}
			return m, nil
		}
		switch key {
		case "n":
			if !m.demo {
				m.form = freshForm()
				m.notice = ""
			}
		case "ctrl+c", "q":
			return m, tea.Quit
		case "tab":
			m.page = (m.page + 1) % 3
			m.offset = 0
		case "shift+tab":
			m.page = (m.page + 2) % 3
			m.offset = 0
		case "r":
			if m.demo {
				m.choose(m.selected)
			} else {
				return m, m.load()
			}
		case "o":
			return m, m.openReport()
		case "p":
			if m.demo && m.page == 2 {
				m.paused = !m.paused
			}
		case "enter":
			if m.page == 0 && len(m.runs) > 0 {
				m.page = 1
			} else if m.page == 1 {
				m.page = 2
			}
		case "up", "k":
			if m.page == 0 {
				m.choose(m.selected - 1)
				if !m.demo {
					return m, m.load()
				}
			} else if m.page == 1 && m.demo {
				m.cursor = max(0, m.cursor-1)
			} else {
				m.offset = min(max(0, len(m.data.Events)-1), m.offset+1)
			}
		case "down", "j":
			if m.page == 0 {
				m.choose(m.selected + 1)
				if !m.demo {
					return m, m.load()
				}
			} else if m.page == 1 && m.demo {
				m.cursor = min(2, m.cursor+1)
			} else {
				m.offset = max(0, m.offset-1)
			}
		case "pgup":
			if m.page == 2 {
				m.offset = min(max(0, len(m.data.Events)-1), m.offset+5)
			}
		case "pgdown":
			if m.page == 2 {
				m.offset = max(0, m.offset-5)
			}
		case "home":
			if m.page == 2 {
				m.offset = 0
			}
		case "space":
			if m.page == 1 && m.demo {
				m.draft[m.cursor] = !m.draft[m.cursor]
				m.dirty = true
			}
		case "1", "2", "3":
			if m.page == 1 && m.demo {
				i := int(key[0] - '1')
				m.cursor = i
				m.draft[i] = !m.draft[i]
				m.dirty = true
			}
			if m.demo && m.page == 2 && m.waiting {
				m.waiting = false
				m.data.add("local_evidence", "running", "ДЕМО: выбран вариант "+map[string]string{"1": "быстро", "2": "подробно", "3": "пропустить"}[key])
				m.step++
			}
		}
	}
	return m, nil
}

func (m model) openReport() tea.Cmd {
	root, id, demo := m.workspace, m.data.Run, m.demo
	return func() tea.Msg {
		var path string
		var err error
		if demo {
			executable, e := os.Executable()
			if e != nil {
				return openedMsg{e}
			}
			path = filepath.Join(filepath.Dir(executable), "demo-report.html")
		} else {
			path, err = within(root, filepath.Join("runs", id, "outputs", "human_report.html"))
			if err != nil {
				return openedMsg{err}
			}
		}
		if _, err = os.Stat(path); err != nil {
			return openedMsg{fmt.Errorf("отчёт ещё не создан: %w", err)}
		}
		var command *exec.Cmd
		switch runtime.GOOS {
		case "windows":
			command = exec.Command("rundll32", "url.dll,FileProtocolHandler", path)
		case "darwin":
			command = exec.Command("open", path)
		default:
			command = exec.Command("xdg-open", path)
		}
		return openedMsg{command.Run()}
	}
}

func (m model) View() tea.View {
	width := max(36, m.width-4)
	bodyHeight := max(5, m.height-11)
	if m.form != nil {
		view := tea.NewView(m.formView(width))
		view.AltScreen = true
		return view
	}
	mode := "HST · настройка и запуск через Cline · N — новый прогон"
	if m.demo {
		mode = "ДЕМО · синтетические события"
	}
	title := paint("1;34", "HST / УПРАВЛЕНИЕ ПРОГОНОМ · "+version+"")
	if m.control.ID != "" {
		controlLines := wrap(controlLabel(m.control.State)+": "+safe(m.control.Message), width)
		if q := m.control.Question; q != nil && q.State != "consumed" {
			controlLines = append(controlLines, wrap("ВОПРОС: "+safe(q.Text), width)...)
			if q.State == "pending" {
				for i, option := range q.Options {
					controlLines = append(controlLines, fmt.Sprintf("%d — %s", i+1, safe(option)))
				}
				if len(q.Options) == 0 {
					controlLines = append(controlLines, "Ответ: "+safe(m.answer)+" ▌ · Enter — отправить")
				}
			} else {
				controlLines = append(controlLines, "Ответ сохранён · ожидаю приёма исполнителем")
			}
		}
		title += "\n" + strings.Join(controlLines, "\n")
		bodyHeight = max(3, bodyHeight-len(controlLines))
	}
	if m.startup != "" {
		lines := wrap(m.startup, width)
		title += "\n" + paint("1;33", strings.Join(lines, "\n"))
		bodyHeight = max(3, bodyHeight-len(lines))
	}
	completed := 0
	for _, p := range m.data.Phases {
		if p.State == "completed" {
			completed++
		}
	}
	status := fmt.Sprintf("%s   %d/10 этапов", safe(m.data.Run), completed)
	if m.data.Validation != "" {
		status += "   Проверка: " + safe(m.data.Validation)
	}
	var tabs []string
	for i, label := range []string{"Прогоны", "Источники", "Журнал"} {
		if i == m.page {
			tabs = append(tabs, paint("1;34", "["+label+"]"))
		} else {
			tabs = append(tabs, label)
		}
	}
	var body []string
	switch m.page {
	case 0:
		body = append(body, "N — настроить новый прогон. Стрелки — прошлые, Enter — источники.", "")
		if len(m.runs) == 0 {
			body = append(body, "Прогонов пока нет. Начни новый прогон в Cline.")
		}
		start := max(0, m.selected-max(1, bodyHeight-4))
		for i := start; i < len(m.runs) && len(body) < bodyHeight; i++ {
			prefix := "  "
			if i == m.selected {
				prefix = "▶ "
			}
			line := prefix + safe(m.runs[i].ID)
			if i == m.selected {
				line = paint("1;34", line)
			}
			body = append(body, line)
		}
		body = append(body, "", "Выбор здесь меняет только просмотр.")
	case 1:
		if !m.demo {
			body = append(body, "ИСТОЧНИКИ ЭТОГО ПРОГОНА", "Сохранённые настройки и события · только чтение", "")
			for _, channel := range channels {
				body = append(body, wrap(channelName(channel)+": "+m.data.sourceSetting(channel), width)...)
				body = append(body, wrap("  "+m.data.sourceActivity(channel), width)...)
				body = append(body, "")
			}
			body = append(body, "Включение источника не подтверждает его чтение.", "Enter — показать журнал.")
		} else {
			body = append(body, "ИСТОЧНИКИ ДЕМОНСТРАЦИИ", "Space или 1/2/3 — переключить. Enter — показать журнал.", "")
			for i, label := range []string{"Локальная база знаний", "Confluence", "Интернет"} {
				mark := " "
				if m.draft[i] {
					mark = "✓"
				}
				prefix := "  "
				if i == m.cursor {
					prefix = "▶ "
				}
				line := fmt.Sprintf("%s[%s] %s", prefix, mark, label)
				if i == m.cursor {
					line = paint("1;34", line)
				}
				body = append(body, line)
			}
			body = append(body, "", "Выбор влияет только на демонстрацию.")
		}
	case 2:
		phaseRows := min(5, max(0, bodyHeight/3))
		logBudget := max(2, bodyHeight-phaseRows-3)
		body = append(body, "ЖУРНАЛ · новые сверху · ↑/↓ прокрутка · Home к свежим")
		if m.demo && m.waiting {
			body = append(body, paint("1;33", "Нужен выбор: 1 быстро · 2 подробно · 3 пропустить"))
			logBudget--
		}
		if m.demo && m.paused {
			body = append(body, paint("1;33", "Демонстрация на паузе · P продолжить"))
			logBudget--
		}
		if m.offset > 0 {
			body = append(body, fmt.Sprintf("История: отступ %d событий · Home вернёт новые", m.offset))
			logBudget--
		}
		count := 0
		for i := len(m.data.Events) - 1 - m.offset; i >= 0 && count < logBudget; i-- {
			e := m.data.Events[i]
			clock := "--:--:--"
			if t, err := time.Parse(time.RFC3339, e.At); err == nil {
				clock = t.In(time.FixedZone("МСК", 3*3600)).Format("15:04:05")
			}
			name := phaseName(e.Phase)
			if e.Channel != "" {
				name = channelName(e.Channel)
			}
			line := clock + "  " + stateName(e.State) + " · " + name + " · " + safe(e.Message)
			for _, part := range wrap(line, width) {
				if count >= logBudget {
					break
				}
				body = append(body, paint(stateColor(e.State), part))
				count++
			}
		}
		if len(m.data.Events) == 0 {
			body = append(body, "Журнал ещё не появился. R — обновить.")
		}
		body = append(body, "", "ЭТАПЫ · по порядку")
		for i := 0; i < len(m.data.Phases) && i < phaseRows*2; i += 2 {
			cells := []string{}
			for j := i; j < min(i+2, len(m.data.Phases)); j++ {
				p := m.data.Phases[j]
				mark := "·"
				if p.State == "completed" {
					mark = "✓"
				} else if p.State == "running" {
					mark = "▶"
				}
				cells = append(cells, fmt.Sprintf("%s %02d %s: %s", mark, j+1, phaseName(p.ID), stateName(p.State)))
			}
			body = append(body, strings.Join(cells, "  |  "))
		}
	}
	if len(body) > bodyHeight {
		body = body[:bodyHeight]
	}
	for len(body) < bodyHeight {
		body = append(body, "")
	}
	help := "N новый прогон · Tab экран · O отчёт · R обновить · Q выход (Cline продолжает)"
	if m.demo {
		help += " · P пауза демо"
	}
	notice := safe(m.notice)
	content := title + "\n" + mode + "\n" + status + "\n\n" + strings.Join(tabs, "   ") + "\n" + strings.Repeat("─", width) + "\n" + strings.Join(body, "\n") + "\n" + notice + "\n" + help
	view := tea.NewView(content)
	view.AltScreen = true
	view.WindowTitle = "HST · Bubble Tea prototype"
	return view
}

func main() {
	workspace := flag.String("workspace", "", "Корень DataB: настройка, запуск и просмотр")
	newRun := flag.Bool("new", false, "Сразу открыть настройку нового прогона")
	install := flag.Bool("install", false, "Установить текущий EXE и модуль связи VS Code")
	demo := flag.Bool("demo", false, "Демонстрация без записи файлов")
	showVersion := flag.Bool("version", false, "Версия сборки")
	flag.Parse()
	if *showVersion {
		fmt.Println(version)
		return
	}
	if *workspace != "" && *demo {
		fmt.Fprintln(os.Stderr, "Выбери --demo или --workspace")
		os.Exit(2)
	}
	m := model{demo: *demo || *workspace == "", width: 110, height: 36, draft: [3]bool{true, true, true}}
	if m.demo {
		m.runs = []run{{ID: "DEMO-001 · новый прогон"}, {ID: "DEMO-002 · завершён"}, {ID: "DEMO-003 · ошибка доступа"}}
		m.data = demoSnapshot(0)
	} else {
		root, err := filepath.EvalSymlinks(*workspace)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(2)
		}
		m.workspace, err = filepath.Abs(root)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(2)
		}
	}
	if *install {
		if m.demo {
			fmt.Fprintln(os.Stderr, "Нужен --workspace")
			os.Exit(2)
		}
		data, err := readFile(m.workspace, filepath.Join(".hst", "workspace.json"))
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(2)
		}
		var setup struct {
			Framework string `json:"framework_dir"`
		}
		json.Unmarshal(data, &setup)
		script, err := within(m.workspace, filepath.Join(setup.Framework, "scripts", "install_tui.py"))
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(2)
		}
		executable, _ := os.Executable()
		python := "python"
		if runtime.GOOS != "windows" {
			python = "python3"
		}
		command := exec.Command(python, script, "--workspace", m.workspace, "--binary", executable)
		command.Stdout = os.Stdout
		command.Stderr = os.Stderr
		if err = command.Run(); err != nil {
			os.Exit(1)
		}
		return
	}
	if *newRun && !m.demo {
		m.form = freshForm()
	}
	if _, err := tea.NewProgram(m).Run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

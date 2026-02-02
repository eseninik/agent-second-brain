# TickTick Integration

## Available MCP Tools

### Reading Tasks
- `get_projects` — all projects list
- `get_project_tasks` — tasks in specific project
- `get_all_tasks` — all tasks from all projects
- `search_tasks` — search by title, content, subtasks
- `get_tasks_due_today` — today's tasks
- `get_tasks_due_this_week` — next 7 days
- `get_overdue_tasks` — overdue tasks
- `get_tasks_by_priority` — filter by priority (0-5)

### Writing Tasks
- `create_task` — create new task
- `update_task` — modify existing
- `complete_task` — mark as done
- `delete_task` — remove task
- `batch_create_tasks` — create multiple at once

---

## Pre-Creation Checklist

### 1. Check Workload (REQUIRED)

```
get_tasks_due_this_week
```

Build workload map:
```
Mon: 2 tasks
Tue: 4 tasks  ← overloaded
Wed: 1 task
Thu: 3 tasks  ← at limit
Fri: 2 tasks
Sat: 0 tasks
Sun: 0 tasks
```

### 2. Check Duplicates (REQUIRED)

```
search_tasks:
  search_term: "key words from new task"
```

If similar exists → mark as duplicate, don't create.

---

## Priority Mapping

TickTick uses 0-5 priority scale:
- **5** (Highest) = p1 — срочно, критично, дедлайн клиента
- **3** (High) = p2 — важно, приоритет, до конца недели
- **1** (Medium) = p3 — нужно, надо, не забыть
- **0** (None) = p4 — strategic, R&D, long-term

### Priority by Domain

Based on user's work context (see [ABOUT.md](ABOUT.md)):

| Domain | Default Priority | TickTick Value | Override |
|--------|-----------------|----------------|----------|
| Migrator Work | p1-p2 | 5 или 3 | — |
| Company Ops (urgent) | p2 | 3 | — |
| Company Ops (regular) | p3 | 1 | — |
| Content (with deadline) | p2-p3 | 3 или 1 | — |
| Product/R&D | p4 | 0 | масштабируемость → 1 |
| AI & Tech | p4 | 0 | автоматизация → 1 |
| Personal | p3 | 1 | — |

### Priority Keywords

| Keywords in text | Priority Value |
|-----------------|----------------|
| срочно, критично, дедлайн, собственник | 5 (Highest) |
| важно, приоритет, до конца недели | 3 (High) |
| нужно, надо, не забыть | 1 (Medium) |
| (strategic, R&D, long-term) | 0 (None) |

### Apply Decision Filters for Priority Boost

If entry matches 2+ filters → boost priority by 1 level:
- Это масштабируется?
- Это можно автоматизировать?
- Это усиливает экспертизу/бренд?
- Это приближает к продукту/SaaS?

---

## Date Mapping

| Context | due_date format |
|---------|-----------------|
| **Migrator deadline** | exact date (YYYY-MM-DD) |
| **Urgent ops** | today / tomorrow |
| **This week** | this friday |
| **Next week** | next monday |
| **Strategic/R&D** | +7 days |
| **Not specified** | +3 days |

### Russian → due_date

| Russian | due_date |
|---------|----------|
| сегодня | today |
| завтра | tomorrow |
| послезавтра | +2 days |
| в понедельник | next monday |
| в пятницу | next friday |
| на этой неделе | this friday |
| на следующей неделе | next monday |
| через неделю | +7 days |
| 15 января | 2026-01-15 |

---

## Task Creation

```
create_task:
  title: "Task title"
  project_id: "project_id_here"  # MANDATORY
  due_date: "2026-01-27"         # MANDATORY
  priority: 3                     # based on domain (0-5)
  content: "Optional description"
```

### Task Title Style

User prefers: прямота, ясность, конкретика

✅ Good:
- "Отправить презентацию бот-квалификатора собственнику"
- "Созвон с командой по проекту NPC"
- "Написать пост про ИИ-агенты для Telegram"
- "Дописать функционал базы знаний"

❌ Bad:
- "Подумать о презентации"
- "Что-то с ботом"
- "Разобраться с AI"

### Workload Balancing

If target day has 3+ tasks:
1. Find next day with < 3 tasks
2. Use that day instead
3. Mention in report: "сдвинуто на {day} (перегрузка)"

---

## Project Detection

User's TickTick structure:

| Keywords | Project Name | project_id |
|----------|-------------|------------|
| ОП, собственник, бот-квалификатор, бот база знаний, оценка звонков, рейтинг ОП, NPC, контроль качества, Migrator | Migrator Work | (get from get_projects) |
| пост, Telegram, LinkedIn, контент, тезис, статья, личный бренд | Content | (get from get_projects) |
| книга, курс, обучение, узнал, изучить, learning | Learning | (get from get_projects) |
| здоровье, Полина, отношения, тренировка, питание, личное | Personal | (get from get_projects) |
| продукт, SaaS, MVP, гипотеза, ИИ-стартап | (create if needed or use Migrator Work) | — |

If unclear → create in **Migrator Work** (default for work tasks) or **Personal** (for personal).

---

## Tags System

TickTick supports tags. Recommended tags for user:

### Work-related:
- `#migrator` — связано с Migrator
- `#startup` — идеи для ИИ-стартапа
- `#urgent` — срочные задачи
- `#собственник` — требует внимания собственника

### Personal:
- `#здоровье` — тренировки, питание
- `#отношения` — Полина, семья
- `#развитие` — книги, курсы, навыки

### Content:
- `#telegram` — посты для Telegram
- `#linkedin` — контент для LinkedIn

Apply tags automatically based on keywords in entry.

---

## Anti-Patterns (НЕ СОЗДАВАТЬ)

Based on user preferences:

- ❌ "Подумать о..." → конкретизируй действие
- ❌ "Разобраться с..." → что именно сделать?
- ❌ Абстрактные задачи без Next Action
- ❌ Дубликаты существующих задач
- ❌ Задачи без дат
- ❌ Задачи без указания проекта

---

## Batch Creation for Multiple Tasks

When multiple tasks detected in one entry:

```
batch_create_tasks:
  tasks:
    - title: "Task 1"
      project_id: "..."
      due_date: "2026-01-27"
      priority: 3
    - title: "Task 2"
      project_id: "..."
      due_date: "2026-01-28"
      priority: 1
```

---

## Error Handling

CRITICAL: Никогда не предлагай "добавить вручную".

If `create_task` fails:
1. Include EXACT error message in report
2. Continue with next entry
3. Don't mark as processed
4. User will see error and can debug

WRONG output:
  "Не удалось добавить (MCP недоступен). Добавь вручную: Task title"

CORRECT output:
  "Ошибка создания задачи: [exact error from MCP tool]"

---

## Getting Project IDs

Before creating tasks, ALWAYS run:

```
get_projects
```

This returns list of projects with their IDs. Cache them for the session:
```
{
  "Migrator Work": "project_id_123",
  "Content": "project_id_456",
  "Learning": "project_id_789",
  "Personal": "project_id_000"
}
```

Use these IDs in `create_task` calls.

---

## Task Update Flow

When user wants to modify existing task:

1. Search for task: `search_tasks`
2. Get full details: `get_task`
3. Update: `update_task` with new parameters
4. Confirm in report

---

## Integration with Goals

When creating task, check alignment with user's goals (see [goals.md](goals.md)):

- **ONE Big Thing** (weekly focus) → priority +1 level
- **Monthly Top 3** → priority +1 level
- **Yearly goals** → add tag `#goal`

Example:
```
Entry: "Закончить бот-квалификатор"
→ Matches Monthly Priority 1 (ОП проекты)
→ Priority: 5 (Highest)
→ Project: Migrator Work
→ Tags: #migrator #urgent
```

---

## Report Format

After processing entries, include in daily report:

```html
<b>✅ Задачи созданы в TickTick:</b>
• [Migrator Work] Задача 1 (приоритет: Highest, 27 янв)
• [Learning] Задача 2 (приоритет: Medium, 30 янв)

<b>📊 Загрузка на неделю:</b>
Пн: 2 | Вт: 4 ⚠️ | Ср: 1 | Чт: 3 | Пт: 2

<b>⚠️ Внимание:</b>
• Вторник перегружен (4 задачи), некоторые сдвинуты на среду
```

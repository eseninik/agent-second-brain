# HTML Report Template

## CRITICAL: Output Format

**Return RAW HTML text only. No markdown wrappers.**

WRONG (markdown code block):
```html
<b>Title</b>
```

CORRECT (raw HTML):
<b>Title</b>

Output goes directly to Telegram `parse_mode=HTML`.

## Allowed Tags

<b> or <strong> — bold
<i> or <em> — italic
<code> — inline code
<pre> — code blocks
<s> or <strike> or <del> — strikethrough
<u> — underline
<a href="url">text</a> — links

## FORBIDDEN

NO markdown: **, ##, -, *, backticks
NO code blocks with triple backticks
NO tables (Telegram doesn't support)
NO unsupported tags: div, span, br, p, table, tr, td

## Template

📊 <b>Обработка за {DATE}</b>

<b>🎯 Текущий фокус:</b>
{ONE_BIG_THING from goals/3-weekly.md}

<b>📓 Сохранено мыслей:</b> {N}
• {emoji} {title} → {category}/

<b>✅ Создано задач:</b> {M}
• {task_name} <i>({priority}, {due})</i>

<b>📅 Загрузка на неделю:</b>
Пн: {n} | Вт: {n} | Ср: {n} | Чт: {n} | Пт: {n} | Сб: {n} | Вс: {n}

<b>⚠️ Требует внимания:</b>
• {count} просроченных задач
• Цель "{goal}" без активности {days} дней

<b>🔗 Новые связи:</b>
• [[Note A]] ↔ [[Note B]]

<b>⚡ Топ-3 приоритета на завтра:</b>
1. {task} <i>({goal if aligned})</i>
2. {task}
3. {task}

<b>📈 Прогресс по целям:</b>
• {goal_name}: {progress}% {emoji}

---
<i>Обработано за {duration}</i>

## Section Rules

### Focus (🎯)
Read from goals/3-weekly.md, find "ONE Big Thing" section.
If not found: "Не задан — обновите goals/3-weekly.md"

### Thoughts (📓)
Count saved, list with category emoji:
💡 idea, 🪞 reflection, 🎯 project, 📚 learning

### Tasks (✅)
Count created, list with priority and due date.
Format: • Task name <i>(p2, friday)</i>

### Week Load (📅)
Call get_tasks_due_this_week from TickTick, group by day.
Format: Пн: 4 | Вт: 2 | Ср: 3 | Чт: 1 | Пт: 5 ⚠️ | Сб: 0 | Вс: 0

Show ⚠️ if day has 4+ tasks (overloaded).

### Attention (⚠️)
ALWAYS show this section with:
1. **Overdue tasks** — use get_overdue_tasks from TickTick
2. **Stale goals** — goals with 7+ days no activity (SHOW EVERY DAY)
3. **Overloaded days** — days with 4+ tasks

Format:
```
<b>⚠️ Требует внимания:</b>
• 2 просроченные задачи
• Цель "Чтение книг" без активности 9 дней
• Пятница перегружена (5 задач)
```

### Links (🔗)
Show only if new links created.
Format: • [[Note A]] ↔ [[Note B]]

### Priorities (⚡)
Get tomorrow's tasks from TickTick (use get_tasks_due_tomorrow), sort by priority, show top 3.
Format: • Task name <i>(connected to goal if aligned)</i>

### Goals Progress (📈)
Read goals/1-yearly-2026.md (or 1-yearly-2025.md), show goals with recent activity.
Emojis: 🔴 0-25%, 🟡 26-50%, 🟢 51-75%, ✅ 76-100%

**CRITICAL:** Show goal stale alerts EVERY DAY if goal has no activity for 7+ days.
Format:
```
<b>⚠️ Требует внимания:</b>
• Цель "Чтение книг" без активности 9 дней
```

## Error Report

❌ <b>Ошибка обработки</b>

<b>Причина:</b> {error_message}
<b>Файл:</b> <code>{file_path}</code>

<i>Попробуйте /process снова</i>

## Empty Report

📭 <b>Нет записей для обработки</b>

Файл <code>daily/{date}.md</code> пуст.

<i>Добавьте записи в течение дня</i>

## Length Limit

Telegram max: 4096 characters.
If exceeds: truncate "Новые связи" first, then keep only top 3 goals.

## Validation Checklist

Before returning report:
1. All tags closed
2. No raw < or > in text (use &lt; &gt;)
3. No markdown syntax
4. No tables
5. Length under 4096 chars

---

## Example Report (Nikita's Real Scenario)

📊 <b>Обработка за 26 января 2026</b>

<b>🎯 Текущий фокус:</b>
Доработать текущие 5 проектов для ОП + начать новый проект для отдела исполнения

<b>📓 Сохранено мыслей:</b> 2
• 💡 AI-автоматизация для ОП → ideas/
• 🪞 Разговор с Полиной — подготовка → reflections/

<b>✅ Создано задач:</b> 5
• Внести правки в бот база знаний <i>(Highest, среда)</i>
• Доработать бот контроля качества <i>(Highest, четверг)</i>
• Созвон с Павлом — показать MVP <i>(Highest, пятница)</i>
• Тренировка на площадке <i>(Medium, завтра)</i>
• Прочитать главу 3 "Atomic Habits" <i>(Medium, вторник)</i>

<b>📅 Загрузка на неделю:</b>
Пн: 3 | Вт: 4 | Ср: 5 ⚠️ | Чт: 4 | Пт: 6 ⚠️ | Сб: 1 | Вс: 0

<b>⚠️ Требует внимания:</b>
• 1 просроченная задача: "Отправить отчёт собственнику"
• Среда и пятница перегружены (5-6 задач)

<b>⚡ Топ-3 приоритета на завтра:</b>
1. Внести правки в бот для оценки переписок <i>(→ Monthly: ОП проекты)</i>
2. Начать MVP для отдела исполнения <i>(→ Weekly focus)</i>
3. Тренировка на площадке <i>(→ Goal: Здоровье)</i>

<b>📈 Прогресс по целям:</b>
• Закрыть 5 проектов для ОП: 80% ✅ (доработка финальная)
• CTO с долей в Migrator: 60% 🟢 (активно доказываю ценность)
• Чтение 30+ книг: 8% 🔴 (3 книги за месяц)

---
<i>Обработано за 1.2 сек</i>

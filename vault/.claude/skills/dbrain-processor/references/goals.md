# Goals Integration

## ALWAYS Do First

Before processing daily entries:

1. **Read current focus:**
   ```
   Read goals/3-weekly.md → Extract ONE Big Thing
   ```

2. **Read yearly goals:**
   ```
   Read goals/1-yearly-2025.md (или 1-yearly-2026.md) → Know active goals by area
   ```

3. **Check monthly priorities:**
   ```
   Read goals/2-monthly.md → Top 3 priorities
   ```

## Goal Alignment

When creating a task, ask:

1. **Does it connect to ONE Big Thing?**
   - Yes → add to task description: `→ Weekly focus`
   - No → continue checking

2. **Does it connect to monthly priority?**
   - Yes → add: `→ Monthly: [Priority name]`
   - No → continue checking

3. **Does it connect to yearly goal?**
   - Yes → add: `→ Goal: [Goal name]`
   - No → mark as "operational"

## Task Priority Boost

If task aligns with goals, consider priority bump:

| Alignment | Default | Boost to |
|-----------|---------|----------|
| ONE Big Thing | p3 | p2 |
| Monthly priority | p3 | p2-p3 |
| Yearly goal | p4 | p3 |
| No alignment | p4 | p4 |

## Saving Thoughts

When saving to thoughts/:

1. **Check goal relevance:**
   - Scan goals/1-yearly-2025.md или goals/1-yearly-2026.md for matching areas
   - If matches → add link in frontmatter:
     ```yaml
     related:
       - "[[goals/1-yearly-2026#Career & Business]]"
     ```

2. **Tag with goal area:**
   ```
   #goal/career
   #goal/health
   #goal/learning
   ```

## Goal Progress Tracking

Track goal activity by:

- Task created → goal is "active"
- Thought saved → goal is "active"
- No activity 7+ days → "stale"
- No activity 14+ days → "warning"

## Report Section

Add to report:

```
<b>📈 Прогресс по целям:</b>
{for each active yearly goal with recent activity:}
• {goal}: {progress}% {status_emoji}

{if stale goals:}
<b>⚠️ Требует внимания:</b>
• Цель "{goal}" без активности {days} дней
```

## Goal File Parsing

### 3-weekly.md — Find ONE Big Thing

Look for pattern:
```markdown
> **If I accomplish nothing else, I will:**
> [THE ONE THING]
```

### 1-yearly-2026.md (or 2025.md) — Find Active Goals

Look for tables or structured goals:
```markdown
| Goal | Progress | Status |
|------|----------|--------|
| Goal name | X% | 🟡 |
```

Or look for sections:
```markdown
## Career & Business
- Goal: CTO с долей 2-3% в ИИ-стартапе
- Progress: [track based on tasks]
```

### 2-monthly.md — Find Top 3

Look for section:
```markdown
## Top 3 Priorities

1. **[Priority 1]**
2. **[Priority 2]**
3. **[Priority 3]**
```

## Example Alignment (Nikita's Real Scenario)

**Entry:** "Внести правки в бот база знаний по фидбэку от Кати"

**Check:**
- ONE Big Thing (week): "Доработать текущие 5 проектов для ОП" → ✅ Related
- Monthly #1: "Закрыть 5 проектов для отдела продаж" → ✅ Related
- Yearly: "CTO с долей в Migrator, доказать ценность" → ✅ Related

**Result:**
```
Title: Внести правки в бот база знаний
Description: По фидбэку от Кати → Weekly focus: Доработка проектов → Monthly: ОП проекты
Priority: 5 (Highest) — aligned with ONE Big Thing + Monthly #1
Project: Migrator Work
Tags: #migrator #urgent
Due: this week (до пятницы)
```

---

**Entry 2:** "Показать MVP проекта для отдела исполнения Павлу"

**Check:**
- ONE Big Thing (week): "Начать разработку проекта для отдела исполнения + показать MVP Павлу в пятницу" → ✅ Related
- Monthly #1: "Закрыть 5 проектов" → ✅ Related (новый проект = доп. ценность)
- Yearly: "CTO с долей, доказать ценность" → ✅ Related

**Result:**
```
Title: Созвон с Павлом — показать MVP
Description: Проект для отдела исполнения → Weekly focus: Новый проект
Priority: 5 (Highest)
Project: Migrator Work
Tags: #migrator #собственник
Due: пятница (31 января)
```

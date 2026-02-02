# Entry Classification

## Work Domains → Categories

Based on user's work context (see [ABOUT.md](ABOUT.md)):

### Migrator Work
ИИ-проекты для отделов компании (ОП, отдел исполнения), автоматизация процессов, задачи для собственника

**Keywords:** Migrator, ОП, отдел продаж, отдел исполнения, собственник, бот-квалификатор, бот база знаний, оценка звонков, рейтинг ОП, NPC, контроль качества, помощник, дедлайн, презентация, срочно, критично

**→ Category:** task (p1-p2) → TickTick

### AI & Tech
Инструменты, модели, промпты, пайплайны, агенты

**Keywords:** GPT, Claude, модель, агент, API, пайплайн, автоматизация, интеграция

**→ Category:** learning или project → thoughts/

### Product (ИИ-стартап)
Идеи для будущего ИИ-стартапа внутри Migrator, гипотезы, MVP, бизнес-модель

**Keywords:** продукт, SaaS, MVP, гипотеза, монетизация, юнит-экономика, стартап, ИИ-стартап, опционы

**→ Category:** idea или project → thoughts/

### Company Ops
Команда Migrator, процессы, управление, карьерный рост, взаимодействие с собственником

**Keywords:** команда, процесс, управление, карьера, CTO, доля, опционы, собственник, встреча, фидбэк, Migrator

**→ Category:** task или project (depends on urgency)

### Content
Посты, идеи, тезисы для будущего Telegram-канала и LinkedIn (личный бренд)

**Keywords:** пост, Telegram, LinkedIn, контент, тезис, статья, личный бренд, экспертиза

**→ Category:** idea → thoughts/ideas/ или task если с дедлайном

---

## Decision Tree

```
Entry text contains...
│
├─ Migrator project or deadline? ────────────────> TASK (p1-p2)
│  (ОП, собственник, бот, срочно, дедлайн, презентация)
│
├─ Operational/urgent? ──────────────────────────> TASK (p2-p3)
│  (нужно сделать, не забыть, позвонить, встреча)
│
├─ AI/tech learning? ────────────────────────────> LEARNING
│  (узнал, модель, агент, интеграция, курс, книга)
│
├─ Product/SaaS idea? ───────────────────────────> IDEA или PROJECT
│  (продукт, MVP, гипотеза, SaaS, ИИ-стартап)
│
├─ Strategic thinking? ──────────────────────────> PROJECT
│  (стратегия, план, R&D, долгосрочно, карьера, CTO)
│
├─ Personal insight? ────────────────────────────> REFLECTION
│  (понял, осознал, рефлексия, отношения, здоровье)
│
└─ Content idea? ────────────────────────────────> IDEA
   (пост, тезис, контент, Telegram, LinkedIn)
```

## Apply Decision Filters

Перед сохранением спроси:
- Это масштабируется?
- Это можно автоматизировать?
- Это усиливает экспертизу или бренд?
- Это приближает к продукту или SaaS?

Если да на 2+ вопроса → повысить приоритет.

---

## Photo Entries

For `[photo]` entries:

1. Analyze image content via vision
2. Determine domain:
   - Screenshot проекта Migrator → Migrator Work
   - Схема/диаграмма → AI & Tech или Product
   - Текст/статья/книга → Learning
   - Скриншот личных целей → Reflection
3. Add description to daily file

---

## Output Locations

| Category | Destination | Priority |
|----------|-------------|----------|
| task (Migrator) | TickTick | p1-p2 |
| task (ops) | TickTick | p2-p3 |
| task (content) | TickTick | p3-p4 |
| idea | thoughts/ideas/ | — |
| reflection | thoughts/reflections/ | — |
| project | thoughts/projects/ | — |
| learning | thoughts/learnings/ | — |

---

## File Naming

```
thoughts/{category}/{YYYY-MM-DD}-short-title.md
```

Examples:
```
thoughts/ideas/2026-01-26-ai-startup-pricing-model.md
thoughts/projects/2026-01-26-migrator-automation-pipeline.md
thoughts/learnings/2026-01-26-claude-mcp-setup.md
thoughts/reflections/2026-01-26-career-growth-insights.md
```

---

## Thought Structure

Use preferred format:

```markdown
---
date: {YYYY-MM-DD}
type: {category}
domain: {Migrator Work|AI & Tech|Product|Company Ops|Content|Personal}
tags: [tag1, tag2]
---

## Context
[Что привело к мысли]

## Insight
[Ключевая идея]

## Implication
[Что это значит для Migrator/ИИ-стартапа/карьеры/личных целей]

## Next Action
[Конкретный шаг — не абстрактный]
```

---

## Anti-Patterns (ИЗБЕГАТЬ)

При создании мыслей НЕ делать:
- Абстрактные рассуждения без Next Action
- Академическая теория без применения к вашему проекту/продукту
- Повторы без синтеза (кластеризуй похожие!)
- Хаотичные списки без приоритетов
- Задачи типа "подумать о..." (конкретизируй!)

---

## MOC Updates

After creating thought file, add link to:
```
MOC/MOC-{category}s.md
```

Group by domain when relevant:
```markdown
## AI & Tech
- [[2026-01-26-claude-mcp-setup]] - MCP integration for dbrain

## Product (ИИ-стартап)
- [[2026-01-26-ai-startup-pricing]] - Pricing research for future product

## Migrator Work
- [[2026-01-26-bot-qualifier-improvements]] - Bot-квалификатор optimization
```

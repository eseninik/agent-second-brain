"""TickTick task notifier — polls API every 3 min, notifies 10 min before tasks."""

import asyncio
import json
import logging
import time
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import httpx

from aiogram import Bot

from d_brain.config import Settings

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 180  # 3 minutes
NOTIFY_BEFORE_MINUTES = 10
WINDOW_EARLY = 9  # notify if task starts in [9..13] min
WINDOW_LATE = 13
MSK = timezone(timedelta(hours=3))

TICKTICK_BASE = "https://api.ticktick.com"


def _parse_ticktick_date(raw: str) -> datetime | None:
    """Parse TickTick date string to aware datetime.

    TickTick uses non-standard ISO format like ``2025-02-05T18:00:00.000+0000``
    (missing colon in tz offset).
    """
    if not raw:
        return None
    try:
        # Fix offset: +0000 → +00:00
        if len(raw) >= 5 and raw[-5] in ("+", "-") and ":" not in raw[-5:]:
            raw = raw[:-2] + ":" + raw[-2:]
        return datetime.fromisoformat(raw)
    except (ValueError, IndexError):
        logger.debug("Cannot parse TickTick date: %s", raw)
        return None


class TickTickNotifier:
    """Polls TickTick Open API and sends Telegram reminders."""

    def __init__(self, bot: Bot, settings: Settings) -> None:
        self._bot = bot
        self._settings = settings
        self._api_key = settings.ticktick_api_key
        self._sent_path = settings.vault_path / ".notifications" / "sent.jsonl"
        self._sent_keys: set[str] = set()
        self._projects_cache: dict[str, str] = {}  # id → name
        self._projects_cache_ts: float = 0

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _load_sent(self) -> None:
        if not self._sent_path.exists():
            return
        for line in self._sent_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    entry = json.loads(line)
                    self._sent_keys.add(entry["key"])
                except (json.JSONDecodeError, KeyError):
                    pass

    def _mark_sent(self, key: str) -> None:
        self._sent_keys.add(key)
        self._sent_path.parent.mkdir(parents=True, exist_ok=True)
        with self._sent_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"key": key, "ts": datetime.now(UTC).isoformat()}) + "\n")

    # ------------------------------------------------------------------
    # TickTick API helpers
    # ------------------------------------------------------------------
    async def _fetch_projects(self, client: httpx.AsyncClient) -> dict[str, str]:
        now = time.monotonic()
        if self._projects_cache and (now - self._projects_cache_ts) < 1800:
            return self._projects_cache

        resp = await client.get(f"{TICKTICK_BASE}/open/v1/project")
        resp.raise_for_status()
        projects = {p["id"]: p["name"] for p in resp.json()}
        self._projects_cache = projects
        self._projects_cache_ts = now
        return projects

    async def _fetch_tasks_for_project(
        self, client: httpx.AsyncClient, project_id: str
    ) -> list[dict]:
        resp = await client.get(f"{TICKTICK_BASE}/open/v1/project/{project_id}/data")
        resp.raise_for_status()
        data = resp.json()
        return data.get("tasks", [])

    # ------------------------------------------------------------------
    # Core loop
    # ------------------------------------------------------------------
    async def start(self) -> None:
        if not self._api_key:
            logger.warning("TickTick API key not set — notifier disabled")
            return

        self._load_sent()
        logger.info("TickTick notifier started (poll every %ds)", POLL_INTERVAL_SECONDS)

        headers = {"Authorization": f"Bearer {self._api_key}"}

        while True:
            try:
                async with httpx.AsyncClient(headers=headers, timeout=30) as client:
                    await self._poll(client)
            except Exception:
                logger.exception("TickTick poll error")

            await asyncio.sleep(POLL_INTERVAL_SECONDS)

    async def _poll(self, client: httpx.AsyncClient) -> None:
        projects = await self._fetch_projects(client)
        now = datetime.now(UTC)
        window_start = now + timedelta(minutes=WINDOW_EARLY)
        window_end = now + timedelta(minutes=WINDOW_LATE)

        for project_id, project_name in projects.items():
            try:
                tasks = await self._fetch_tasks_for_project(client, project_id)
            except httpx.HTTPStatusError as exc:
                logger.warning("Failed to fetch tasks for %s: %s", project_name, exc)
                continue

            for task in tasks:
                if task.get("isAllDay", False):
                    continue
                if task.get("status", 0) != 0:
                    continue

                start_date = _parse_ticktick_date(task.get("startDate", ""))
                if start_date is None:
                    continue

                if not (window_start <= start_date <= window_end):
                    continue

                key = f"{task['id']}:{task.get('startDate', '')}"
                if key in self._sent_keys:
                    continue

                # Send notification
                time_msk = start_date.astimezone(MSK).strftime("%H:%M")
                text = (
                    f"\U0001f514 Через {NOTIFY_BEFORE_MINUTES} минут: "
                    f"<b>{task['title']}</b>\n"
                    f"\u23f0 {time_msk} MSK\n"
                    f"\U0001f4c2 {project_name}"
                )

                for user_id in self._settings.allowed_user_ids:
                    try:
                        await self._bot.send_message(user_id, text)
                    except Exception:
                        logger.exception("Failed to notify user %s", user_id)

                self._mark_sent(key)
                logger.info("Notified: %s at %s", task["title"], time_msk)

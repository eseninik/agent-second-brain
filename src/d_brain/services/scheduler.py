"""Daily digest scheduler — fires at 18:00 UTC (21:00 MSK)."""

import asyncio
import logging
from datetime import UTC, date, datetime

from aiogram import Bot

from d_brain.bot.formatters import format_process_report
from d_brain.config import Settings
from d_brain.services.git import VaultGit
from d_brain.services.processor import ClaudeProcessor

logger = logging.getLogger(__name__)

DAILY_DIGEST_HOUR_UTC = 18  # 21:00 MSK
CHECK_INTERVAL_SECONDS = 60


async def start(bot: Bot, settings: Settings) -> None:
    """Run the daily digest loop.

    Checks every 60 seconds whether it's time to fire the digest.
    Guards against double-firing with ``_last_digest_date``.
    """
    last_digest_date: date | None = None
    logger.info("Scheduler started (digest at %02d:00 UTC)", DAILY_DIGEST_HOUR_UTC)

    while True:
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

        now = datetime.now(UTC)
        today = now.date()

        if now.hour != DAILY_DIGEST_HOUR_UTC:
            continue
        if last_digest_date == today:
            continue

        last_digest_date = today
        logger.info("Triggering daily digest for %s", today)

        try:
            processor = ClaudeProcessor(settings.vault_path, settings.ticktick_api_key)
            git = VaultGit(settings.vault_path)

            report = await asyncio.to_thread(processor.process_daily, today)

            if "error" not in report:
                await asyncio.to_thread(
                    git.commit_and_push,
                    f"chore: process daily {today.isoformat()}",
                )

            formatted = format_process_report(report)

            for user_id in settings.allowed_user_ids:
                try:
                    await bot.send_message(user_id, formatted)
                except Exception:
                    logger.exception("Failed to send digest to user %s", user_id)

            logger.info("Daily digest sent successfully")
        except Exception:
            logger.exception("Daily digest failed")

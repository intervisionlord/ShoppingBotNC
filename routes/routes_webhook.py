"""Роуты для обработки вебхуков Telegram"""

from fastapi import APIRouter, Request

from handlers.handler_bot import process_update
from handlers.handler_logging import logger

webhook_router = APIRouter(tags=["webhook"])
WEBHOOK_PATH = "/webhook"


@webhook_router.post(WEBHOOK_PATH)
async def telegram_webhook(update: Request):
    """Ручка для вебхука Telegram"""
    try:
        update_data = await update.json()
        await process_update(update_data)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука: {e}")
        return {"ok": False, "error": str(e)}

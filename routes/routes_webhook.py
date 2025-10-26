from fastapi import APIRouter, Request
from handlers.handler_logging import logger
from handlers.handler_bot import process_update

# Создаем роутер для вебхука
webhook_router = APIRouter(tags=["webhook"])

# Простой путь без токена
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


@webhook_router.get(WEBHOOK_PATH)
async def webhook_debug():
    """Отладочная ручка для проверки вебхука"""
    return {
        "message": "Webhook endpoint is active",
        "path": WEBHOOK_PATH,
        "method": "Use POST for Telegram webhooks",
    }

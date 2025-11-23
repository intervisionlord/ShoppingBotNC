"""Основной хендлер бота"""

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from config.settings import settings
from handlers.bot_routes.routes_deck import nc_deck_router
from handlers.handler_logging import logger

# Инициализация бота
BOT_INSTANCE = Bot(token=settings.BOT_TOKEN) if settings.BOT_TOKEN else None
dispatcher = Dispatcher()
dispatcher.include_router(nc_deck_router)

logger.info("Бот списка покупок инициализирован")


async def process_update(update_data: dict) -> None:
    """Обработка обновления от Telegram"""
    if not BOT_INSTANCE:
        logger.warning("Получено обновление, но бот не инициализирован")
        return

    tg_update = Update(**update_data)
    await dispatcher.feed_webhook_update(BOT_INSTANCE, tg_update)


async def setup_webhook(webhook_url: str) -> None:
    """Настройка вебхука"""
    if not BOT_INSTANCE:
        logger.warning("Попытка настроить вебхук без бота")
        return

    await BOT_INSTANCE.delete_webhook()
    await BOT_INSTANCE.set_webhook(webhook_url)
    logger.info(f"Вебхук установлен: {webhook_url}")


async def close_bot_session() -> None:
    """Закрытие сессии бота"""
    if BOT_INSTANCE:
        await BOT_INSTANCE.session.close()

"""Основной хендлер бота"""

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from config.settings import settings
from handlers.bot_routes.routes_deck import nc_deck_router
from handlers.handler_logging import logger

# Инициализация бота
bot = Bot(token=settings.BOT_TOKEN) if settings.BOT_TOKEN else None
dispatcher = Dispatcher()

# Главный роутер Deck
dispatcher.include_router(nc_deck_router)

logger.info("Бот инициализирован")


async def process_update(update_data: dict) -> None:
    """
    Обработка обновления от Telegram

    :param update_data: Описание
    :type update_data: dict
    """
    if not bot:
        logger.warning("Получено обновление, но бот не инициализирован")
        return

    tg_update = Update(**update_data)
    await dispatcher.feed_webhook_update(bot, tg_update)


async def setup_webhook(webhook_url: str) -> None:
    """
    Настройка вебхука

    :param webhook_url: Описание
    :type webhook_url: str
    """
    if not bot:
        logger.warning("Попытка настроить вебхук без бота")
        return

    await bot.delete_webhook()
    await bot.set_webhook(webhook_url)
    logger.info(f"Вебхук установлен: {webhook_url}")


async def close_bot_session() -> None:
    """
    Закрытие сессии бота
    """
    if bot:
        await bot.session.close()

"""Основной хендлер бота"""

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from config.settings import settings
from handlers.bot_routes.base_routes import base_router
from handlers.bot_routes.nc_deck_routes import nc_deck_router
from handlers.handler_logging import logger

# Инициализация бота
bot = (  # pylint: disable=C0103:invalid-name
    Bot(token=settings.BOT_TOKEN) if settings.BOT_TOKEN else None
)
dispatcher = Dispatcher()

# Регистрируем роутеры бота
dispatcher.include_router(base_router)
dispatcher.include_router(nc_deck_router)

logger.info("Бот инициализирован")


async def process_update(update_data: dict) -> None:
    """
    Обработка обновления от Telegram

    :param update_data: Обновление от телеграм
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

    :param webhook_url: Передаваемый вебхук
    :type webhook_url: str
    """
    if not bot:
        logger.warning("Попытка настроить вебхук без бота")
        return

    await bot.delete_webhook()
    await bot.set_webhook(webhook_url)
    logger.info(f"Вебхук установлен: {webhook_url}")


async def close_bot_session() -> None:
    """Закрытие сессии бота"""
    if bot:
        await bot.session.close()

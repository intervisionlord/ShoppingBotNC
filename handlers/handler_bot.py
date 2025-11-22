"""Класс для управления Telegram ботом"""

from typing import Optional
from aiogram import Bot, Dispatcher
from aiogram.types import Update

from config.settings import settings
from routes_bot.router_main import main_router
from handlers.handler_logging import logger


class ShoppingBotNC:
    """Синглтон класс для управления Telegram ботом"""

    _instance: Optional["ShoppingBotNC"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self.bot: Optional[Bot] = None
            self.dispatcher: Optional[Dispatcher] = None
            self._initialized = True

    async def initialize(self) -> None:
        """Инициализация бота"""
        if not settings.BOT_TOKEN:
            logger.warning("Токен бота не установлен")
            return

        self.bot = Bot(token=settings.BOT_TOKEN)
        self.dispatcher = Dispatcher()
        self.dispatcher.include_router(main_router)

        logger.success("Бот списка покупок инициализирован")

    async def process_update(self, update_data: dict) -> None:
        """Обработка обновления от Telegram"""
        if not self.bot or not self.dispatcher:
            logger.warning("Бот не инициализирован")
            return

        tg_update = Update(**update_data)
        await self.dispatcher.feed_webhook_update(self.bot, tg_update)

    async def setup_webhook(self, webhook_url: str) -> None:
        """Настройка вебхука"""
        if not self.bot:
            logger.warning("Бот не инициализирован")
            return

        await self.bot.delete_webhook()
        await self.bot.set_webhook(webhook_url)
        logger.info(f"Вебхук установлен: {webhook_url}")

    async def close(self) -> None:
        """Закрытие сессии бота"""
        if self.bot:
            await self.bot.session.close()
            self.bot = None
            self.dispatcher = None
            logger.info("Сессия бота закрыта")

    @property
    def is_initialized(self) -> bool:
        """Проверка инициализации бота"""
        return self.bot is not None and self.dispatcher is not None


bot = ShoppingBotNC()
